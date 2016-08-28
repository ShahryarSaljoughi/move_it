

from flask import render_template, request, make_response, jsonify
from flask import abort

# from app import app
from app import db

from ..models import Freight, User, DestinationAddress, PickupAddress
from . import main
from .forms import SignupForm



@main.route('/shipment/<string:username>/freights', methods=['GET'])
def get_freights(username):
    """
    this will return the freights made by user!
    :return: text/json
    """
    user_id = User.query.filter_by(username=username).first().id
    freights = Freight.query.filter_by(owner=user_id).all()
    return jsonify({'freights': freights})


@main.route('/shipment/<string:username>/freights', methods=['POST'])
def create_freight(username):

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
                      weight=request.json['weight']
                      )

    freight.destination.append[destination]
    freight.pickup_address.append[pickup_address]

    user = Freight.query.filter_by(username=username).first()
    user.freights.append(freight)

    db.session.add(destination)
    db.session.add(pickup_address)
    db.session.add(freight)
    db.session.add(user)

    db.session.commit()


@main.route('/signup', methods=['POST', 'GET'])
def sign_up():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)

    elif request.method == 'POST':
        print "request is post"

        if request.json:
            new_user = models.User(username=request.json['username'],
                                   email=request.json['email'],
                                   phonenumber=request.json['phonenumber'],
                                   role_id=request.json['role_id'] if request.json['role_id'] in [1, 2] else 1,
                                   password=request.json['password']
                                   )
            db.session.add(new_user)
            db.session.commit()
            return "success :) %r created" % new_user
        else:
            print "is about to return 400"
            abort(400)


@main.route('/author')
def see_author():
    return render_template('aboutAuthor.html')


@main.route('/')
def hello_world():
    return 'main_page'


@main.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


# if __name__ == '__main__':
#    app.run()
