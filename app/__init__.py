__author__ = 'shahryar_slg'

from flask import Flask
# import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

# note that by moving the next code to the line after registering the blueprint ,
# we will get an error , because db is needed in the main package
db = SQLAlchemy(app)

# import blueprints
from .main import main as main_blue_print
from app.models import *
app.register_blueprint(main_blue_print)
db.create_all()
from . import initialize_db
initialize_db.init_db()
# app.secret_key = "secret-key!"
# app.config['secret_key'] = "scared rabbits fly"

