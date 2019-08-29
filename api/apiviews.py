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
        new_data = literal_eval(data.decode('utf-8'))
        try:
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
            # add email to db
            emails = mongo.emails
            emails.insert_one(email_object)

            body = """
                <div style="height: auto; background: #eeeeee; color:#000411; padding: 10px; border-radius: 3px; font-size: .9rem">
                   <p> Name :  %s  </p>
                   <p> Email :  %s  </p>
                   <p> Nationality :  %s  </p>
                   <p> Number :  %s  </p>
                   <p> Departure :  %s  </p>
                   <p> Adults :  %s  </p>
                   <p> Children :  %s  </p>
                   <p> Budget :  %s  </p>
                   <span> <h4> Additional Information </h4> <p> %s </p></span>
            """ % (new_data['Name'], new_data['Email'], new_data['Nationality'], new_data['Number'], new_data['Departure'], new_data['Adults'], new_data['Children'], new_data['Budget'], new_data['Info'])

            # # send mail to mail server
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.webfaction.com", port=port, context=context) as server:
                # connect to smtp server
                server.login(usr, pwd)
                msg = MIMEMultipart()
                msg['FROM'] = sender
                msg['TO'] = receiver
                msg['Subject'] = new_data['Package']
                body = body
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
