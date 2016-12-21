__author__ = 'shahryar_slg'

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as jsonSerializer, SignatureExpired, BadSignature
from flask import json
from datetime import datetime
from pytz import timezone
from flask_admin.contrib.sqla import ModelView

from . import db
from . import app
from . import admin


tehran = timezone('Asia/Tehran')


class role(db.Model, json.JSONEncoder):

    """
    this class is actually an Enum , used in users table
    """
    __tablename__ = 'role'

    seq = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.TEXT, nullable=False)

    def __init__(self, title):
        self.title = title

    def json_form(self):
        return {
            '__type__': 'role',
            'title': self.title
        }


class User(db.Model, json.JSONEncoder):  # there is a relationship between User and Freight : User is parent , Freight is child
    """
    tip : you SHOULD provide each object of this class with a role_id yourself ! :
                1 corresponds with : customer
                2 corresponds with : courier
    """
    __tablename__ = 'users'

    email = db.Column(db.TEXT, unique=True,
                      nullable=True)
    username = db.Column(db.TEXT, unique=True)
    first_name = db.Column(db.TEXT)
    last_name = db.Column(db.TEXT)
    phonenumber_confirmed = db.Column(db.BOOLEAN, default=False)
    email_confirmed = db.Column(db.BOOLEAN, default=False)
    phonenumber = db.Column(db.INTEGER)
    id = db.Column(db.INTEGER, primary_key=True)
    freights = db.relationship('Freight',
                               backref=db.backref('freights'))
    role_id = db.Column(db.INTEGER, db.ForeignKey('role.seq'))
    role = db.relationship(role, backref=db.backref('users',
                                                    uselist=True,
                                                    cascade='delete,all'))
    password_hash = db.Column(db.TEXT, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return self.email_confirmed or self.phonenumber_confirmed

    @staticmethod
    def get_user(user_id=None, username=None, email=None):
        """
        :raises: exception if no argument is passed!
        :param: user_id or username or email
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

    def generate_auth_token(self, expiration=600):
        serializer = jsonSerializer(app.config['SECRET_KEY'], expires_in=expiration)
        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        serializer = jsonSerializer(secret_key=app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None     # valid token but expired
        except BadSignature:
            return None     # invalid token
        user = User.get_user(user_id=data['id'])
        return user

    def generate_email_confirmation_token(self, expiration=86400):  # token is valid for 24 hours .
        serializer = jsonSerializer(app.config['SECRET_KEY'], expires_in=expiration)
        return serializer.dumps({'confirm': self.username})

    @staticmethod
    def confirm_email_token(token):
        serializer = jsonSerializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return "expired"
        except BadSignature:
            return None
        print "data is :", data
        username = data['confirm']
        user = User.query.filter_by(username=username).first()
        return user


    def __repr__(self):
        return "user : " + str(self.username)
        # return "user : %s" str(self.username)

    def get_dict(self):
        dictionary = self.__dict__
        dictionary.pop('password_hash')
        dictionary.pop('_sa_instance_state')
        return dictionary

    def json_form(self):
        return {
            '__type__': 'User',
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'username': self.username
        }


class Dimension:

    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth


class Freight(db.Model, json.JSONEncoder):
    """
    later , other classes will inherit from this class
    classes like : grocery , furnicher , vehicle , etc.
    """

    __tablename__ = 'freights'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    name = db.Column(db.TEXT)
    price = db.Column(db.REAL)
    height = db.Column('height', db.REAL)
    width = db.Column('width', db.REAL)
    depth = db.Column('depth', db.REAL)
    weight = db.Column(db.REAL)
    destination = db.relationship('DestinationAddress')
    pickup_address = db.relationship('PickupAddress')
    # addresses = db.relationship('Address')
    receiver_name = db.Column(db.TEXT)
    receiver_phonenumber = db.Column(db.INTEGER, nullable=False)
    owner = db.Column(db.INTEGER, db.ForeignKey('users.id'))
    description = db.Column(db.TEXT)
    pictures = db.relationship('FreightPicture')
    creation_data = db.Column(db.DateTime, default=datetime.now(tehran))

    # overwriting ModelView :
    column_searchable_list = ['id', 'owner', 'creation_data', 'description', 'receiver_name']

    # this class is json serializable:
    def json_form(self):

        # following lines avoid 500 status code , in the case there is no destination or pickup_address
        info = {
            '__type__': "Freight",
            'name': self.name,
            'price': self.price,
            'creation_date': self.creation_data,
            'description': self.description,
            'id': self.id,
            'weight': self.weight,
            'width': self.width,
            'height': self.height,
            'depth': self.depth,
            # 'destination': self.destination[0],
            # 'pickup_address': self.pickup_address[0],
            'receiver_name': self.receiver_name,
        }
        try:
            info["destination"] = self.destination[0]
        except IndexError:
            pass
        try:
            info["pickup_address"] = self.pickup_address[0]
        except IndexError:
            pass

        # todo: what about pictures?
        return info


    def __repr__(self):
        return "freight: owner : " + \
               str(User.get_user(user_id=self.owner)) + " name:"+str(self.name)

    def get_dict(self):
        dictionary = self.__dict__
        dictionary.pop('_sa_instance_state')
        return dictionary


class PickupAddress(db.Model, json.JSONEncoder):

    __tablename__ = 'pickupAddresses'
    country = db.Column(db.TEXT)
    city = db.Column(db.TEXT)
    rest_of_address = db.Column(db.TEXT)
    postal_code = db.Column(db.INTEGER)
    id = db.Column(db.INTEGER, primary_key=True)
    # freights = db.relationship('Freight',backref='address',lazy='dynamic')
    freight_id = db.Column(db.INTEGER, db.ForeignKey('freights.id'))

    def json_form(self):
        return {
            '__type__': 'PickupAddress',
            'country': self.country,
            'city': self.city,
            'rest_of_address': self.rest_of_address,
            'postal_code': self.postal_code,
            'id': self.id
        }

    def __repr__(self):
        address_string = ' '.join([self.country,
                                   self.city,
                                   self.rest_of_address, 'zipcode : '
                                   + str(self.postal_code)])
        return address_string

    @staticmethod
    def str_to_object(address_string):
        """str --> (object of Address)"""
        words_of_address = address_string.split()
        rod = ""
        for part in words_of_address[2:]:
            if 'zipcode' in part:
                break
            rod = rod + part + ' '
        address = PickupAddress(country=words_of_address[0],
                                city=words_of_address[1],
                                rest_of_address=rod,
                                zipcode=words_of_address[-1]
                                )
        return address


class DestinationAddress(db.Model, json.JSONEncoder):

    __tablename__ = 'destinationAddress'
    country = db.Column(db.TEXT)
    city = db.Column(db.TEXT)
    rest_of_address = db.Column(db.TEXT)
    postal_code = db.Column(db.INTEGER)
    id = db.Column(db.INTEGER, primary_key=True)
    # freights = db.relationship('Freight',backref='address',lazy='dynamic')
    freight_id = db.Column(db.INTEGER, db.ForeignKey('freights.id'))

    def json_form(self):
        return {
            '__type__': 'DestinationAddress',
            'country': self.country,
            'city': self.city,
            'rest_of_address': self.rest_of_address,
            'postal_code': self.postal_code,
            'id': self.id
        }

    def __repr__(self):
        address_string = ' '.join([self.country,
                                   self.city,
                                   self.rest_of_address, 'zipcode : '
                                   + str(self.postal_code)])
        return address_string

    @staticmethod
    def str_to_object(address_string):
        """str --> (object of Address)"""
        words_of_address = address_string.split()
        rod = ""
        for part in words_of_address[2:]:
            if 'zipcode' in part:
                break
            rod = rod + part + ' '
        address = DestinationAddress(country=words_of_address[0],
                                     city=words_of_address[1],
                                     rest_of_address=rod,
                                     zipcode=words_of_address[-1]
                                     )
        return address


class FreightPicture(db.Model, json.JSONEncoder):
    __tablename__ = 'freight_pictures'
    filename = db.Column(db.TEXT, nullable=False)
    path = db.Column(db.TEXT, nullable=False)
    freight_id = db.Column(db.INTEGER, db.ForeignKey('freights.id'))
    id = db.Column(db.INTEGER, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now(tehran))

    def json_form(self):
        return {
            '__type__': 'FreightPicture',
            'filename': self.filename,
            'path': self.path,
            'id': self.id,
            'created': self.created,
            'freight_id': self.freight_id
        }


class Tender(db.Model):
    __tablename_ = 'tenders'
    id = db.Column(db.INTEGER, primary_key=True)

    #  there are some One-to-Many relations: (based on:  http://flask-sqlalchemy.pocoo.org/2.1/quickstart)
    freight_id = db.Column(db.INTEGER, db.ForeignKey('freights.id'))
    freight = db.relationship('Freight', backref='tenders')

    courier_id = db.Column(db.INTEGER, db.ForeignKey('users.id'))
    courier = db.relationship('User', backref='tenders')  # courier = tenderer : the one who asks to do the shipment!

    # extra information:
    suggested_price = db.Column(db.REAL)
    description = db.Column(db.TEXT)
    creation_data = db.Column(db.DateTime, default=datetime.now(tehran))

    # if approved is True, the courier making this record won the trend
    # and have to ship the freight!
    approved = db.Column(db.BOOLEAN, default=False)

    def __init__(self, courier, freight, price, description, creation_date=datetime.now(tehran)):
        self.courier = courier
        self.freight = freight
        self.suggested_price = price
        self.description = description
        self.creation_data = creation_date

    def json_form(self):
        return {
            '__type__': 'Tender',
            'freight_id': self.freight_id,
            'courier_id': self.courier_id,
            'price': self.suggested_price,
            'creation_date': self.creation_data
        }

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Freight, db.session))
admin.add_view(ModelView(DestinationAddress, db.session))
admin.add_view(ModelView(PickupAddress, db.session))
admin.add_view(ModelView(FreightPicture, db.session))
admin.add_view(ModelView(Tender, db.session))



class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Freight)or\
                isinstance(obj, User) or\
                isinstance(obj, role) or\
                isinstance(obj, DestinationAddress) or \
                isinstance(obj, PickupAddress):

            return obj.json_form()

        else:
            return json.JSONEncoder.default(self, obj)


app.json_encoder = MyEncoder