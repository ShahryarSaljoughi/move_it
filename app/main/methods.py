__author__ = 'shahryar_slg'

import requests


def send_signup_code(phonenumber, code):
    params = {
        'user': "09127401672",
        'pass': "amin1672",
        'lineNo': "30004554551672",
        'to': str(phonenumber),
        'text': "your code is : {0} \n Respectfully, \n Shipment Team".format(str(code))
    }
    response = requests.post('http://ip.sms.ir/SendMessage.ashx', params=params)

    return response
