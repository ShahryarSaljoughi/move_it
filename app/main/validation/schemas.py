from app.models import role


# custom rule for validators:
def id_found(field, value, error):

    cls = field[:len(field)-3].title()  # freight_id --> Freight
    try:
        data = eval('{}.query.get({})'.format(cls, field))
        if data is None:
            error(field, "{} not found".format(field))

    except NameError:
        # some class names can't be reached via the approach I designed ! these class names are handled here:
        pass  # todo: associate field with class names!

# Tender schemas **************************************

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
    'user_type': {'allowed': [role.query.get(2).title],  # user_type : courier
                  'required': True}
}
# End of Tender schemas ********************************
