# imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, StringField, PasswordField
from wtforms.validators import DataRequired, length

# detail form class


class DetailForm(FlaskForm):
    title = TextAreaField('title', validators=[DataRequired])
    overview = TextAreaField('overview', validators=[DataRequired])
    itinerary = TextAreaField('itinerary', validators=[DataRequired])
    inclusion = TextAreaField('inclusion', validators=[DataRequired])
    price = TextAreaField('price', validators=[DataRequired])
    addinfo = TextAreaField('additional information',
                            validators=[DataRequired])


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
