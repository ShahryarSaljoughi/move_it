
# Tender schemas **************************************

show_tenders = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1}
}

freight_received = {
    'tender_id': {'type': 'integer', 'required': True, 'min': 1}
}

approve_courier = {
    'tender_id': {'type': 'integer', 'required': True, 'min': 1}
}

apply_freight = {
    'freight_id': {'type': 'integer', 'required': True, 'min': 1},
    'price': {'type': 'number', 'required': True, 'min': 0},
    'description': {'type': 'string', 'required': False, 'maxlength': 3500}
}
# End of Tender schemas ********************************
