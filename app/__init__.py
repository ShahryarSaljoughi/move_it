__author__ = 'shahryar_slg'

from flask_admin import Admin
from flask import Flask
# import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config')

# note that by moving the next code to the line after registering the blueprint ,
# we will get an error , because db is needed in the main package
db = SQLAlchemy(app)

# database migrations ! (it helps me to update the database structure without losing data)
migrate = Migrate(app, db, directory=app.config['MIGRATIONS_DIR'])

# admin blog:
admin = Admin(app, 'admin blog', template_mode='bootstrap3')
# admin.add_view(ModelView())
# import blueprints
from .main import main as main_blue_print
from app.models import *
app.register_blueprint(main_blue_print)
db.create_all()
from . import initialize_db
initialize_db.init_db()

