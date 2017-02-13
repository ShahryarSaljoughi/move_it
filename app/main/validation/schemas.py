
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
# End of Tender schemas ********************************
