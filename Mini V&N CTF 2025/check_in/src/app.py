'''
I wish you a good head start.
flag is in file namely 'flag' in the same directory as this file.

Good luck!
'''

import re
import flask
import requests
import ipaddress
from urllib.parse import urlparse

GENERAL_WAF_REGEX = r'[a-zA-Z0-9_\[\]{}()<>,.!@#$^&*]{3}' # only two of these characters ;)

app = flask.Flask(__name__)

def general_waf(code):
    # Why do you need so many characters?
    if re.findall(GENERAL_WAF_REGEX, code):
        return True
    else:
        return False

def check_hostname(url):
    # must starts with vnctf.
    if not url.startswith('http://vnctf.'):
        return False

    hostname = urlparse(url).hostname
    query = urlparse(url).query

    # must only contain two of the restricted characters
    if general_waf(query):
        return False

    # must not be an ip address, so no 127.0.0.1 or ::1
    try:
        ipaddress.ip_address(hostname)
        return False
    except ValueError:
        pass

    return url

@app.route('/')
def index():
    return 'Welcome to MINI VNCTF 2025!'

@app.route('/fetch')
def fetch():
    url = flask.request.args.get('url')
    safe_url = check_hostname(url)
    if safe_url:
        try:
            response = requests.get(safe_url, allow_redirects=False) # no redirects
            return response.text
        except:
            return 'Error'
    else:
        return 'Invalid URL'

@app.route('/__internal/safe_eval')
def safe_eval():
    # check if the request is from the internal network
    if flask.request.remote_addr not in ['127.0.0.1', '::1']:
        return 'Forbidden'

    code = flask.request.args.get('hi')

    if len(code) >= 24 * 10 + 8 * 8:
        # Man! What can I say. 
        return 'Invalid code'

    # Ah, if you get here, then your final challenge is to break this jail.
    # Try it. Not as hard as it seems ;)
    blacklist = ['\\x','+','join', '"', "'", '[', ']', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in blacklist:
        if i in code:
            return 'Invalid code'
    
    safe_globals = {'__builtins__':None, 'lit':list, 'dic':dict}

    return repr(eval(code, safe_globals))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)


    

    