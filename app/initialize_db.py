__author__ = 'shahryar_slg'

from app.models import role
# from app.main.views import db
from app import db


def init_db():
    """
    this function is responsible for initializing
    the lookup tables in the database
    :return: nothing!
    """

    customer = role(title='customer')
    courier = role(title='courier')

    #fedding database the roles :
    db.session.add(customer)
    db.session.add(courier)
    db.session.commit()
