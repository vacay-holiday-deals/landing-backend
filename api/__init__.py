from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from flask_talisman import Talisman
from dotenv import load_dotenv
from flask_assets import Environment, Bundle
import cloudinary
from flask_login import LoginManager
from itsdangerous import URLSafeSerializer
from flask_fontawesome import FontAwesome
from flask_ckeditor import CKEditor


db = SQLAlchemy()
cors = CORS()
login_manager = LoginManager()
assets = Environment()
fa = FontAwesome()
ckeditor = CKEditor()


css = Bundle('css/root.css', 'css/layouts.css', 'css/navbar.css',
             'css/index.css', 'css/login.css', 'css/offers.css', 'css/edit_offers.css', 'css/add_offers.css', output='gen/main.css')
js = Bundle('js/app.js', output='gen/main.js')


# create the app function
def create_app():
    app = Flask(__name__)

    # prevents crossite scripting
    cors.init_app(app)

    ckeditor.init_app(app)

    # initialise all css js assets
    assets.init_app(app)

    # load the static files
    assets.register('css_all', css)
    assets.register('js_all', js)

    # load environmental variables
    load_dotenv(verbose=True)

    # fontawesome configuration
    fa.init_app(app)

    # app config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialise the database
    db.init_app(app)

    # create a secret key
    SECRET_KEY = os.urandom(64)
    app.config['SECRET_KEY'] = SECRET_KEY
    serial = URLSafeSerializer(app.secret_key)

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

    # initialise app with flask login manager
    login_manager.init_app(app)

    # import blueprint from views
    from .views import main
    from .apiviews import api

    app.register_blueprint(main)
    app.register_blueprint(api)

    return app
