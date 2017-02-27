from flask import g, request
from app.models import role, Freight, Tender


# custom rules for validators:
def id_found(field, value, error):

    cls = field[:len(field)-3].title()  # freight_id --> Freight
    try:
        data = eval('{}.query.get({})'.format(cls, value))
        if data is None:
            error(field, "{} not found".format(field))

    except NameError:
        # some class names can't be reached via the approach I designed ! these class names are handled here:
        pass  # todo: associate field with class names!


def is_courier(field, value, error):
    if value != role.query.get(2).title:
        error(field, "only couriers can use this route!")


def user_is_freight_owner(field, value, error):  # for checking user's permissions ...
    assert hasattr(request.json, 'freight_id')
    freight = Freight.query.get(request.json['freight_id'])
    if freight.owner.id != g.user:
        error(field, "Only the owner of the freight is permitted")


def user_is_tender_freight_owner(field, value, error):  # for checking user's permissions ...

    assert hasattr(request.json, 'tender_id')
    tender = Tender.query.get(request.json['tender_id'])
    if g.user != tender.freight.owner.id:  # g.user = request.json['user_id]
        error(field, "Only the owner of the freight is permitted")

# TenderCore schemas **************************************


show_tenders = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': id_found}
}

freight_received = {
    'tender_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': id_found}
}

approve_courier = {
    'tender_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': id_found}
}

apply_freight = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': id_found},
    'price': {'type': 'number', 'required': True, 'min': 0},
    'description': {'type': 'string', 'required': False, 'maxlength': 3500},
    'user_type': {'allowed': [r.title for r in role.query.all()],  # user_type : [courier, customer]
                  'required': True,                                # (other roles can be added later)
                  'validator': is_courier}
}
# End of TenderCore schemas ********************************

# freightCRUD schemas :     ********************************

delete_freight = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': id_found}
}