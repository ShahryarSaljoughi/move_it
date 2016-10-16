__author__ = 'panizava'

from requests import post

codes = [608021, 761262, 985122, 101641, 611294, 344556, 518693, 138944, 957094, 576698]
header = {'Content-Type': 'application/json'}
for code in codes:
    response = post(
        url='http://127.0.0.1:5000/confirm_phonenumber',
        headers=header,
        json={
            "code": code
        }
    )
    print response.json()
