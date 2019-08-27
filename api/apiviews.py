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
from bson import ObjectId, objectid

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
                            'id': str(offer['_id']),
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
            except Exception as error:
                print(error)
                return jsonify({"Message": "could not connect to the database"}), 400
        return jsonify({'Message': 'method not allowed'}), 405
    except Exception as error:
        print(error)
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
        print(data)
        new_data = literal_eval(data.decode('utf-8'))

        body = 'Name: ' + new_data['Name'] + '\n' + 'Email: ' + new_data['Email'] + '\n' + ' Nationality: ' + new_data['Nationality'] + '\n' + ' Number: ' + new_data['Number'] + '\n' + ' Departure: ' + \
            new_data['Departure'] + '\n' + ' Adults: ' + new_data['Adults'] + '\n' + ' Children: ' + \
            new_data['Children'] + '\n' + 'Budget : ' + new_data['Budget'] + '\n' \
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
                    'Number': new_data['Number'],
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
                # ** Todo: create a backup email database **
                return jsonify({'Message': 'Your inquiry has been sent'}), 200
            except Exception as error:
                print(error)
                return jsonify({'Message': 'something went wrong, please try again!!'}), 400

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
            return jsonify({"message": "could not get offer"}), 404
    except Exception as error:
        print(error)
        return jsonify({"Message": "something went wrong"}), 400
    return output, 200


# endpoint to record number of clicks
@api.route('/api/recordclicks', methods=['POST', 'GET'])
def recordclicks():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        clicks = mongo.clicks
        # clicks.insert_one(data)
        print(data + "has been recorded")
    return 'no data received'
