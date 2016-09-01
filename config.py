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

PORT = 9000
HOST = '0.0.0.0'
THREADS_PER_PAGE = 2

"""
since , the server is intended to be RESTfull , there should not be any session ! hence I'm not setting the secret_key
"""



