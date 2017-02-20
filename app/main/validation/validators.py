from flask import g
from app.main.views import TenderCore
from cerberus import Validator
from app.main.validation import schemas
from app.models import Freight, Tender


# other validation methods will be called by this function
def validate(document, viewfunction):

    schema = eval('schemas.{}'.format(viewfunction.func_name))
    v = Validator(schema)

    result = dict()
    result['is_validated'] = v.validate(document)
    result['errors'] = dict(v.errors)
    # result will be modified more
    # as the below specific validators are called! (side effect are used!)

    exec('validate_{}({}, {}, {})'.format(viewfunction.func_name, document, result, v))
    return result


def validate_freight_received(document, result, validator):
    """
    validates data associated with the view function: TenderCore.freight_received
    :param document: request.json
    :param result: , result is a dictionary, containing keys: 'is_validated' and 'errors'
    :param validator: an instance of cerberus.Validator . validator.schema is already set.
    """

    is_doc_validated = result['is_validated']
    errors = result['errors']

    # check if tender exists in database:

    if is_doc_validated:
        # tender = Tender.query.get(document['tender_id'])  # tender of None
        # if tender is None:
        #    assert 'tender_id' not in errors.keys()  # because doc is validated so far!
        #    errors['tender_id'] = ['tender_id not found!']
        #    is_doc_validated = False
        pass

        # only the owner of the freight can approve it's received! Let's check it:
    elif g.user != Tender.query.get(document['tender_id']).freight.owner:
        errors['access denied'] = 'only the owner of the freight can approve it is delivered'
        is_doc_validated = False

    result['is_validated'] = is_doc_validated
    result['errors'] = errors


def validate_show_tender(document, result, validator):
    """
    validates data associated with the view function: TenderCore.show_tender
    :param document: request.json
    :param result: result is a dict to be modified!
    :param validator: validator is an instance of cerberus.Validator(schema) with the proper schema!
    """

    # check if freight id is in database
    if result['is_validated'] and not Freight.query.get(document['freight_id']):
        assert 'freight_id' not in result['errors'].keys()
        result['errors']['freight_id'] = list()
        result['errors']['freight_id'].append('freight not found')
        result['is_validated'] = False


def validate_approve_courier(document, result):
    """

    :param document: received json (that we are trying to validate)
    :param result: indicating the current state of validation
    :return: this function is using side effects of dictionaries instead of return!
    """

    if result['is_validated']:
        assert 'tender_id' not in result['errors'].keys()
        tender = Tender.query.get(document['tender_id'])

        # check ir tender_id is in database:
        if tender is None:
            result['errors']['tender_id'] = ['tender not found']
            result['is_validated'] = False

        # check if the user has permission to approve courier:
        elif g.user != tender.freight.owner:
            result['errors']['access denied'] = 'only the owner of the freight' \
                                                ' has the permission to approve courier'


def validate_apply_freight(document, result):

    # check if freight_id is valid
    if 'freight_id' not in result['errors'].keys():
        freight = Freight.query.get(document['freight_id'])
        if freight is None:
            result['errors']['freight_id'] = ['freight_id not found']
            result['is_validated'] = False

    if g.user.role.title != 'courier':
        result['is_validated'] = False
        result['errors']['access_denied'] = ['only couriers can apply for a freight']
