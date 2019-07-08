from . import login_manager
from .models import User
from flask_pymongo import MongoClient
import os
from dotenv import load_dotenv
from flask import request, redirect, url_for, flash
import cloudinary
from cloudinary import uploader


load_dotenv(verbose=True)

# functions to do things

# upload to cloudinary


def upload(file):
    if request.method == 'POST':
        urls = []
        res = cloudinary.uploader.upload(file, folder='Projects/vacay')
        result = res['secure_url']
    return result


# getting a user id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    flash('login to access page')
    return redirect(url_for('api.login'))


# add offer to mongodb
def push_offer(offer):
    try:
        insert

    except Exception as error:
        return jsonify({'msg': str(error)})
