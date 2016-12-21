
from flask import request, g, jsonify, abort, json
import os
from werkzeug.utils import secure_filename

from app.models import Freight, User, DestinationAddress, PickupAddress, FreightPicture
from . import auth
from app.main import main
from app import db
from app import app

__author__ = 'shahryar_saljoughi'


# CRUD OPERATIONS
@main.route('/freights', methods=['DELETE'])
@auth.login_required
def delete_freight():
    # if g.user is None:
    #     abort(401)
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


@main.route('/freights', methods=['PUT'])
@auth.login_required
def update_freight():
    user = g.user

    # ####### is request  healthy? #########################################################
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
    # #####################################################################################

    new_data = request.json['new_data']
    keys = new_data.keys()

    # ###### core of updating data : ######################################################
    for key in keys:
        if key != "destination" and key != "pickup_address":
            exec("freight.{0} = new_data['{0}']".format(key))
        elif key in ["destination", "pickup_address"]:  # key is either destination or pickup_address
            for field in request.json['new_data'][key]:
                exec("freight.{0}[0].{1} = new_data['{0}']['{1}']".format(key, field))
        db.session.commit()

    return jsonify({
        "status": "success",
        "message": "fields "+" , ".join(keys) + " are updated"
    })


@main.route('/<string:username>/freights', methods=['GET'])
@auth.login_required
def get_user_freights(username):
    """
    this will return the freights made by user!
    :return: text/json
    """
    user_id = User.query.filter_by(username=username).first().id
    freights = Freight.query.filter_by(owner=user_id).all()
    # freights_list = [fr.get_dict() for fr in freights]
    freights_list = [fr for fr in freights]
    return jsonify({'freights': freights_list})


@main.route('/freights', methods=['GET'])
@auth.login_required
def get_freights():
    freights = Freight.query.all()
    freights_list = [fr for fr in freights]

    # I want the result to be in dictionary form!
    result_str = json.dumps({'freights': freights_list})
    result_dict = json.loads(result_str)

    # let's show fewer information if the client is not logged in:
    if g.user is None:
        for freight in result_dict['freights']:
            freight.pop('receiver_name')
            freight.pop('price')

    return jsonify(result_dict)


@main.route('/freights', methods=['POST'])
@auth.login_required
def create_freight():

    # if g.user is None:
    #     abort(401)
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
                      description=request.json['description'],
                      price=request.json['price']
                      )

    freight.destination.append(destination)
    freight.pickup_address.append(pickup_address)

    # user = User.query.filter_by(username=request.json['username']).first()
    user = g.user
    user.freights.append(freight)

    db.session.add(destination)
    db.session.add(pickup_address)
    db.session.add(freight)
    db.session.add(user)

    db.session.commit()

    return jsonify({
        'status': "success",
        'message': " freight created",
        'freight_info': freight})


def allowed_picture(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_PICTURE_EXTENSIONS']


@main.route('/upload/freight/picture', methods=['POST'])
@auth.login_required
def upload_freight_picture():

    # if g.user is None:
    #     abort(401)
    freight = Freight.query.filter_by(id=request.form['freight_id']).first()

    if freight is None:
        return jsonify({'status': 'failure', 'message': 'there is no freight with that id!'})

    if freight.owner != g.user.id:
        return jsonify({'status': 'failure', 'message': 'you can not append picture to this freight'})

    if 'file' not in request.files:
        return jsonify({"status": "failure", "message": "no file part!"})

    pic_file = request.files['file']

    if pic_file.filename == '':
        return jsonify({'status': 'failure', 'message': 'no file selected!'})

    if pic_file and allowed_picture(pic_file.filename):
        filename = secure_filename(pic_file.filename)
        pic_path = os.path.join(app.config['FREIGHT_PICTURES_DIR'], filename)
        pic_file.save(pic_path)
        picture = FreightPicture(filename=filename,
                                 path=pic_path,
                                 )
        freight.pictures.append(picture)
        db.session.add(picture)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'done'})

    return jsonify({'status': 'failure', 'message': 'file is not allowed'})
