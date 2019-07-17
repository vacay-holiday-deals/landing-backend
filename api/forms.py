# imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, StringField, PasswordField,  MultipleFileField
from wtforms.validators import DataRequired, length, regexp

# detail form class


class DetailForm(FlaskForm):
    file = MultipleFileField('Images', validators=[
                             regexp('\w+\.(jpg|jpeg|png)')])
    title = StringField('Title', validators=[
                        DataRequired, length(min=1, max=200)], )
    overview = TextAreaField('Overview', validators=[
                             DataRequired, length(min=100)])
    itinerary = TextAreaField('Itinerary', validators=[
                              DataRequired, length(min=100)])
    inclusion = TextAreaField('Inclusion', validators=[
                              DataRequired, length(min=100)])
    price = TextAreaField('Price', validators=[DataRequired, length(min=100)])
    addinfo = TextAreaField('Additional information',
                            validators=[DataRequired, length(min=100)])

# user registration form, only accessible to the admin


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[length(min=1, max=50)])
    username = StringField('username', validators=[length(min=4, max=25)])
    email = StringField('email', validators=[length(min=6, max=50)])
    password = PasswordField('password', validators=[DataRequired])
    role = StringField('role', validators=[DataRequired])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired])
