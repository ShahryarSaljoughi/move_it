from flask import g
from cerberus import Validator
from app.main.validation import schemas
from app.models import Freight


# other validation methods will be called by this function
def validate(document, viewfunction):
    if viewfunction == 'main.views.TenderCore.show_tender':
        return validate_show_tender(document)
    elif viewfunction == 'main.views.'


def validate_show_tender(document):
    """
    validates data associated with the view function: TenderCore.show_tender
    :param document: request.json
    :return result: result is a dictionary, containing keys 'is_validated'(boolean) and 'errors'(dictionary)
    """

    v = Validator(schemas.show_tenders)
    result = dict()
    is_doc_validated = v.validate(document)

    errors = v.errors  # so, errors is a dict!
    # check if freight id is in database
    if is_doc_validated and not Freight.query.get(document['freight_id']):
        assert 'freight_id' not in v.errors.keys()
        errors['freight_id'] = list()
        errors['freight_id'].append('freight_id does not found')
        is_doc_validated = False

    result['is_validated'] = is_doc_validated
    result['errors'] = errors

    return result


def validate_freight_received(document):
    """
    validates data associated with the view function: TenderCore.freight_received
    :param document: request.json
    :return: result , result is a dictionary, containing keys 'is_validated' and 'errors'
    """
    v = Validator(schema=schemas.freight_received)

