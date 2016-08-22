__author__ = 'shahryar_slg'


class Address:

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
                          rest_of_address = rod,
                          zipcode=words_of_address[-1]
                          )
        return address
