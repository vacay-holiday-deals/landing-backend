# make script excecutable with chmod a+rx my-script.sh

export FLASK_APP=api
export FLASK_ENV=development
flask run --port=5001 --host=0.0.0.0
