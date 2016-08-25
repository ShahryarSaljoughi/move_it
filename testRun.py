__author__ = 'shahryar_slg'
import models
from routes import db
from initialize_db import courier
from initialize_db import customer
from initialize_db import courier

pegah = models.User('pegah_fth','456321','pegah.fateh@gmail.com', role=customer, phonenumber=989127401672)
db.session.add(pegah)


dims = models.Dimension(12, 12, 12)
dest = models.DestinationAddress('iran', 'zanjan',
                                 'misaq 17pelake 4015',
                                 123856, freight_id=13)
pickAddr = models.PickupAddress('iran', 'tehran',
                                'dehkade olympics', 8965,
                                freight_id=13)

fr = models.Freight('sofa', '6', destination=dest,
                    pickup_address=pickAddr,
                    dimension=dims, price= 12354,
                    owner=pegah.id, receiver_name='siamak')

pegah.freights.append(fr)

db.session.add(dest)
db.session.add(pickAddr)
db.session.add(fr)

db.session.commit()
