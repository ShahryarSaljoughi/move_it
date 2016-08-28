__author__ = 'shahryar_slg'

from flask import Flask
# import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.root_path+'\\database\\shipment.db'
# app.config['SQLALCHEMY_NATIVE_UNICODE'] = True


db = SQLAlchemy(app)
# app.secret_key = "development-key"

#import blueprints
from .main import main as main_blue_print
app.register_blueprint(main_blue_print)