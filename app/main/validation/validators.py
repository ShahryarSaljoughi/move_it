from DNS import TimeoutError
from flask import g, request, session
import phonenumbers
from validate_email import validate_email
from phonenumbers import NumberParseException
from app.models import role, Freight, Tender, User


# custom validators:
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
    if freight.owner.id != g.user.id:
        error('other_errors', "Only the owner of the freight is permitted")


def freight_not_taken(field, value, error):
    freight = Freight.query.get(value)
    if freight is not None:
        if freight.is_courier_chosen:
            error('other_errors', "this freight is already assigned to another courier")


def user_is_tender_freight_owner(field, value, error):  # for checking user's permissions ...

    tender = Tender.query.get(value)
    if g.user.id != tender.freight.owner.id:  # g.user = request.json['user_id]
        error('other_errors', "Only the owner of the freight is permitted")


def is_phonenumber(field, value, error):
    try:
        phonenumber = phonenumbers.parse(number=value, region='IR')
        if not (phonenumbers.is_valid_number(phonenumber) and phonenumbers.is_possible_number(phonenumber)):
            error(field, "phone number is not valid")
    except NumberParseException:
        error(field, "phone number is not valid")


def unconfirmed_account_in_session(field, value, error):
    """
    used in confirmation of an account registered with phonenumber
    """
    if 'inactive_account_phone' not in session:
        error('other_errors', "there is no pending phone number to be confirmed")


def is_email_valid(field, value, error):
    try:
        is_valid = validate_email(email=value)
    except TimeoutError: # todo : I'm not sure maybe we should tell client sth went wrong!
        is_valid = False

    if not is_valid:
        error(field, "email is not valid")


def is_username_unique(field, value, error):
    user = User.query.filter_by(username=value).first()
    if user:
        error(field, "This username already exists")


def is_email_unique(field, value, error):
    user = User.query.filter_by(email=value).first()
    if user:
        error(field, "This email address already exists")
