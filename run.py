from api import create_app

app = create_app()

app.run(port=5000 or 80)
