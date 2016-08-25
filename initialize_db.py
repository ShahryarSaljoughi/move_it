__author__ = 'shahryar_slg'

from models import role
from routes import db


customer = role(title='customer')
courier = role(title='courier')

def init_db():
    """
    this function is responsible for initializing
    the lookup tables in the database
    :return: nothing!
    """

    #fedding database the roles :
    db.session.add(customer)
    db.session.add(courier)
    db.session.commit()

    db.session.commit()

def testy():
    pass