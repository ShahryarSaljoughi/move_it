
import requests
from flask_mail import Mail, Message
from app import app
from app.main.appExceptions import MailingError
__author__ = 'shahryar_slg'


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
    # print response.text  # this single line is a BUG do you believe it ???
    #                        since the response.text can't be decoded on my vps
    return response


def send_confirmation_email(email, name, token):
    """
    may raise MailingError
    """
    msg = Message(subject='SHIPMENT-confirm your email',
                  recipients=[email])
    # url = 'http://localhost:5000/email_confirmation/'+str(token)
    url = 'http://136.243.203.173:9000/email_confirmation/'+str(token)
    msg.body = "{}".format(url)
    try:
        mail.send(msg)
    except:
        raise MailingError(message="some thing went wrong while sending you confirmation mail . Try again later")

# just to test if the snippet works:
if __name__ == '__main__':
    send_signup_code("09127401672", code=123456)
