from flask import Blueprint, jsonify, flash, request
from .views import mongo
from .models import User
import ssl
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from bson import ObjectId, objectid
from .data import Data

api = Blueprint('api', __name__)

# return all offers
@api.route('/api/getoffer', methods=['GET'])
def get_offers():
    if request.method == 'GET':
        try:
            # connect to db
            offers = mongo.offers
            # find all overs
            my_offers = list(offers.find({}))
            output = []
            for offer in my_offers:
                if not offer:
                    return jsonify({'message': 'no offers were found'}), 400

                output.append({
                    'id': str(offer['_id']),
                    'title': offer['Title'],
                    'overview': offer['Overview'],
                    'itinerary': offer['Itinerary'],
                    'inclusion': offer['Inclusion'],
                    'price': offer['Price'],
                    'addinfo': offer['AddInfo'],
                    'images': offer['Images'],
                    'destination': offer['Destination'],
                    'created': offer['CreatedAt']
                })
            return jsonify(output), 200
        except Exception as error:
            print(error)
            return jsonify({'message': error}), 400
    return jsonify({'message': 'method not allowed'}), 405

# data from frontend
@api.route('/api/uploadDetail', methods=['POST'])
def get_data():
    if request.method == 'POST':
        usr = os.getenv('USR')
        pwd = os.getenv('PASSWORD')
        sender = os.getenv('SENDER')
        receiver = os.getenv('RECEIVER')
        port = 465

        data = request.json
        try:
            # email object
            email_object = {
                'Name': data['Name'],
                'Email': data['Email'],
                'Nationality': data['Nationality'],
                'Number': data['Number'],
                'Package': data['Package'],
                'Departure': data['Departure'],
                'Destination': data['Destination'],
                'Adult': data['Adults'],
                'Children': data['Children'],
                'Budget': data['Budget'],
                'Addinfo': data['Info'],
                'CreatedAt': datetime.datetime.now()
            }
            # add email to db
            emails = mongo.emails
            emails.insert_one(email_object)

            email_body = Data.body(email_object)

            # # send mail to mail server
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.webfaction.com", port=port, context=context) as server:
                # connect to smtp server
                server.login(usr, pwd)
                msg = MIMEMultipart()
                msg['FROM'] = sender
                msg['TO'] = receiver
                msg['Subject'] = data['Package']
                body = email_body
                msg.attach(MIMEText(body, 'html'))
                text = msg.as_string()
                server.sendmail(sender, receiver, text)

            return jsonify({'Message': 'Your inquiry has been sent'}), 200
        except Exception as error:
            print(error)
            return jsonify({'Message': 'Something went wrong please try again'}), 400
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
                'id': str(offer['_id']),
                'title': offer['Title'],
                'overview': offer['Overview'],
                'itinerary': offer['Itinerary'],
                'inclusion': offer['Inclusion'],
                'price': offer['Price'],
                'addinfo': offer['AddInfo'],
                'images': offer['Images'],
                'destination': offer['Destination'],
                'created': offer['CreatedAt']
            }
            return jsonify(output), 200
        else:
            return jsonify({"Message": "could not get offer"}), 400
    except Exception as error:
        print(error)
        return jsonify({"Message": "something went wrong"}), 400
