__author__ = 'shahryar_slg'

from move_it import db

class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)


class Address(db.Model):

    def __init__(self, country, city, rest_of_address, zipcode):
        self.country = country
        self.city = city
        self.rest_of_address = rest_of_address
        self.zipcode = zipcode


    def __str__(self):
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
    def __init__(self, name, weight, destination, pickup_address, dimension, price, customer_name, receiver_name, id):
        self.name=name
        self.weight=weight
        self.destination=destination
        self.pickup_address=pickup_address
        self.dimension=dimension
        self.price=price
        self.customer_name=customer_name
        self.id=id
        self.receiver_name=receiver_name
