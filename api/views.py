# imports
import os
import datetime
from . import db
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
from flask import render_template, redirect, url_for, flash, request, jsonify, Blueprint

# initialise blueprint
main = Blueprint('main', __name__)

# load env variables from the .env file
load_dotenv(verbose=True)

# mongodb configurations
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, connect=False, connectTimeoutMS=30000)
mongo = client.get_database('offers')


# define routes

# index route
@main.route('/')
def index():
    return render_template('index.html')

# register route
@main.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # get the json information to create a user
        user = request.get_json()

        # user details
        name = user['name']
        username = user['username']
        email = user['email']
        passw = user['password']
        role = user['role']

        # before adding user check that they are not null ::Todo

        new_user = User(name=name, email=email, username=username,
                        role=role, password=hashpw(passw.encode('utf-8'), gensalt()))

        try:
            db.session.add(new_user)
            db.session.commit()
            print('*** user added ***')
            return jsonify({'msg': 'user added successfully'})
        except Exception as error:
            print(error)
            return jsonify({'msg': 'found error'})

    return jsonify({'msg': 'method not allowed'}), 405


# login route
@main.route('/login', methods=['POST', 'GET'])
def login():
    # form = LoginForm()
    if request.method == 'POST':
        # get value from field
        try:
            pass_candidate = request.form['password']
            username = request.form['username']
            # get user by usernamr
            log_user = User.query.filter_by(username=username).first()

            if log_user:
                # check if password is same as one in the db
                if hashpw(pass_candidate.encode('utf-8'), log_user.password) == log_user.password:
                    login_user(log_user, remember=True,
                               duration=datetime.timedelta(minutes=40))
                    flash('you have been logged in successfully', 'success')
                    return redirect(url_for('main.show_offers'))
                else:
                    error = 'invalid login, check username or password'
                    return render_template('login.html', error=error)
            else:
                error = 'username not found'
                flash('username not found', 'danger')
                return render_template('login.html', error=error)
        except Exception as error:
            print('could not continue due to ', error)
    return render_template('login.html')


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
        file = []
        for f in files:
            # upload each file
            result = upload(f)
            # append result to empty list
            file.append(result)

        title = form.title.data
        overview = form.overview.data
        itinerary = form.itinerary.data
        inclusion = form.inclusion.data
        price = form.price.data
        addinfo = form.addinfo.data

        offer_item = {
            'Title': title,
            'Overview': overview,
            'Itinerary': itinerary,
            'Inclusion': inclusion,
            'Price': price,
            'AddInfo': addinfo,
            'Images':  file,
            'CreatedAt': datetime.datetime.now()
        }

        try:
            offers = mongo.offers
            print("connected successfully to collection")
            offers.insert_one(offer_item)
            flash("added offer successfully", 'success')
            return redirect(url_for('main.show_offers'))

        except Exception as err:
            flash('we have a problem ' + str(err), 'danger')
            msg = 'you face a problem please try again'
            return render_template('add_offers.html', msg=msg), jsonify({'Message': 'we found a problem ' + err})

    return render_template('add_offers.html', form=form)


# show the offers available
@main.route('/showOffers', methods=['GET'])
@login_required
def show_offers():
    if request.method == 'GET':
        output = []
        try:
            offer = mongo.offers
            print("successfully connected to collection")

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

            return render_template('offers.html', output=output)
        except Exception as err:
            print("could not connect to collection due to ", err)

    return render_template('offers.html')


# route to edit offer
@main.route('/editOffer/<string:id>', methods=['POST', 'GET'])
@login_required
def edit_offer(id):
    # get the form
    form = DetailForm(request.form)

    # connect to db and get offer
    offers = mongo.offers
    offer = offers.find_one({'_id': ObjectId(id)})

    # images
    images = offer['Images']

    # populate  fields
    form.file.data = images
    form.title.data = offer['Title']
    form.overview.data = offer['Overview']
    form.itinerary.data = offer['Itinerary']
    form.inclusion.data = offer['Inclusion']
    form.price.data = offer['Price']
    form.addinfo.data = offer['AddInfo']

    if request.method == 'POST':
        # get files from input files
        files = form.file.data
        file = offer['Images']
        for f in files:
            if not f:
                return file
                # upload each file
            result = upload(f)
            # append result to empty list
        file.append(result)
        print(file)

        title = request.form['title']
        overview = request.form['overview']
        itinerary = request.form['itinerary']
        inclusion = request.form['inclusion']
        price = request.form['price']
        addinfo = request.form['addinfo']

        update = {'Title': title,
                  'Overview': overview,
                  'Itinerary': itinerary,
                  'Inclusion': inclusion,
                  'Price': price,
                  'AddInfo': addinfo,
                  'Images': file,
                  'CreatedAt': datetime.datetime.now()
                  }

        offers.update({'_id': ObjectId(id)}, update, True)

        print('article successfully edited')
        return redirect(url_for('main.show_offers'))
    return render_template('edit_offers.html', form=form, images=images)


# route to delete an offer
@main.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_offer(id):
    if request.method == 'GET':
        # connect to the database
        offers = mongo.offers

        # find item to delete
        offers.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('main.show_offers'))
        flash('item deleted', 'success')
    return render_template('offers.html')
