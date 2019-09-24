# imports
import os
import datetime
from . import db, create_app
import cloudinary
from .models import User
from bson import ObjectId
from functools import wraps
from ast import literal_eval
from dotenv import load_dotenv
from cloudinary import uploader
from .controllers import upload
from mailer import Mailer, Message
from bcrypt import hashpw, gensalt
from flask_pymongo import MongoClient
from .forms import RegisterForm, DetailForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request, jsonify, Blueprint, session, make_response

# initialise blueprint
main = Blueprint('main', __name__)

# load env variables from the .env file
load_dotenv(verbose=True)

# mongodb configurations
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, connect=False, connectTimeoutMS=30000)
mongo = client.get_database('offers')

# routes
@main.route('/adduser', methods=['POST', 'GET'])
@login_required
def adduser():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        # user details
        name = form.name.data
        username = form.username.data
        email = form.email.data
        passw = form.password.data
        role = form.role.data

        try:
            registered_user = User.objects(email=email).first()
            if registered_user:
                error = 'a user with that email already exists'
                print(error)
                return render_template('register.html', form=form, error=error)

            password = hashpw(passw.encode('utf-8'), gensalt(rounds=12))

            new_user = User(name, email, username, role, password)

            new_user.save()
            return redirect(url_for('main.show_offers')), 200
        except Exception as error:
            print(error)
            error = 'something went wrong, please try again'
            return render_template('register.html', error=error), 400
    return render_template('register.html', form=form)


# login route
@main.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated == True:
        return redirect(url_for('main.show_offers'))
    if request.method == 'POST':
        # get value from field
        try:
            pass_candidate = form.password.data
            username = form.username.data
            # get user by username
            log_user = User.objects(username=username).first()

            if log_user:
                # check if password is same as one in the db
                if hashpw(pass_candidate.encode('utf-8'), log_user['password'].encode('utf-8')) == log_user['password'].encode('utf-8'):
                    session.permanent = True
                    login_user(log_user, remember=True,
                               duration=datetime.timedelta(hours=24))
                    msg = 'Welcome, you have logged in successfully'
                    return redirect(url_for('main.show_offers'))
                else:
                    error = 'invalid login, check username or password'
                    return render_template('login.html', form=form, error=error), 400
            else:
                error = 'this user does not exist'
                print(error)
                return render_template('login.html', form=form, error=error), 400
        except Exception as error:
            print(error)
            err = 'Error, something went wrong'
            return render_template('login.html', form=form, error=err), 400
    return render_template('login.html', form=form)


# route to logout user
@main.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# route to add an offer
@main.route('/addoffer', methods=['POST', 'GET'])
@login_required
def add_offer():
    form = DetailForm()
    if request.method == 'POST':

        # get files from input files
        files = form.file.data
        images = []
        for f in files:
            # upload each file
            result = upload(f)
            # append result to empty list
            images.append(result)

        title = form.title.data
        overview = form.overview.data
        itinerary = form.itinerary.data
        inclusion = form.inclusion.data
        price = form.price.data
        destination = form.destination.data
        addinfo = form.addinfo.data

        destinations = list(destination.split(','))
        print(destinations)

        offer_item = {
            'Title': title,
            'Overview': overview,
            'Itinerary': itinerary,
            'Inclusion': inclusion,
            'Price': price,
            'AddInfo': addinfo,
            'Images':  images,
            'Destination': destinations,
            'CreatedAt': datetime.datetime.now()
        }

        try:
            offers = mongo.offers
            offers.insert_one(offer_item)
            return redirect(url_for('main.show_offers')), 200

        except Exception as err:
            print(err)
            error = 'something went wrong, try again'
            return render_template('add_offers.html', form=form, error=error), 400

    return render_template('add_offers.html', form=form)


# show the offers available
@main.route('/showOffers', methods=['GET'])
@login_required
def show_offers():
    if request.method == 'GET':
        output = []
        try:
            offer = mongo.offers
            proxy = os.getenv('PROXY')
            offers = offer.find()
            for offer in offers:
                if offer:
                    output.append({
                        'id': offer['_id'],
                        'title': offer['Title'],
                        'overview': offer['Overview'],
                        'itinerary': offer['Itinerary'],
                        'inclusion': offer['Inclusion'],
                        'price': offer['Price'],
                        'addinfo': offer['AddInfo'],
                        'images': offer['Images'],
                        'created': offer['CreatedAt']
                    })

            return render_template('offers.html', output=output, proxy=proxy)
        except Exception as error:
            print(error)
            return jsonify({'Message': 'something went wrong'})

    return render_template('offers.html')


# route to edit offer
@main.route('/editOffer/<string:id>', methods=['POST', 'GET'])
@login_required
def edit_offer(id):
    # get the form model
    form = DetailForm(request.form)
    # get details from db
    # connect to db
    offers = mongo.offers
    # find offers
    offer = offers.find_one({'_id': ObjectId(id)})
    images = offer['Images']
    offer_id = offer['_id']
    location = ','.join(offer['Destination'])

    # add data to the fields
    form.file.data = images
    form.title.data = offer['Title']
    form.overview.data = offer['Overview']
    form.itinerary.data = offer['Itinerary']
    form.inclusion.data = offer['Inclusion']
    form.price.data = offer['Price']
    form.destination.data = location
    form.addinfo.data = offer['AddInfo']

    # post the updated information
    # If method == post
    if request.method == 'POST':
        # get the new new form data
        files = request.files.getlist('file')
        for file in files:
            if not file:
                images = form.file.data
            else:
                result = upload(file)
                images.insert(0, result)

        title = request.form.get('title')
        overview = request.form.get('overview')
        itinerary = request.form.get('itinerary')
        inclusion = request.form.get('inclusion')
        price = request.form.get('price')
        destination = request.form.get('destination')
        addinfo = request.form.get('addinfo')

        destinations = destination.split(',')

        # create the update object with all updated data
        update = {'$set': {
            "Images": images,
            "Title": title,
            "Overview": overview,
            "Itinerary": itinerary,
            "Inclusion": inclusion,
            "Price": price,
            "Destination": destinations,
            "AddInfo": addinfo,
            'CreatedAt': datetime.datetime.now()
        }
        }
        # call the update function in mongo and pass the update
        try:
            offers.update_one({'_id': ObjectId(id)},
                              update=update, upsert=True)
            return redirect(url_for('main.show_offers'))
        except Exception as error:
            print(error)
            flash('Error, something went wrong')
            return redirect(url_for('main.show_offers')), 400
    return render_template('edit_offers.html', form=form, images=images, offer_id=offer_id)


# route to delete an offer
@main.route('/delete/<string:id>', methods=['POST', 'GET'])
@login_required
def delete_offer(id):
    if request.method == 'POST':
        # connect to the database
        offers = mongo.offers
        # find item to delete
        try:
            offers.delete_one({'_id': ObjectId(id)})
            return redirect(url_for('main.show_offers'))
        except Exception as error:
            print(error)
            return redirect(url_for('main.show_offers'))
    return render_template('offers.html')
