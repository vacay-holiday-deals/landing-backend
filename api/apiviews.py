from flask import Blueprint, jsonify, flash, request
from .views import mongo
from .models import User
from ast import literal_eval
import ssl
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from bson import ObjectId

api = Blueprint('api', __name__)

# return all offers
@api.route('/api/getoffer', methods=['GET'])
def get_offers():
    try:
        if request.method == 'GET':

            try:
                offer = mongo.offers
                offers = offer.find()
                output = []
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
                return jsonify({"Message": "sould not connect to the database"}), 400
        return jsonify({'Message': 'method not allowed'}), 405
    except Exception as error:
        return jsonify({'Message': "something went wrong"}), 400


# data from frontend
@api.route('/api/uploadDetail', methods=['POST'])
def get_data():
    if request.method == 'POST':
        usr = os.getenv('USR')
        pwd = os.getenv('PASSWORD')
        sender = os.getenv('SENDER')
        receiver = os.getenv('RECEIVER')
        port = 465

        data = request.data
        new_data = literal_eval(data.decode('utf-8'))

        body = 'Name: ' + new_data['Name'] + '\n' + 'Email: ' + new_data['Email'] + '\n' + ' Nationality: ' + new_data['Nationality'] + '\n' + ' Number: ' + new_data['Number'] + '\n' + ' Departure: ' + \
            new_data['Departure'] + '\n' + ' Adults: ' + new_data['Adults'] + '\n' + ' Children: ' + \
            new_data['Children'] + '\n' + \
            ' Additional information: ' + new_data['Info']

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.webfaction.com", port=port, context=context) as server:
            try:
                # connect to smtp server
                server.login(usr, pwd)
                msg = MIMEMultipart()
                msg['FROM'] = sender
                msg['TO'] = receiver
                msg['Subject'] = new_data['Package']
                body = body
                msg.attach(MIMEText(body, 'plain'))
                text = msg.as_string()
                server.sendmail(sender, receiver, text)

                # email object
                email_object = {
                    'Name': new_data['Name'],
                    'Email': new_data['Email'],
                    'Nationality': new_data['Nationality'],
                    'Package': new_data['Package'],
                    'Depature': new_data['Departure'],
                    'Adult': new_data['Adults'],
                    'Children': new_data['Children'],
                    'Bugdet': new_data['Budget'],
                    'Addinfo': new_data['Info'],
                    'CreadetAt': datetime.datetime.now()
                }

                # connect to database
                emails = mongo.emails
                emails.insert_one(email_object)
                return jsonify({'Message': 'Thank you,information sent'}), 200
            except Exception as error:
                return jsonify({'Message': 'we encountered an error'}), 400

    return jsonify({'Message': 'you encountered a problem'}), 400


# get offer by name
# endpoint to get article by id
@api.route('/api/getoffer/<title>', methods=["GET"])
def get_offer(title):
    offers = mongo.offers
    try:
        offer = offers.find_one(filter={"Title": title})
        if offer:
            output = {
                # 'id': offer['_id'],
                'title': offer['Title'],
                'overview': offer['Overview'],
                'itinerary': offer['Itinerary'],
                'inclusion': offer['Inclusion'],
                'price': offer['Price'],
                'addinfo': offer['AddInfo'],
                'images': offer['Images'],
                'created': offer['CreatedAt']
            }

        else:
            return jsonify({"message": "could not get offer"})
    except Exception as e:
        return jsonify({"Message": "something went wrong"}), 400
    return output


@api.route('/api/getusers', methods=['GET'])
def get_users():
    users = User.query.all()
    output = []
    for user in users:

        output.append({
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "password": str(user.password),
            "role": user.role
        })
        return jsonify({"Output": output})
    return users
