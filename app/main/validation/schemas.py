from app.main.validation.validators import *


# TenderCore schemas **************************************


show_tenders = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': id_found},
    'rules': {}
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
    },
    'rules': {}
}

approve_courier = {
    'tender_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'validator': [id_found, user_is_tender_freight_owner]
    },
    'rules': {}
}

apply_freight = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1, 'validator': [id_found, freight_not_taken]},
    'price': {'type': 'number', 'required': True, 'min': 0},
    'description': {'type': 'string', 'required': False, 'maxlength': 4000},
    'user_type': {'allowed': [r.title for r in role.query.all()],  # user_type : [courier, customer]
                  'required': True,                                # (other roles can be added later)
                  'validator': is_courier},
    'rules': {}
}
# End of TenderCore schemas ********************************

# freightCRUD schemas :     ********************************

delete_freight = {
    'freight_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'validator': [id_found, user_is_freight_owner]
    },
    'rules': {}
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
    },
    'rules': {}
}

create_freight = {
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
    'rules': {}
}


# REGISTRATION.PY :
signup_using_phonenumber = {
    "username": {
        'type': 'string',
        'required': True,
        'validator': is_username_unique
    },
    'password': {'type': 'string', 'required': True},
    'role_id': {'type': 'integer', 'required': True},
    'first_name': {'type': 'string', 'required': True},
    'last_name': {'type': 'string', 'required': True},
    'phonenumber': {'type': 'string', 'validator': is_phonenumber, 'required': True},
    'rules': {}
}

confirm_phonenumber = {
    'code': {'type': 'integer', 'required': True},
    'rules': {'validator': unconfirmed_account_in_session}
}

signup_using_email = {
    'email': {
        'required': True,
        'validator': [is_email_valid, is_email_unique]
    },
    "username": {
        'type': 'string',
        'required': True,
        'validator': is_username_unique
    },
    'password': {'type': 'string', 'required': True},
    'role_id': {'type': 'integer', 'required': True},
    'first_name': {'type': 'string', 'required': True},
    'last_name': {'type': 'string', 'required': True},
    'rules': {}
}

verify_credentials = {
    'username': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True},
    'rules': {}
}
