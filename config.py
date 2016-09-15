__author__ = 'shahryar_slg'

import os
# from app import app

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.root_path+'\\database\\shipment.db'
# app.config['SQLALCHEMY_NATIVE_UNICODE'] = True

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + app.root_path+'\\database\\shipment.db'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, '\\app\\database\\shipment.db')
# SQLALCHEMY_DATABASE_URI = 'sqlite:///E:\\flask_example\\move_it\\app\\database\\shipment.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + '\\app\\database\\shipment.db'
# SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, '\\app\\database\\db_repository')

PORT = 9000
HOST = '0.0.0.0'
THREADS_PER_PAGE = 2

SECRET_KEY = "scared rabbits fly"

# flask_mail configuration:
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
ADMINS = ['s.shahryar75@gmail.com']
MAIL_USERNAME = 's.shahryar75'
MAIL_PASSWORD = 'meajcveaxrnvwvhy'
MAIL_DEFAULT_SENDER = ('SHIPMENT TEAM', 's.shahryar75@gmail.com')

# image uploading configuration
FREIGHT_PICTURES_DIR = BASE_DIR + "\\media\\freight_pictures"
ALLOWED_PICTURE_EXTENSIONS = ['jpg', 'jpeg', 'png']

MIGRATIONS_DIR = BASE_DIR + '\\app\\database\\migrations'  # os.path.join(BASE_DIR, '\\app\\database\\migrations')

