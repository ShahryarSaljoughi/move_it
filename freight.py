__author__ = 'shahryar_slg'

class Dimension:

    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth


class Freight :
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

