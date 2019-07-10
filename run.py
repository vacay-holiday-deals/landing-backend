from api import create_app

# initialise the create_app() with a variable
app = create_app()

if __name__ == '__main__':
    # use the variable to run the app
    app.run(port=5000 or 80)
