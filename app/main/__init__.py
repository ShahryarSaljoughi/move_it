from flask import Blueprint

__author__ = 'shahryar_saljoughi'

main = Blueprint('main', __name__)

from app.main.views import views, freightCRUD, registration, TenderCore