from flask_cors import CORS, cross_origin
import json
from common_functions import return_success,return_error,valid_email,read_credentials_from_file
from flask import Flask, request
from mongo_connection import *
app = Flask(__name__)
app.secret_key = "harshit25102000"
CORS(app, supports_credentials=True)
import datetime
import pytz
import threading

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
file_path = 'Credentials.txt'
EMAIL_ADDRESS, EMAIL_PASSWORD = read_credentials_from_file(file_path)
reCAPTCHA=0


@app.route("/submit_form",methods=["POST"])
def submit_form():
    try:
        data = request.get_json()
        print(data)
        f_name = data["firstName"]
        l_name=data["lastName"]
        email = data["email"]
        if not valid_email(email):
            return return_error(message="Invalid email")
        phone = data["phone"]
        subject=data["subject"]
        message = data["message"]

        #  reCAPTCHA Code
        code=data["code"]
        current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        # query={"name":name,"email":email,"message":message,"submitted_at":current_time}
        # response_db.insert_one(query)

        if not reCAPTCHA :
            return return_error(message="reCAPTCHA verfication failed", code=401)
        #sending mail----------------------------
        mail_subject = "You got a new Form Response"
        body = f"Form Data:\n\nFirst Name - {f_name}\n\nLast Name - {l_name}\n\nEmail - {email}\n\nPhone - {phone}\n\nSubject - {subject}\n\nMessage - {message}\n\nSubmitted At - {current_time}"


        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = 'harshitsingh25102000@gmail.com'
        msg["Subject"] = mail_subject

        msg.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())


        return return_success()
    except Exception as e:
            return return_error(message=str(e))






if __name__=="__main__":
    app.run(debug=True)
    app.config['DEBUG'] = True
    app.secret_key = "harshit25102000"
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)