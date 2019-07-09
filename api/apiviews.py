from flask import Blueprint, jsonify, flash, request
from .views import mongo
from .models import User

api = Blueprint('api', __name__)

# return all offers
@api.route('/api/getoffer', methods=['GET'])
def get_offers():
    if request.method == 'GET':
        output = []
        try:
            offer = mongo.offers
            print("successfully connected to collection")

            offers = offer.find()
            for offer in offers:
                if offer:
                    output.append({
                        # 'id': offer['_id'],
                        'title': offer['Title'],
                        'overview': offer['Overview'],
                        'itinerary': offer['Itinerary'],
                        'inclusion': offer['Inclusion'],
                        'price': offer['Price'],
                        'addinfo': offer['AddInfo'],
                        'images': offer['Images'],
                        'created': offer['CreatedAt']
                    })

            return jsonify(output)
        except Exception as err:
            print("could not connect to collection due to ", err)
    return jsonify({'msg': 'method not allowed'}), 405


# return all users
# get all users route
@api.route('/api/getusers', methods=['GET'])
def get_users():
    if request.method == 'GET':
        # get all the users
        output = []
        users = User.query.all()

        for usr in users:
            output.append({
                'username': usr.username,
                'password': usr.password.decode('utf-8'),
                'email': usr.email,
                'name': usr.name
            })
        return jsonify({'Output': output})
    return jsonify({'msg': 'method not allowed'}), 405
