__author__ = 'shahryar_slg'

def init_db():
    """
    this function is responsible for initializing
    the lookup tables in the database
    :return: nothing!
    """
    from models import role
    from routes import db

    #fedding database the roles :
    customer = role(title='customer')
    db.session.add(customer)
    db.session.commit()

    courier = role(title='courier')
    db.session.add(courier)
    db.session.commit()


