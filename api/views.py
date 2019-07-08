# imports

from . import db
from flask import render_template, redirect, url_for, flash, request, jsonify, Blueprint, session
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
from bcrypt import hashpw, gensalt
from .forms import RegisterForm, DetailForm, LoginForm
from functools import wraps
from bson import ObjectId
import os
import datetime
import cloudinary
from cloudinary import uploader
from dotenv import load_dotenv
from ast import literal_eval
from mailer import Mailer, Message
from .controllers import upload
from flask_pymongo import MongoClient

# initialise blueprint
api = Blueprint('api', __name__)

# load env variables from the .env file
load_dotenv(verbose=True)

# mongodb configurations
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, connect=False, connectTimeoutMS=30000)
mongo = client.get_database('offers')


# define routes

# index route
@api.route('/')
def index():
    return render_template('index.html')

# register route
@api.route('/register', methods=['POST'])
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
@api.route('/login', methods=['POST', 'GET'])
def login():
    #form = LoginForm()
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
                    return redirect(url_for('api.show_offers'))
                else:
                    error = 'invalid login, check username of password'
                    return render_template('login.html', error=error)
            else:
                error = 'username not found'
                flash('username not found', 'danger')
                return render_template('login.html', error=error)
        except Exception as error:
            print('could not continue due to ', error)
    return render_template('login.html')


# get all users route
@api.route('/getusers', methods=['GET'])
def get_users():
    if request.method == 'GET':
        # get all the users
        output = []
        users = User.query.all()

        for usr in users:
            output.append({
                'username': usr.username,
                'password': usr.password.decode('utf-8'),
                'email': usr.email,
                'name': usr.name
            })
            print(output)

        return jsonify({'Output': output})
    return jsonify({'msg': 'method not allowed'}), 405


# route to logout user
@api.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    clear()
    return redirect(url_for('api.login'))


# show the offers available
@api.route('/showOffers', methods=['GET'])
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
    msg = 'Method not allowed'
    return render_template('offers.html', msg=msg)


# sreturn offer to frontend
@api.route('/api/getOffer', methods=['GET'])
def get_offers():
    if request.method == 'GET':
        output = []
        try:
            offer = mongo.offers
            print("successfully connected to collection")

            offers = offer.find()
            for offer in offers:
                if offer:
                    output.append({
                        # 'id': offer['_id'],
                        'title': offer['Title'],
                        'overview': offer['Overview'],
                        'itinerary': offer['Itinerary'],
                        'inclusion': offer['Inclusion'],
                        'price': offer['Price'],
                        'addinfo': offer['AddInfo'],
                        'images': offer['Images'],
                        'created': offer['CreatedAt']
                    })

            return jsonify(output)
        except Exception as err:
            print("could not connect to collection due to ", err)
    return jsonify({'msg': 'method not allowed'}), 405


# route to add an offer


@api.route('/api/addOffer', methods=['POST', 'GET'])
def add_offer():
    form = DetailForm()
    if request.method == 'POST':
        files = request.files.getlist('file')
        file = []
        for f in files:
            result = upload(f)
            file.append(result)

        title = request.form['title']
        overview = request.form['overview']
        itinerary = request.form['itinerary']
        inclusion = request.form['inclusion']
        price = request.form['price']
        addinfo = request.form['addinfo']

        offer_item = {
            'Title': title,
            'Overview': overview,
            'Itinerary': itinerary,
            'Inclusion': inclusion,
            'Price': price,
            'AddInfo': addinfo,
            'CreatedAt': datetime.datetime.now(),
            'Images':  file
        }

        try:
            offers = mongo.offers
            print("connected successfully to collection")
        except Exception as err:
            print('could not connect to collection due to ', err)

        try:
            offers.insert_one(offer_item)
            flash("added offer successfully", 'success')
            return redirect(url_for('api.show_offers'))

        except Exception as err:
            flash('could not add offer due to ' + str(err), 'danger')

    return render_template('add_offers.html')

# route to delete an offer
@api.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_offer(id):
    if request.method == 'GET':
        # connect to the database
        offers = mongo.offers

        # find item to delete
        offers.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('api.show_offers'))
        flash('item deleted', 'success')
    return render_template('offers.html')


# route to edit offer
@api.route('/editOffer/<string:id>', methods=['POST', 'GET', 'PATCH'])
@login_required
def edit_offer(id):
    # connect to the database

    # get form
    form = DetailForm(request.form)
    data = request.form

    if request.method == 'PATCH':
        title = request.form['title']
        overview = request.form['overview']
        itinerary = request.form['itinerary']
        inclusion = request.form['inclusion']
        price = request.form['price']
        addinfo = request.form['addinfo']

        update_offer = {
            'Title': title,
            'Overview': overview,
            'Itinerary': itinerary,
            'Inclusion': inclusion,
            'Price': price,
            'AddInfo': addinfo,
            'CreatedAt': datetime.datetime.now(),
        }

        # connect to db
        offers = mongo.offers

        # find one and update
        offers.find_one_and_update(
            filter={'_id': ObjectId(id)}, update=update_offer)

        flash('Offer has been updated', 'success')
        print('updated successfully')

        return redirect(url_for('api.show_offers'))
    return render_template('edit_offers.html', form=form)

# data from frontend
@api.route('/api/uploadDetail', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        data = request.data
        new_data = literal_eval(data.decode('utf-8'))

        msg_string = 'Name: ' + new_data['Name'] + '\n' + 'Email: ' + new_data['Email'] + '\n' + ' Nationality: ' + new_data['Nationality'] + '\n' + ' Number: ' + new_data['Number'] + '\n' + ' Departure: ' + \
            new_data['Departure'] + '\n' + ' Adults: ' + new_data['Adults'] + '\n' + ' Children: ' + \
            new_data['Children'] + '\n' + \
            ' Additional information: ' + new_data['Info']

        # sending email information to vacay email
        msg = Message(From=new_data['Email'],
                      To='newtonmbugua95@gmail.com', charset='utf-8')
        msg.CC = 'newtonmbugua95@gmail.com'
        msg.Subject = new_data['Package']
        msg.Body = msg_string

        sender = Mailer(host='smtp.gmail.com', use_tls=True)
        usr = 'mymbugua@gmail.com'
        pwd = 'Ahou-smil3y-fac3'
        sender.login(usr, pwd)
        sender.send(msg)

        print('** email sent ***')

        # email object
        email_object = {
            'Name': new_data['Name'],
            'Email': new_data['Email'],
            'Nationality': new_data['Nationality'],
            'Package': new_data['Package'],
            'Depature': new_data['Departure'],
            'Adult': new_data['Adults'],
            'Children': new_data['Children'],
            'Bugdet': new_data['Budget'],
            'Addinfo': new_data['Info'],
            'CreadetAt': datetime.datetime.now()
        }

        # connect to database
        try:
            emails = db.emails
            emails.insert_one(email_object)
            print('*** added to the database ***')
        except Exception as error:
            print('could not add to the database due to', error)
    else:
        msg = 'Page not available'
        return render_template('notfound.html', msg=msg)

    return jsonify(email_object)
