__author__ = 'shahryar_slg'


from routes import db


class User(db.Model):

    __tablename__='users'

    email = db.Column(db.TEXT)
    username = db.Column(db.TEXT,unique=True)
    password = db.Column(db.TEXT)
    role = db.Column(db.INTEGER)
    phonenumber = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER, primary_key=True)
    freights = db.relationship('Freight', backref='person', lazy='dynamic')

    def __init__(self, username, password, email, role, phonenumber):
        self.email = email
        self.password = password
        self.role = role
        self.phonenumber = phonenumber
        self.username = username


class Address(db.Model):

    __tablename__='address'
    country=db.Column(db.TEXT)
    city=db.Column(db.TEXT)
    rest_of_address=db.Column(db.TEXT)
    postal_code=db.Column(db.INTEGER)
    address_id=db.Column(db.INTEGER,primary_key=True)
    freights = db.relationship('Freight',backref='address',lazy='dynamic')

    def __init__(self, country, city, rest_of_address, zipcode):
        self.country = country
        self.city = city
        self.rest_of_address = rest_of_address
        self.zipcode = zipcode

    def __repr__(self):
        address_string = ' '.join([self.country,
                                   self.city,
                                   self.rest_of_address, 'zipcode : '
                                   + str(self.zipcode)])
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
        address = Address(country=words_of_address[0],
                          city=words_of_address[1],
                          rest_of_address=rod,
                          zipcode=words_of_address[-1]
                          )
        return address


class Dimension:

    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth


class Freight(db.Model) :
    """
    later , other classes will inherit from this class
    classes like : grocery , furnitcher , vehicle , etc.
    """

    __tablename__='freight'


    freight_id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.TEXT)
    price = db.Column(db.REAL)
    dimension.height = db.Column('height', db.REAL)
    dimension.width = db.Column('width', db.REAL)
    dimension.depth = db.Column('depth', db.REAL)
    group = db.Column(db.INTEGER)
    weight = db.Column(db.REAL)
    destination = db.Column(db.INTEGER,db.ForeignKey('address.address_id') )
    pickup_address = db.Column(db.INTEGER,db.ForeignKey('address.address_id'))
    receiver_name = db.Column()
    owner = db.Column(db.INTEGER,db.ForeignKey('users.user_id'))

    def __init__(self, name, weight,
                 destination, pickup_address, dimension,
                 price, owner, receiver_name, freight_id, group):
        self.name = name
        self.weight = weight
        self.destination = destination
        self.pickup_address = pickup_address
        self.dimension = dimension
        self.price = price
        self.owner = owner
        self.freight_id = freight_id
        self.receiver_name = receiver_name
        self.group = group
