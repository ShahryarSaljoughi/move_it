from flask import g, request, jsonify
from app import db
from app.main import main
from app.main.views import auth
from app.models import Tender, Freight
__author__ = 'shahryar_saljoughi'


@main.route('/apply_freight')
@auth.login_required
def apply_freight():
    """
    this view function makes an apply for a freight !
    """
    needed_keys = ['freight_id', 'price']
    for key in needed_keys:
        if key not in request.json.keys():
            return jsonify('bad request, this key is not received: {}'.format(key)), 400

    freight_id = request.json['freight_id']
    price = request.json['price']

    #  check type accuracy:
    if not (isinstance(freight_id, int) or isinstance(freight_id, long)) or not isinstance(price, float):
        return jsonify('bad request, type error'), 400

    if 'description' in request.json.keys():
        description = request.json['description']
    else:
        description = ''

    tender = Tender(courier=g.user,
                    freight=Freight.query.get(freight_id),
                    price=price,
                    description=description)

    db.session.add(tender)
    db.session.commit()
