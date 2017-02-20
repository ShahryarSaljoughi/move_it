from flask import g
from app.main.views import TenderCore
from cerberus import Validator
from app.main.validation import schemas
from app.models import Freight, Tender, role


# other validation methods will be called by this function
def validate(document, viewfunction):

    schema = eval('schemas.{}'.format(viewfunction.func_name))
    v = Validator(schema)

    result = dict()
    result['is_validated'] = v.validate(document)
    result['errors'] = dict(v.errors)

    # result will be modified more
    # as the below specific validators are called! (side effect are used!)
    try:
        exec('validate_{}({}, {}, {})'.format(viewfunction.func_name, document, result, v))
    # maybe there is no specific validate_... method for this view function:
    except NameError:
        pass

    return result


def validate_freight_received(document, result, validator):
    """
    validates data associated with the view function: TenderCore.freight_received
    :param document: request.json
    :param result: , result is a dictionary, containing keys: 'is_validated' and 'errors'
    :param validator: an instance of cerberus.Validator . validator.schema is already set.
    """

    # only the owner of the freight can approve it's received! Let's check it:
    if g.user != Tender.query.get(document['tender_id']).freight.owner:
        result['errors']['access denied'] = 'only the owner of the freight can approve it is delivered'
        result['is_validated'] = False


def validate_show_tender(document, result, validator):
    """
    validates data associated with the view function: TenderCore.show_tender
    :param document: request.json
    :param result: result is a dict to be modified!
    :param validator: validator is an instance of cerberus.Validator(schema) with the proper schema!
    """
    pass


def validate_approve_courier(document, result):
    """

    :param document: received json (that we are trying to validate)
    :param result: indicating the current state of validation
    :return: this function is using side effects of dictionaries instead of return!
    """

    if result['is_validated']:
        assert 'tender_id' not in result['errors'].keys()
        tender = Tender.query.get(document['tender_id'])
        # check if the user has permission to approve courier:
        if g.user != tender.freight.owner:
            result['errors']['access denied'] = 'only the owner of the freight' \
                                                ' has the permission to approve courier'


def validate_apply_freight(document, result):
    pass
