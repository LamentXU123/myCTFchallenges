# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2025/03/29 15:52:17
@Author  :   LamentXU 
'''
import bottle
'''
flag in /flag
'''
@bottle.route('/')
def index():
    return 'Hello, World!'
blacklist = [
    'o', '\\', '\r', '\n', 'import', 'eval', 'exec', 'system', ' ', ';' , 'read'
]
@bottle.route('/attack')
def attack():
    payload = bottle.request.query.get('payload')
    if payload and len(payload) < 25 and all(c not in payload for c in blacklist):
        print(payload)
        return bottle.template('hello '+payload)
    else:
        bottle.abort(400, 'Invalid payload')
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=5000)