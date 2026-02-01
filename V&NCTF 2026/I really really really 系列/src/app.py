# flag in /flag
import unicodedata

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output, code = '', ''
    if request.method == 'POST':
        try:
            code = request.form.get('code', '')
            if '＿' in code:
                raise Exception('Ahhh... I know what you want to do with "＿". It is pretty boarding stuff. Could you find some another character representing it?')
            if '︳' in code:
                raise Exception('Ahhh... I know what you want to do with "︳". It is pretty boarding stuff. Could you find some another character representing it?')
            unicode = unicodedata.normalize('NFKC', code)
            if 'getitem' in unicode:
                raise Exception('You cannot use "getitem", it will too easy for you i guess ;)')
            blacklist = ['__', '"', "'", '\\', '[', ']', ';', '{', '}', '1', '2', '3',
                         '4', '5', '6', '7', '8', '9', '0', 'def', 'class', 'lambda',
                         'builtins']
            for i in blacklist:
                if i in code:
                    raise Exception(f'Invalid code {i}')
            payload_l = code.split('\n')
            for i in payload_l:
                if len(i) >= 30:
                    raise Exception('Do not exceed 30 characters per line')
            exec(code, {'__builtins__': {}})
            output = 'Code executed successfully!'
        except Exception as e:
            output = e
    
    return render_template('index.html', output=output, code=code)

if __name__ == '__main__':
    app.run(debug=False, port=8081, host='0.0.0.0')
