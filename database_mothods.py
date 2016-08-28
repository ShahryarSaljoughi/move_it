__author__ = 'shahryar_slg'

from models import User
from routes import db


def get_user(user_id=None, username=None, email=None):
    """
    :raises: exception if no argument is passed!
    :param: user_id or username
    :return: User object
    """
    if user_id is not None:
        user = User.query.filter_by(id=user_id).first()
    elif username is not None:
        user = User.query.filter_by(username=username).first()
    elif email is not None:
        user = User.query.filter_by(email=email).first()
    else:
        raise Exception("takes exactly one argument , which can be email or username or user_id)")
    return user
