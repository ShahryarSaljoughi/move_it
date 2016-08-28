__author__ = 'shahryar_slg'
from app import models
from app.main.views import db


def main():
    shahryar = models.User(username='sh_slg',password='852369',email='s.shahryar75@gmail.com', role_id='2', phonenumber=989127401672)



    dims = models.Dimension(12, 12, 12)

    #dest = models.DestinationAddress('iran', 'zanjan',
    #                                'misaq 17pelake 4015',
    #                                 123856, freight_id=13)

    #pickAddr = models.PickupAddress('iran', 'tehran',
    #                                'dehkade olympics', 8965,
    #                                freight_id=13)

    dest = models.DestinationAddress(country='iran', city='zanjan',
                                    rest_of_address='misaq 17pelake 4015',
                                     postal_code=123856)

    pickAddr = models.PickupAddress(country='iran', city='zanjan',
                                    rest_of_address='shahrek e karmandan faz e 2', postal_code= 8569721)


    fr = models.Freight(name='sofa', width=dims.width, height=dims.height, receiver_name='ali reza sanaee')
    fr.destination.append(dest)
    fr.pickup_address.append(pickAddr)
    shahryar.freights.append(fr)

    db.session.add(dest)
    db.session.add(pickAddr)
    db.session.add(fr)
    db.session.add(shahryar)

    db.session.commit()

    print shahryar.role.title

if __name__ == '__main__':
    main()