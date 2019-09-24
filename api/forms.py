# imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, length, regexp, InputRequired, Email
from wtforms.fields.html5 import EmailField
from flask_ckeditor import CKEditorField

# detail form class


class DetailForm(FlaskForm):
    file = MultipleFileField('Images', validators=[
                             regexp('\w+\.(jpg|jpeg|png)')])
    title = StringField('Title', validators=[
                        DataRequired, length(min=1, max=200)], )
    destination = StringField('Destination', validators=[
        DataRequired, length(min=1, max=200)], )
    overview = CKEditorField('Overview', validators=[
                             DataRequired, length(min=100)])
    itinerary = CKEditorField('Itinerary', validators=[
                              DataRequired, length(min=100)])
    inclusion = CKEditorField('Inclusion', validators=[
                              DataRequired, length(min=100)])
    price = CKEditorField('Price', validators=[DataRequired, length(min=100)])
    addinfo = CKEditorField('Additional information',
                            validators=[DataRequired, length(min=100)])

# user registration form, only accessible to the admin


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[length(
        min=1, max=50), InputRequired('Name is required')])
    username = StringField('username', validators=[length(
        min=4, max=25), InputRequired('Username is required')])
    email = EmailField('email', validators=[length(min=6, max=50), InputRequired(
        'Email is required'), Email('Please enter a valid email')])
    password = PasswordField('password', validators=[
                             InputRequired('Password is required')])
    role = SelectField('role', choices=[('admin', 'admin'), ('user', 'user')], validators=[
                       InputRequired('Role is required')])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired])
