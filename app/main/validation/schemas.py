from flask import g, request, session
import phonenumbers
from validate_email import validate_email

from phonenumbers import NumberParseException
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


def is_phonenumber(field, value, error):
    try:
        phonenumber = phonenumbers.parse(number=value, region='IR')
        if not (phonenumbers.is_valid_number(phonenumber) and phonenumbers.is_possible_number(phonenumber)):
            error(field, "phone number is not valid")
    except NumberParseException:
        error(field, "phone number is not valid")


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
    'freight_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'validator': [id_found, user_is_freight_owner]
    }
}

update_freight = {
    'freight_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'validator': [id_found, user_is_freight_owner]
    },
    'new_data': {
        'type': 'dict',
        'schema': {
            'name': {'type': 'string'},
            'height': {'type': 'number'},
            'width': {'type': 'number'},
            'depth': {'type': 'number'},
            'receiver_name': {'type': 'string'},
            'receiver_phonenumber': {'validator': is_phonenumber},
            'weight': {'type': 'number'},
            'description': {'type': 'string', 'maxlength': 4000},
            'destination': {
                'type': 'dict',
                'schema': {
                    'country': {'type': 'string'},
                    'city': {'type': 'string'},
                    'rest_of_address': {'type': 'string'},
                    'postal_code': {'type': 'integer'}
                }
            },
            'pickup_address': {
                'type': 'dict',
                'schema': {
                    'country': {'type': 'string'},
                    'city': {'type': 'string'},
                    'rest_of_address': {'type': 'string'},
                    'postal_code': {'type': 'integer'}
                }
            },
        }
    }
}

create_freight = {

    'type': 'dict',
    'schema': {
        'name': {'type': 'string', 'required': True},
        'height': {'type': 'number'},
        'width': {'type': 'number'},
        'depth': {'type': 'number'},
        'receiver_name': {'type': 'string', 'required': True},
        'receiver_phonenumber': {'validator': is_phonenumber, 'required': True},
        'weight': {'type': 'number', 'required': True},
        'description': {'type': 'string', 'maxlength': 4000},
        'price': {'type': 'number', 'min': 0},
        'destination': {
            'type': 'dict',
            'required': True,
            'schema': {
                'country': {'type': 'string', 'required': True},
                'city': {'type': 'string', 'required': True},
                'rest_of_address': {'type': 'string', 'required': True},
                'postal_code': {'type': 'integer', 'required': True}
            }
        },
        'pickup_address': {
            'type': 'dict',
            'required': True,
            'schema': {
                'country': {'type': 'string', 'required': True},
                'city': {'type': 'string', 'required': True},
                'rest_of_address': {'type': 'string', 'required': True},
                'postal_code': {'type': 'integer', 'required': True}
            }
        },
    }
}


def unconfirmed_account_in_session(field, value, error):
    if 'inactive_account_phone' not in session:
        error('other_errors', "there is no pending phone number to be confirmed")


def is_email_valid(field, value, error):
    is_valid = validate_email(
        email=value,
        check_mx=True,
        verify=True
    )

    if not is_valid:
        error(field, "email is not valid")

# REGISTRATION.PY :
signup_using_phonenumber = {
    "username": {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True},
    'role_od': {'type': 'integer', 'required': True},
    'first_name': {'type': 'string', 'required': True},
    'last_name': {'type': 'string', 'required': True},
    'phonenumber': {'type': 'string', 'validator': is_phonenumber, 'required': True}
}

confirm_phonenumber = {
    'code': {'type': 'integer', 'required': True},
    'rules': {'validator': unconfirmed_account_in_session}
}

signup_using_email = {
    "username": {'type': 'string', 'required': True},  # todo : check if it is unique
    'password': {'type': 'string', 'required': True},
    'role_od': {'type': 'integer', 'required': True},
    'first_name': {'type': 'string', 'required': True},
    'last_name': {'type': 'string', 'required': True},
    'email': {'required': True, 'validator': is_email_valid}
}
