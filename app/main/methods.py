__author__ = 'shahryar_slg'

import requests


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

# just to test if the snippet works:
if __name__ == '__main__':
    send_signup_code("09127401672", code=123456)
