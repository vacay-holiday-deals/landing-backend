# python imports

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import cloudinary
from flask_assets import Environment, Bundle
import os

# initialise flask app
app = Flask(__name__)

# other imports { needed after app initialisation }
from views import *

# initialise the app with CORS for cross origin scripting
CORS(app)

# initialise assets to app
assets = Environment(app)

# load env variables from the .env file
load_dotenv(verbose=True)

# Cloudinary configurations
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET')
)

# secret key
SECRET_KEY = os.urandom(64)

# update the app config
app.config.update(
    SECRET_KEY=SECRET_KEY,
    PERMANENT_SESSION_LIFETIME=30,
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=10,
    DROPZONE_MAX_FILES=10,
)

# load the static files
css = Bundle('css/root.css', 'css/layouts.css', 'css/navbar.css',
             'css/index.css', 'css/login.css', 'css/offers.css', 'css/edit_offers.css', 'css/add_offers.css', output='gen/main.css')

assets.register('css_all', css)

# run the app
if __name__ == '__main__':
    # run app in debug for dev and remove debug for prod
    app.run(debug=True)
