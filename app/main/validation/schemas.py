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
        error('other_errors', "only couriers can use this api!")


def user_is_freight_owner(field, value, error):  # for checking user's permissions ...

    freight = Freight.query.get(value)
    if freight.owner.id != g.user:
        error('other_errors', "Only the owner of the freight is permitted")


def freight_not_taken(field, value, error):
    freight = Freight.query.get(value)
    if freight.is_courier_chosen:
        error('other_errors', "this freight is already assigned to another courier")


def user_is_tender_freight_owner(field, value, error):  # for checking user's permissions ...

    tender = Tender.query.get(value)
    if g.user != tender.freight.owner.id:  # g.user = request.json['user_id]
        error('other_errors', "Only the owner of the freight is permitted")

# TenderCore schemas **************************************


show_tenders = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': id_found}
}

freight_received = {   # acts like exclusive or :
    'tender_id': {     # either tender_id or freight_id should exist. (only one of them)
        'type': 'integer',
        'required': True,
        'min': 1,
        'excludes': 'freight_id',
        'validator': [user_is_tender_freight_owner, id_found]
    },
    'freight_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'validator': [id_found, user_is_freight_owner],
        'excludes': 'tender_id'
    }
}

approve_courier = {
    'tender_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'validator': [id_found, user_is_tender_freight_owner]
    }
}

apply_freight = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': [id_found, freight_not_taken]},
    'price': {'type': 'number', 'required': True, 'min': 0},
    'description': {'type': 'string', 'required': False, 'maxlength': 4000},
    'user_type': {'allowed': [r.title for r in role.query.all()],  # user_type : [courier, customer]
                  'required': True,                                # (other roles can be added later)
                  'validator': is_courier}
}
# End of TenderCore schemas ********************************

# freightCRUD schemas :     ********************************

delete_freight = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': id_found}
}