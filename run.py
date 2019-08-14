from api import create_app
from dotenv import load_dotenv
import os

# load env variables
load_dotenv(verbose=True)

env_host = os.getenv('HOST')

# initialise the create_app() with a variable
app = create_app()

if __name__ == '__main__':
    # use the variable to run the app
    if app.env == 'development':
        port = '5000'
        app.run(port=port)
    else:
        app.run(host=env_host)
