__author__ = 'shahryar_saljoughi'

from . import auth
from app.main import main
from flask import jsonify, g, session, request, abort
from random import randint
from app.models import User
from app import db
import methods


@main.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
    # I don't know what decode really does ! it makes no difference as I tested !

@auth.verify_password
def verify_password(username_or_token, password):
    # if token is passed , next line will assign the user
    user = User.verify_auth_token(username_or_token)
    if not user:
        # if username is passed , next line will assign the user
        user = User.get_user(username=username_or_token)
        if not user:
            # if email is passed , next line will assign the user
            user = User.get_user(email=username_or_token)
            if not user:
                # if user_id is passed , next line will assign the user
                user = User.get_user(user_id=username_or_token)
                if not user:
                    return False
        if not user.verify_password(password):
            return False
    g.user = user
    return True

# REGISTRATION:
@main.route('/signup/using_phonenumber', methods=['POST'])
def signup_using_phonenumber():
    if not request.json:
        return jsonify({
            'status': 'failure',
            'message': "no json received"
        }), 400

    new_user = User(username=request.json['username'],
                    phonenumber=request.json['phonenumber'],
                    role_id=request.json['role_id'] if request.json['role_id'] in [1, 2] else 1,
                    first_name=request.json['first_name'],
                    last_name=request.json['last_name']
                    )
    new_user.set_password(request.json['password'])
    new_user.phonenumber_confirmed = False

    code = randint(100000, 999999)  # six digits
    response = methods.send_signup_code(phonenumber=request.json['phonenumber'], code=code)

    session['inactive_account_phone'] = \
        {
            'user':
                {
                    'data': new_user.get_dict(),  # email, phone , role_id, username
                    'password': request.json['password']
                },
            'code': code
        }

    if response.status_code == 200:
        return jsonify({
            'status': "success",
            'message': "a six-digit code is sent to your phone . enter the code within the next 10 mins"
                       " to confirm the phone number"
                       " and complete your registration"
        })
    else:
        return jsonify({
            'status': "failure",
            'message': "we got problems sending code: '{}' \n"
                       " try confirming your phone number later".format(response.text)
        })

@main.route('/confirm_phonenumber', methods=['POST'])
def confirm_phonenumber():

    if 'code' not in request.json:
        return jsonify({
            'status': "failure",
            'message': "the key ,'code', must be sent"
        })
    elif 'inactive_account_phone' not in session:
        return jsonify({
            'status': "failure",
            'message': "no phone number is pending to be confirmed!"
        })
    elif session['inactive_account_phone']['code'] != request.json['code']:
        return jsonify({
            'status': "failure",
            'message': "code does not match"
        })

    new_user = User(username=session['inactive_account_phone']['user']['data']['username'],
                    phonenumber=session['inactive_account_phone']['user']['data']['phonenumber'],
                    role_id=session['inactive_account_phone']['user']['data']['role_id'],
                    first_name=session['inactive_account_phone']['user']['data']['first_name'],
                    last_name=session['inactive_account_phone']['user']['data']['last_name']
                    )
    new_user.set_password(session['inactive_account_phone']['user']['password'])
    new_user.phonenumber_confirmed = True
    db.session.add(new_user)
    db.session.commit()

    session.pop('inactive_account_phone')

    return jsonify({
        'status': "success",
        'message': "{} was successfully signed up".format(new_user)
    })

@main.route('/signup/using_email', methods=['POST'])
def signup_using_email():
    new_user = User(username=request.json['username'],
                    email=request.json['email'],
                    role_id=request.json['role_id'] if request.json['role_id'] in [1, 2] else 1,
                    first_name=request.json['first_name'],
                    last_name=request.json['last_name']
                    )
    new_user.set_password(request.json['password'])
    new_user.email_confirmed = False
    db.session.add(new_user)
    db.session.commit()
    methods.send_confirmation_email(email=new_user.email,
                                    name=new_user.username,
                                    token=new_user.generate_email_confirmation_token()
                                    )
    return jsonify({
        'status': 'success',
        'message': "an email containing an activation link is sent to your email address ."
                   " make sure to confirm your email within the next 24 hours"
    })

@main.route('/email_confirmation/<string:token>')
def confirm_email(token):
    user = User.confirm_email_token(token)
    if user is None:
        print "user is None"
        abort(400)
    if user == "expired":
        return jsonify({
            'status': "failure",
            'message': "token is expired"
        })
    else:
        user.email_confirmed = True
        user.isActive = True
        db.session.commit()
        return jsonify({'status': 'success', 'message': "your email is successfully confirmed"})
