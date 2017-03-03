from flask import g
from cerberus import Validator
from app.main.validation import schemas
from app.models import Freight, Tender, role
# from app.main.views import TenderCore

# class MyValidator(Validator):
#
#     def _validate_unique(self, unique, field, value):
#         """Test if value (email , username, id etc.) is unique
#
#       The rule's arguments are validated against this schema:
#       {'allowed': ['email', 'username'], 'type': 'string'}
#       """
#       # note that other fields, later (as needed), can be added to the list above: [email, username]
#
#       pass


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
        exec('validate_{}({}, {}, {})'.format(viewfunction.func_name, 'document', 'result', 'v'))

    # maybe there is no specific validate_... method for this view function:
    except NameError:
        pass

    return result

"""
the following functions will be omitted soon!
Once upon a time!! they performed a lot of validation tasks, but now
these tasks are done by schemas! and custom validators defined there.
"""


def validate_freight_received(document, result, validator):
    """
    validates data associated with the view function: TenderCore.freight_received
    :param document: request.json
    :param result: , result is a dictionary, containing keys: 'is_validated' and 'errors'
    :param validator: an instance of cerberus.Validator . validator.schema is already set.
    """
    pass


def validate_show_tender(document, result, validator):
    """
    validates data associated with the view function: TenderCore.show_tender
    :param document: request.json
    :param result: result is a dict to be modified!
    :param validator: validator is an instance of cerberus.Validator(schema) with the proper schema!
    """
    pass


def validate_approve_courier(document, result, validator):
    """

    :param document: received json (that we are trying to validate)
    :param result: indicating the current state of validation
    :return: this function is using side effects of dictionaries instead of return!
    """
    pass


def validate_apply_freight(document, result, validator):
    pass
