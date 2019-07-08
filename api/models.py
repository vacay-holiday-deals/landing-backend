from . import db
from flask_login import UserMixin
from datetime import datetime


# users db model


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(50))
    role = db.Column(db.String(50))
    password = db.Column(db.String(50))
