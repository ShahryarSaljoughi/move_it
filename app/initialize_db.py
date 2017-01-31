__author__ = 'shahryar_slg'
from random import choice
from app.models import role, User
# from app.main.views import db
from app import db


def init_db():
    """
    this function is responsible for initializing
    the lookup tables in the database
    :return: nothing!
    """
    if len(role.query.all()) == 0:
        customer = role(title='customer')
        courier = role(title='courier')

        # fedding database the roles :
        db.session.add(customer)
        db.session.add(courier)
        db.session.commit()

# let's fill database with some data (fake!)


# add users
first_names = ['shahryar', 'pegah', 'alireza', 'hadi',
              'shima', 'james', 'sam', 'fariba', 'siamak',
              'marjan', 'elaheh', 'john', 'leila', 'reyhaneh',
              'parisa', 'kimia', 'mohammad','sadeq', 'esmaeil',
              'mahdiye', 'morteza', 'mehdi', 'amir', 'hooman',
              'sina', 'soroush', 'saleh']

last_names = ['maleki', 'fateh', 'basharzad', 'saljoughi',
              'khatibi', 'seyyedin', 'mortazavi', 'montakhabi',
              'bakhtiari', 'vosoghi', 'hatami', 'rad', 'bahrami',
              'rock', 'khatami', 'badloo']

courier = role.query.get(2)
customer = role.query.get(1)


def add_users():
    for i in range(50):
        fn = choice(first_names)
        ls = choice(last_names)
        username = '{}_{}{}'.format(fn, ls, choice(range(100)))
        user = User(
            first_name=fn,
            last_name=ls,
            username=username,
            role_id=choice([1, 2])
        )
        user.set_password('fake_user')
        db.session.add(user)
        db.session.commit()


# add some freights:
def add_freights():
    for i in range(100):
        pass
