from flask import render_template, request, make_response, jsonify, g, session
from flask import abort
from flask_httpauth import HTTPBasicAuth
from random import randint
import methods
# from app import app
from app import db
from ..models import Freight, User, DestinationAddress, PickupAddress
from . import main
from .forms import SignupForm

auth = HTTPBasicAuth()




@main.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token':token.decode('ascii')})


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


# @main.route('/')

@main.route('/shipment/freights', methods=['DELETE'])
@auth.login_required
def delete_freight():
    freight_id = request.json['freight_id']
    freight = Freight.query.filter_by(id=freight_id).first()
    user = g.user
    if freight is None:
        return jsonify({"failure": "freight not found"})

    if user.id != freight.owner:
        return jsonify({"status": "failure",
                        "message": "you cannot delete freights ordered by others"}
                       )
    db.session.delete(freight)
    db.session.commit()
    return jsonify({"status": "success"})


@main.route('/shipment/freights', methods=['PUT'])
@auth.login_required
def update_freight():
    user = g.user

    if 'freight_id' not in request.json:
        return jsonify({
            'status': "failure",
            'message': "no freight id in request"
        })

    freight_id = request.json['freight_id']
    freight = Freight.query.filter_by(id=freight_id).first()

    if not freight:
        return jsonify({
            "status": "failure",
            "message": "freight not found"
        })
    if user.id != freight.owner:
        return jsonify({
            "status": "failure",
            "message": "you cannot edit freights ordered by others"}
            )

    new_data = request.json['new_data']
    keys = new_data.keys()
    for key in keys:
        exec("freight.{0} = new_data['{0}']".format(key))
        db.session.commit()
    return jsonify({
        "status": "success",
        "message": "fields "+" , ".join(keys) + " are updated"
    })


@main.route('/shipment/<string:username>/freights', methods=['GET'])
@auth.login_required
def get_user_freights(username):
    """
    this will return the freights made by user!
    :return: text/json
    """
    user_id = User.query.filter_by(username=username).first().id
    freights = Freight.query.filter_by(owner=user_id).all()
    freights_list = [fr.get_dict() for fr in freights]
    return jsonify({'freights': freights_list})


@main.route('/shipment/freights', methods=['GET'])
def get_freights():
    freights = Freight.query.all()
    freights_list = [fr.get_dict() for fr in freights]
    return jsonify({"freights": freights_list})


@main.route('/shipment/freights', methods=['POST'])
def create_freight():

    destination_dict = request.json['destination']
    destination = DestinationAddress(country=destination_dict['country'],
                                     city=destination_dict['city'],
                                     rest_of_address=destination_dict['rest_of_address'],
                                     postal_code=destination_dict['postal_code']
                                     )

    pickup_address_dict = request.json["pickup_address"]
    pickup_address = PickupAddress(country=pickup_address_dict['country'],
                                   city=pickup_address_dict['city'],
                                   rest_of_address=pickup_address_dict['rest_of_address'],
                                   postal_code=pickup_address_dict['postal_code']
                                   )

    freight = Freight(name=request.json['name'],
                      height=request.json['height'],
                      width=request.json['width'],
                      depth=request.json['depth'],
                      receiver_name=request.json['receiver_name'],
                      receiver_phonenumber=request.json['receiver_phonenumber'],
                      weight=request.json['weight'],
                      description=request.json['description']
                      )

    freight.destination.append(destination)
    freight.pickup_address.append(pickup_address)

    user = User.query.filter_by(username=request.json['username']).first()
    user.freights.append(freight)

    db.session.add(destination)
    db.session.add(pickup_address)
    db.session.add(freight)
    db.session.add(user)

    db.session.commit()

    return "%s" % str(freight)


@main.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        form = SignupForm()
        return render_template('signup.html', form=form)

    elif request.method == 'POST':
        if request.json:
            new_user = User(username=request.json['username'],
                            email=request.json['email'],
                            phonenumber=request.json['phonenumber'],
                            role_id=request.json['role_id'] if request.json['role_id'] in [1, 2] else 1,
                            )
            new_user.set_password(request.json['password'])

            code = randint(100000, 999999)
            session['inactive_account'] = {'user': new_user, 'code': code}
            response = methods.send_signup_code(new_user.phonenumber, code=code)

            if response.status_code == 200:
                return jsonify({
                    'status': "success",
                    'message': "a six-digit code in sent to your phone . enter the code to confirm the phone number"
                })
            else:
                return jsonify({
                    'status': "failure",
                    'message': "we got problems sending code: '{}' \n try again later".format(response.text)
                })

        else:
            abort(400)


@main.route('/confirm_phonenumber', methods=['POST'])
def confirm_phonenumber():

    if 'code' not in request.json:
        return jsonify({
            'status': "failure",
            'message': "the key ,'code', must be sent"
        })
    elif 'inactive_account' not in session:
        return jsonify({
            'status': "failure",
            'message': "no phone number is pending to be confirmed!"
        })
    elif session['inactive_account']['code'] != request.json['code']:
        return jsonify({
            'status': "failure",
            'message': "code does not match"
        })

    new_user = session['inactive_account']['user']
    db.session.add(new_user)
    db.session.commit()


# the below method is just for fun and can be deleted:
@main.route('/author')
def see_author():
    return render_template('aboutAuthor.html')


# the below method is just for fun and can be deleted:
@main.route('/')
def hello_world():
    return render_template('main_page.html')


@main.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


# if __name__ == '__main__':
#    app.run()
