# -*- encoding: utf-8 -*-
'''
@File    :   server.py
@Time    :   2025/03/20 12:25:03
@Author  :   LamentXU 
'''
import random 
print('----Welcome to my division calc----')
print('''
menu:
      [1]  Division calc
      [2]  Get flag
''')
while True:
    choose = input(': >>> ')
    if choose == '1':
        try:
            denominator = int(input('input the denominator: >>> '))
        except:
            print('INPUT NUMBERS')
            continue
        nominator = random.getrandbits(32)
        if denominator == '0':
            print('NO YOU DONT')
            continue
        else:
            print(f'{nominator}//{denominator} = {nominator//denominator}')
    elif choose == '2':
        try:
            ans = input('input the answer: >>> ')
            rand1 = random.getrandbits(11000)
            rand2 = random.getrandbits(10000)
            correct_ans = rand1 // rand2
            if correct_ans == int(ans):
                print('WOW')
                with open('flag', 'r') as f:
                    print(f'Here is your flag: {f.read()}')
            else:
                print(f'NOPE, the correct answer is {correct_ans}')
        except:
            print('INPUT NUMBERS')
    else:
        print('Invalid choice')