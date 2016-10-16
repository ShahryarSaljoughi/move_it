__author__ = 'panizava'
import random
import string
from datetime import datetime
from app.models import  Freight,User
from app import db

freights = list()
for i in range(1000):

    a_freight = Freight()
    a_freight.name=''.join(random.choice(string.ascii_letters) for j in range(15))
    a_freight.height = random.random()
    a_freight.width = random.random()
    a_freight.depth = random.random()
    a_freight.receiver_name = "Andrew Ng"
    a_freight.receiver_phonenumber = "09127401672"
    a_freight.weight = random.randint(0, 500)
    a_freight.description = ''.join(random.choice(string.ascii_letters) for j in range(15))
    a_freight.creation_data = datetime(year=random.randint(2014, 2016),
                                       month=random.randint(1, 12),
                                       day=random.randint(1, 30),
                                       hour=random.randint(0, 23),
                                       minute=random.randint(0, 58))

    users=User.query.all()
    a_user = random.choice(users)
    a_user.freights.append(a_freight)
    db.session.add(a_freight)
    db.session.commit()

