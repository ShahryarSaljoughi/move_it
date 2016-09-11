__author__ = 'shahryar_slg'

import requests
from flask_mail import Mail, Message
from app import app

mail = Mail(app)


def send_signup_code(phonenumber, code):
    params = {
        'user': "09127401672",
        'pass': "amin1672",
        'lineNo': "30004554551672",
        'to': phonenumber,
        'text': "your sign up code is : {0} \n\n Respectfully, \n Shipment Team".format(str(code))
    }
    print params
    response = requests.post(url='http://ip.sms.ir/SendMessage.ashx', params=params)
    print response.text
    return response


def send_confirmation_email(email, name, token):
    msg = Message(subject='SHIPMENT-confirm your email',
                  recipients=[email])
    # url = 'http://localhost:5000/email_confirmation/'+str(token)
    url = 'http://192.99.103.124:9000/email_confirmation/'+str(token)
    msg.body = "{}".format(url)
    mail.send(msg)


# just to test if the snippet works:
if __name__ == '__main__':
    send_signup_code("09127401672", code=123456)
