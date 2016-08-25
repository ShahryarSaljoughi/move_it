__author__ = 'shahryar_slg'


from routes import db


class role(db.Model):
    """
    this class is actually an Enum , used in users table
    """
    __tablename__ = 'role'

    seq = db.Column(db.INTEGER,primary_key=True)
    title = db.Column(db.TEXT, nullable=False)

    def __init__(self, title):
        self.title=title



class User(db.Model):  #there is a relationhsip between User and Freight : User is parent , Freight is child

    __tablename__='users'

    email = db.Column(db.TEXT,unique=True,
                      nullable=False)
    username = db.Column(db.TEXT, unique=True)
    password = db.Column(db.TEXT, nullable=False)
    # role = db.Column(db.ForeignKey('role.seq'))
    phonenumber = db.Column(db.INTEGER)
    id = db.Column(db.INTEGER, primary_key=True)
    # freights = db.relationship('Freight', backref='users', lazy='dynamic')
    freights = db.relationship('Freight',
                               backref=db.backref('freights'))

    role_id = db.Column(db.INTEGER, db.ForeignKey('role.seq'))
    role = db.relationship(role, backref=db.backref('users',
                                                    uselist=True,
                                                    cascade='delete,all'))
    """
    def __init__(self, username, password, email, role, phonenumber):
        self.email = email
        self.password = password
        self.role = role
        self.phonenumber = phonenumber
        self.username = username
    """
    def __repr__(self):
        return "user : " + str(self.username)
        #return "user : %s" str(self.username)



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

    __tablename__='freights'


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
    owner = db.Column(db.INTEGER,db.ForeignKey('users.id'))
    """
    def __init__(self, name, weight,
                 destination, pickup_address, dimension,
                 price, owner, receiver_name):
        self.name = name
        self.weight = weight
        self.destination = [destination]
        self.pickup_address = [pickup_address]
        # self.dimension = dimension
        self.height = dimension.height
        self.width = dimension.width
        self.depth = dimension.depth
        self.price = price
        self.owner = owner
        # self.id = freight_id
        self.receiver_name = receiver_name
    """
    def __repr__(self):
        return str(self.__dict__)

class PickupAddress(db.Model):

    __tablename__ = 'pickupAddresses'
    country=db.Column(db.TEXT)
    city=db.Column(db.TEXT)
    rest_of_address=db.Column(db.TEXT)
    postal_code=db.Column(db.INTEGER)
    id=db.Column(db.INTEGER,primary_key=True)
    # freights = db.relationship('Freight',backref='address',lazy='dynamic')
    freight_id = db.Column(db.INTEGER, db.ForeignKey('freights.id'))
    """
    def __init__(self, country, city, rest_of_address, zipcode, freight_id):
        self.country = country
        self.city = city
        self.rest_of_address = rest_of_address
        self.postal_code = zipcode
        self.freight_id=freight_id
   """
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


class DestinationAddress(db.Model):

    __tablename__ = 'destinationAddress'
    country=db.Column(db.TEXT)
    city=db.Column(db.TEXT)
    rest_of_address=db.Column(db.TEXT)
    postal_code=db.Column(db.INTEGER)
    id=db.Column(db.INTEGER,primary_key=True)
    # freights = db.relationship('Freight',backref='address',lazy='dynamic')
    freight_id = db.Column(db.INTEGER,db.ForeignKey('freights.id'))
    """
    def __init__(self, country, city, rest_of_address, zipcode, freight_id):
        self.country = country
        self.city = city
        self.rest_of_address = rest_of_address
        self.postal_code = zipcode
        self.freight_id=freight_id
   """
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

