from pwn import *
from randcrack import RandCrack
from tqdm import tqdm
# context.log_level = 'debug'
rc = RandCrack()
p = remote('gz.imxbt.cn',20261)
# p = process(['python', 'server.py'])
p.recvuntil(b'flag')
for i in tqdm(range(624)):
    p.sendline(b'1')
    p.sendlineafter(b'>>> ',b'1')
    rand = p.recvline().decode().split('=')[-1]
    rand = rand.replace(' ', '')
    rc.submit(int(rand))
p.sendline(b'2')
rand1 = rc.predict_getrandbits(11000)
rand2 = rc.predict_getrandbits(10000)
print(rand1//rand2)
p.recvuntil(b'>>> ')
p.sendline(str(rand1//rand2).encode())
p.interactive()