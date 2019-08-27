from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy  # remove
import os
import datetime
from flask_cors import CORS
from dotenv import load_dotenv
from flask_assets import Environment, Bundle
import cloudinary
from flask_login import LoginManager
from flask_fontawesome import FontAwesome
from flask_ckeditor import CKEditor
from flask_mongoengine import MongoEngine
from flask_pymongo import MongoClient


# load environmental variables
load_dotenv(verbose=True)

mongo_uri = os.getenv('MONGO_URI')

#db = SQLAlchemy()
cors = CORS()
login_manager = LoginManager()
assets = Environment()
fa = FontAwesome()
ckeditor = CKEditor()
db = MongoEngine()

css = Bundle('css/root.css', 'css/layouts.css', 'css/navbar.css',
             'css/index.css', 'css/login.css', 'css/offers.css', 'css/404.css', 'css/register.css', 'css/edit_offers.css', 'css/add_offers.css', output='gen/main.css')
js = Bundle('js/app.js', output='gen/main.js')


# create the app function
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=1)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'offers',
        'host': mongo_uri or None,
        'connect': False
    }

    # create a secret key
    SECRET_KEY = os.urandom(64)
    app.config['SECRET_KEY'] = SECRET_KEY

    # initialise the database
    db.init_app(app)

    # initialise app with flask login manager
    login_manager.init_app(app)

    # set session security to strong
    login_manager.session_protection = "strong"

    # prevents crossite scripting
    cors.init_app(app)

    ckeditor.init_app(app)

    # initialise all css js assets
    assets.init_app(app)

    # load the static files
    assets.register('css_all', css)
    assets.register('js_all', js)

    # fontawesome configuration
    fa.init_app(app)

    # cloudinary configuration
    cloudinary.config(
        cloud_name=os.getenv('CLOUD_NAME'),
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET')
    )

    # import blueprint from views
    from .views import main
    from .apiviews import api
    from .controllers import page_not_found

    app.register_error_handler(404, page_not_found)
    app.register_blueprint(main)
    app.register_blueprint(api)

    return app
