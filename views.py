# imports

from app import app
from flask import render_template, redirect, url_for, flash, request, abort, session, jsonify
from bson import ObjectId
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from bcrypt import hashpw, gensalt
from forms import RegisterForm, DetailForm, LoginForm
from functools import wraps
from flask_pymongo import MongoClient
import os
import datetime
from flask_dropzone import Dropzone as Drop
import cloudinary
from cloudinary import uploader
from dotenv import load_dotenv

# load env variables from the .env file
load_dotenv(verbose=True)


# Mongodb configurations
try:
    client = MongoClient(os.getenv('MONGO_URI'),
                         connect=False, connectTimeoutMS=40000)
    db = client.offers
    print('*** connected to the database successfully ***')
except Exception as error:
    print('*** database connection failed ***', error)


# functions
def upload(file):
    if request.method == 'POST':
        res = cloudinary.uploader.upload(file, folder='Projects/vacay')
        result = res['secure_url']

    return result


# droparea
# initialise dropzone
dropzone = Drop(app)


# check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthoried, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# define routes

# index route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    #form = LoginForm()
    if request.method == 'POST':
        # get value from field
        try:
            pass_candidate = request.form['password']

            # get user by usernamr
            users = db.users
            log_user = users.find_one(
                filter={'username': request.form['username']})

            if log_user:
                # check if password is same as one in the db
                if hashpw(pass_candidate.encode('utf-8'), log_user['password']) == log_user['password']:
                    # check for role
                    if log_user['role'] is not '' and log_user['role'] is not None:
                        # login the user
                        #user = log_user['username']
                        # login_user(user)
                        session['logged_in'] = True
                        session['username'] = log_user['username']
                        session['role'] = log_user['role']
                        session.permanent = True

                        flash('you have been logged in successfully', 'success')

                        return redirect(url_for('show_offers'))

                    else:
                        error = 'you must have a role to login'
                        return render_template('login.html', error=error)
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


# route to logout user
@app.route('/logout', methods=['POST', 'GET'])
@is_logged_in
def logout():
    # logout_user()
    # return redirect(url_for('index'))
    if session['username']:
        del session['username']
        session['logged_in'] = False
        session.permanent = False
        flash('you are now logged out')
        return redirect(url_for('login'))

    flash('user logged out')
    return render_template('login.html')


# show the offers available
@app.route('/showOffers')
@is_logged_in
def show_offers():
    if request.method == 'GET':
        output = []
        try:
            offer = db.offers
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

        except Exception as err:
            print("could not connect to collection due to ", err)
    return render_template('offers.html', output=output)


# sreturn offer to frontend
@app.route('/api/getOffer', methods=['GET'])
def get_offers():
    if request.method == 'GET':
        output = []
        try:
            offer = db.offers
            print("successfully connected to collection")

            offers = offer.find()
            for offer in offers:
                if offer:
                    output.append({
                        #'id': offer['_id'],
                        'title': offer['Title'],
                        'overview': offer['Overview'],
                        'itinerary': offer['Itinerary'],
                        'inclusion': offer['Inclusion'],
                        'price': offer['Price'],
                        'addinfo': offer['AddInfo'],
                        'images': offer['Images'],
                        'created': offer['CreatedAt']
                    })

        except Exception as err:
            print("could not connect to collection due to ", err)
    return jsonify(output)

# route to add an offer
@app.route('/api/addOffer', methods=['POST', 'GET'])
@is_logged_in
def add_offer():
    form = DetailForm()
    if request.method == 'POST':
        file = request.files.get('file')
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
            'Images':  upload(file)
        }

        try:
            offers = db.offers
            print("connected successfully to collection")
        except Exception as err:
            print('could not connect to collection due to ', err)

        try:
            offers.insert_one(offer_item)
            flash("added offer successfully", 'success')
        except Exception as err:
            flash('could not add offer due to ' + str(err), 'danger')

        return redirect(url_for('show_offers'))

    return render_template('add_offers.html')

# route to delete an offer
@app.route('/delete/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def delete_offer(id):
    if request.method == 'GET':
        # connect to the database
        offers = db.offers

        # find item to delete
        offers.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('show_offers'))
        flash('item deleted', 'success')
    return render_template('offers.html')


# route to edit offer
@app.route('/editOffer/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def edit_offer(id):
    # connect to the database
    offers = db.offers

    # find one and update
    offers.find_one({'_id': ObjectId(id)})

    # get form
    form = DetailForm(request.form)
    data = request.form

    # populate article form fields
    form.title.data = offers['Title']
    form.overview.data = offers['Overview']
    form.itinerary.data = offers['Itinerary']
    form.inclusion.data = offers['Inclusion']
    form.price.data = offers['Price']
    form.addinfo.data = offers['AddInfo']

    if request.method == 'POST':
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

        # update the article
        offers.update_one(update=update_offer)

        flash('Offer has been updated', 'success')
        print('updated successfully')

        return redirect(url_for('show_offers'))
    return render_template('edit_offers.html', form=form)

# data from frontend
@app.route('/getData', methods=['POST'])
def get_data():
    output = []
    if request.method == 'POST':
        data = request.data
        print(data)

    return data
