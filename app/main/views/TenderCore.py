from flask import g, request, jsonify
from app import db
from app.main import main
from app.main.views import auth
from app.models import Tender, Freight
__author__ = 'shahryar_saljoughi'

#  CORE  ***************************************************************************************************************

@main.route('/apply_freight', methods=['POST'])
@auth.login_required
def apply_freight():
    """
    this view function makes an apply for a freight !
    """
    if g.user.role.title != 'courier':
        return jsonify('only couriers can apply for freights(you are not logged in as a courier!)'), 400

    needed_keys = ['freight_id', 'price']
    for key in needed_keys:
        if key not in request.json.keys():
            return jsonify('bad request, this key is not received: {}'.format(key)), 400

    #  ##############

    freight_id = request.json['freight_id']
    price = request.json['price']

    #  check type accuracy:
    if not (isinstance(freight_id, int) or isinstance(freight_id, long)) or not isinstance(price, float):
        return jsonify('bad request, type error'), 400

    # check if freight_id is valid:
    freight = Freight.query.get(freight_id)
    if freight is None:
        return jsonify('bad request, freight id does not exist'), 400

    # check if the freight is taken by another courier:
    if freight.is_courier_chosen:
        return jsonify('this freight is assigned to another courier.')

    if 'description' in request.json.keys():
        description = request.json['description']
    else:
        description = ''

    tender = Tender(courier=g.user,
                    freight=freight,
                    price=price,
                    description=description)

    db.session.add(tender)
    db.session.commit()

    return jsonify('successful'), 200


@main.route('/approve_courier', methods=['POST'])
@auth.login_required
def approve_courier():

    tender_id = request.json['tender_id']
    # check tender_id is valid:
    if not (isinstance(tender_id, int) or isinstance(tender_id, long)):
        return jsonify('bad request, tender id should be numeric and integer!'), 400
    tender = Tender.query.get(tender_id)
    if tender is None:
        return jsonify('bad request, tender id does not exist!'), 400
    # check if this is the creator of the freight who is approving a courier for his/her freight:
    if tender.freight.owner != g.user:
        return jsonify('access denied! only the owner of the freight can choose who ships the freight!')

    tender.approved = True
    tender.freight.is_courier_chosen = True
    db.session.commit()
    return jsonify('successful'), 200


@main.route('/freight_delivered', methods=['POST'])
@auth.login_required
def freight_received():
    # check tender_id is valid
    if 'tender_id' not in request.json or \
            not (isinstance(request.json['tender_id'], int)
                 or isinstance(request.json['tender_id'], long)):
        return jsonify('bad request'), 400
    tender = Tender.query.get(request.json['tender_id'])

    if tender.freight.owner != g.user:
        return jsonify('access denied! only the owner of the '
                       'freight can approve that freight is delivered!'), 400

    tender.freight.is_delivered = True
    db.session.commit()

    return jsonify('successful'), 200
# END OF CORE **********************************************************************************************************


@auth.login_required
@main.route('/freight_tenders', methods=['POST'])
def show_tenders():
    """
    give the freight_id and see the couriers who have applied for this freight and what price they have suggested
    :return: tenders
    """
    freight = Freight.query.get(request.json['freight_id'])
    if freight is None:
        return jsonify("there is no freight with that freight_id")
    return jsonify(freight.tenders)