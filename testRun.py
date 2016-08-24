__author__ = 'shahryar_slg'
import models
from routes import db

"""
user = models.User('sh_slg', '12346','s.shahryar75@gmail.com','custorme',989127401672)
dest = models.Address('iran', 'zanjan', 'misaq 17pelake 4015', 123856)
pickAddr = models.Address('iran', 'tehran', 'dehkade olympics', 8965)
dims = models.Dimension(12, 12, 12)
fr = models.Freight('sofa', '6', destination=dest, pickup_address=pickAddr,
                    dimension=dims, price= 12354, owner=4, receiver_name='siamak'
                    , freight_id=13, group='furniture')
db.session.add(user)
db.session.add(fr)
db.session.commit()
"""

users = models.User.query.all()
freights = users[0].freights

user = models.User('pegah_fth', '12346','pegah.fateh@icloud.com','custorme',989142850025)
db.session.add(user)
db.session.commit()

dims = models.Dimension(12, 12, 12)
dest = models.Address('iran', 'zanjan', 'misaq 17pelake 4015', 123856, freight_id=13)
pickAddr = models.Address('iran', 'tehran', 'dehkade olympics', 8965, freight_id=13)
fr = models.Freight('sofa', '6', destination=dest, pickup_address=pickAddr,
                    dimension=dims, price= 12354, owner=user.user_id, receiver_name='siamak'
                    , freight_id=13, group='furniture')

db.session.add(dest)
db.session.add(pickAddr)
db.session.add(fr)

db.session.commit()
