from . import login_manager
from .models import User
from flask_pymongo import MongoClient
import os
from dotenv import load_dotenv
from flask import request, redirect, url_for, flash
import cloudinary
from cloudinary import uploader


# load env variables
load_dotenv(verbose=True)

# functions to do things
# upload file to cloudinary


def upload(file):
    folder = os.getenv('CLOUD_FOLDER')
    res = cloudinary.uploader.upload(file, folder=folder)
    result = res['secure_url']
    return result


# getting a user id
# @login_manager.user_loader
# def load_user(user_id):
   # return User.query.get(int(user_id))


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

# handle unauthorised visits
@login_manager.unauthorized_handler
def unauthorized():
    flash('login to access page')
    return redirect(url_for('main.login'))
