__author__ = 'panizava'

from flask import Blueprint


main = Blueprint('main', __name__)

from app.main.views import searchFreight
from app.main.views import views_general, freightCRUD, registration
