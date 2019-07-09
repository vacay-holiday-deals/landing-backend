## Backend vacay offers - python flask app

In the project directory run;

### pipenv shell 

 This creates a virtual environment for the python flask app
 You don't require a requirements file if you are using [Pipenv](https://docs.pipenv.org/en/latest/) for your dev environment

 ### pip install -r requirements.txt

 This command is for those using other environments such as [virtualenv](https://virtualenv.pypa.io/en/latest/) and the requirements.txt file is provided

## export FLASK_APP=api

In your terminal where you have opened the app and the environment, run the command above to tell flask where the app is located

## export FLASK_DEBUG=1

Still in your terminal run the command to set debug mode to true

## flask run

This command will run you application in debug mode.
