from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from flask_talisman import Talisman
from dotenv import load_dotenv
from flask_assets import Environment, Bundle
import cloudinary
from flask_login import LoginManager
from flask_dropzone import Dropzone


db = SQLAlchemy()
cors = CORS()
login_manager = LoginManager()
dropzone = Dropzone()
assets = Environment()


css = Bundle('css/root.css', 'css/layouts.css', 'css/navbar.css',
             'css/index.css', 'css/login.css', 'css/offers.css', 'css/edit_offers.css', 'css/add_offers.css', output='gen/main.css')


# define the app


def create_app():
    app = Flask(__name__)

    # prevents crossite scripting
    cors.init_app(app)

    # prevents crossite scripting and sql injection

    # initialise all css js assets
    assets.init_app(app)

    # load the static files
    assets.register('css_all', css)

    # load environmental variables
    load_dotenv(verbose=True)

    # app config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DB_URI')

    # initialise the database
    db.init_app(app)

    # create a secret key
    SECRET_KEY = os.urandom(64)
    app.config['SECRET_KEY'] = SECRET_KEY

    # update the app config
    app.config.update(
        PERMANENT_SESSION_LIFETIME=30,
        DROPZONE_ALLOWED_FILE_TYPE='image',
        DROPZONE_MAX_FILE_SIZE=10,
        DROPZONE_MAX_FILES=10,
    )

    # cloudinary configuration
    cloudinary.config(
        cloud_name=os.getenv('CLOUD_NAME'),
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET')
    )

    # initialise dropzone
    dropzone.init_app(app)

    # initialise app with flask login manager
    login_manager.init_app(app)

    # import blueprint from views
    from .views import api

    app.register_blueprint(api)

    return app
