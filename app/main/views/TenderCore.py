from flask import g, request, jsonify
from app import db
from app.main import main
from app.main.views import auth
from app.models import Tender, Freight
from app.main.validation.core import validate
from app.main.appExceptions import ValidationError, NoJSONError

__author__ = 'shahryar_saljoughi'


#  CORE  ***************************************************************************************************************


@main.route('/apply_freight', methods=['POST'])
@auth.login_required
def apply_freight():
    """
    this view function makes an apply for a freight !
    """
    if not request.json:
        raise NoJSONError()

    validation_result = validate(
        document=request.json,
        viewfunction=apply_freight
    )
    if not validation_result['is_validated']:
        raise ValidationError(errors=validation_result['errors'], status_code=400)

    freight_id = request.json['freight_id']
    price = request.json['price']

    freight = Freight.query.get(freight_id)

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

    if not request.json:
        raise NoJSONError()

    validation_result = validate(document=request.json, viewfunction=approve_courier)
    if not validation_result['is_validated']:
        raise ValidationError(errors=validation_result['errors'], status_code=400)

    tender_id = request.json['tender_id']
    tender = Tender.query.get(tender_id)

    tender.approved = True
    tender.freight.is_courier_chosen = True
    db.session.commit()
    return jsonify('successful'), 200


@main.route('/freight_delivered', methods=['POST'])
@auth.login_required
def freight_received():

    if not request.json:
        raise NoJSONError()

    result = validate(request.json, freight_received)

    if not result['is_validated']:
        raise ValidationError(errors=result['errors'], message='bad request', status_code=400)

    freight = Tender.query.get(request.json['tender_id']).freight \
        if 'tender_id' in request.json else Freight.query.get(request.json['freight_id'])

    freight.is_delivered = True
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

    if not request.json:
        raise NoJSONError()

    validation_result = validate(
        document=request.json,
        viewfunction=show_tenders
    )

    if not validation_result['is_validated']:
        raise ValidationError(
            message='bad request',
            errors=validation_result['errors'],
            status_code=400
        )

    freight = Freight.query.get(request.json['freight_id'])

    return jsonify(freight.tenders)
