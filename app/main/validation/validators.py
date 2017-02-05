from cerberus import Validator
from app.main.validation import schemas



def validate_show_tender(document):
    """
    validates data associated with the view function: TenderCore.show_tender
    :param document: request.json
    :return: (boolean, list of errors)
    """

    v = Validator(schemas.show_tenders)
    v.validate(document=document)



