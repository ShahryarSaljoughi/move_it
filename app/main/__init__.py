__author__ = 'panizava'

from flask import Blueprint


main = Blueprint('main', __name__)

from app.main.views import views, freightCRUD, registration
