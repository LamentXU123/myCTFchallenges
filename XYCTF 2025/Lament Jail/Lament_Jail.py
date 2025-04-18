# -*- coding:utf-8 -*-
# @FileName  :Lament_Jail.py
# @Time      :2025/3/22 12:37:43
# @Author    :LamentXU
from socket import *
from os import remove
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from zlib import compress, decompress
from uuid import uuid4
from json import dumps
from subprocess import Popen, PIPE
'''
Definate all the errors
'''
class MessageLengthError(Exception):
    def __init__(self, message) -> None:
        self.message = message

class PasswordError(Exception):
    def __init__(self, message) -> None:
        self.message = message
class SimpleTCP():
    '''
    The main class when using TCP
    '''

    def __init__(self, family: AddressFamily = AF_INET, type: SocketKind = SOCK_STREAM
                 , proto: int = -1, fileno: int = None, is_encrypted: bool = True, AES_key: bytes = None, password: bytes = None) -> None:
        '''
        is_encrypted: use encrypted connection, only for server
        AES_key: use a fixed AES_key, None for random, must be 16 bytes, only for server
        password: A fixed password is acquired from the client (must smaller than be 100 bytes), if wrong, the connection will be closed
            if password is set in server, every time a client connect, the client must send the same password back to the server to accept.
            if password is set in client, every time you connect to the server, the password will be sent to the server to verify.
            if password is None, no password will be used.
        self.Default_message_len: if in encrypted mode, the value must be a multiple of self.BLOCK_SIZE
        MAKE SURE THE DEFAULT_MESSAGE_LEN OF BOTH SERVER AND CLIENT ARE SAME, Or it could be a hassle
        '''
        
        self.BLOCK_SIZE = 16 # block size of padding text which will be encrypted by AES
        # the block size must be a mutiple of 8
        self.default_encoder = 'utf8'  # the default encoder used in send and recv when the message is not bytes
        if is_encrypted:
            if AES_key == None:
                self.key = get_random_bytes(16)  # generate 16 bytes AES code
            else:
                self.key = AES_key #TODO check the input 
            self.cipher_aes = AES.new(self.key, AES.MODE_ECB)
        else:
            self.key, self.cipher_aes = None, None
        self.default_message_len = 1024 # length of some basic message, it's best not to go below 1024 bytes
        if password == None:
            self.password = None
        else:
            self.password = self.turn_to_bytes(password)
            if len(password) > 100:
                raise ValueError('The password is too long, it must be smaller than 100 bytes')
        self.s = socket(family, type, proto, fileno)  # main socket
    def accept(self) -> tuple:
        '''
        Accept with information exchange and key exchange, return the address of the client
        if the password from client is wrong or not set, raise PasswordError
        '''
        self.s, address = self.s.accept()
        if self.key == None:
            is_encrypted = False
        else:
            is_encrypted = True
        if self.password == None:
            has_password = False
        else:
            has_password = True
        info_dict = {
            'is_encrypted' : is_encrypted,
            'has_password' : has_password}
        info_dict = dumps(info_dict).encode(encoding=self.default_encoder)
        self.s.send(self.turn_to_bytes(len(info_dict)))
        self.s.send(info_dict)
        if has_password:
            password_length = self.unpadding_packets(self.s.recv(3), -1)
            if not password_length:
                self.s.close()
                raise PasswordError(f'The client {address} does not send the password, the connection will be closed')
            recv_password = self.s.recv(int(password_length.decode(encoding=self.default_encoder))) # the first byte is whether the password is aquired(1) or not(0), the rest is the password, the password is padded to 100 bytes
            if recv_password != self.password or recv_password[0] == b'0':
                self.s.send(b'0')
                self.s.close()
                raise PasswordError(f'The password {recv_password} is wrong, the connection from {address} will be closed, you can restart the accept() function or put it in a while loop to keep accepting')
            else:
                self.s.send(b'1')
        if is_encrypted:
            public_key = self.s.recv(450)
            rsa_public_key = RSA.import_key(public_key)
            cipher_rsa = PKCS1_OAEP.new(rsa_public_key)
            encrypted_aes_key = cipher_rsa.encrypt(self.key)
            self.s.send(encrypted_aes_key)
        # TODO
        return address
    def turn_to_bytes(self, message) -> bytes:
        '''
        Turn str, int, etc. to bytes using {self.default_encoder}
        '''
        type_of_message = type(message)
        if type_of_message == str:
            try:
                message = message.encode(encoding=self.default_encoder)
            except Exception as e:
                raise TypeError(
                    'Unexpected type "{}" of {} when encode it with {}, raw traceback: {}'.format(type_of_message, message, self.default_encoder, e))
        elif type_of_message == bytes:
            pass
        else:
            try:
                message = str(message).encode(encoding=self.default_encoder)
            except:
                raise TypeError(
                    'Unexpected type "{}" of {}'.format(type_of_message, message))
        return message
    def unpadding_packets(self, data: bytes, pad_num: int) -> bytes:
        '''
        Delete the blank bytes at the back of the message
        pad_num : number of the blank bytes
        pad_num = -1, delete all the blank bytes the the back(or use .rstrip() directly is ok)
        '''
        if pad_num == -1:
            data = data.rstrip()
        else:
            while pad_num > 0 and data[-1:] == b' ':
                data = data[:-1]
                pad_num -= 1
        return data
    def padding_packets(self, message: bytes, target_length: int = None) -> tuple:
        '''
        Pad the packet to {target_length} bytes with b' ', used in not-encrypted mode
        The packet must be smaller then {target_length}
        target_length = None : use self.default_message_len
        '''
        message = self.turn_to_bytes(message)
        if target_length == None:
            target_length = self.default_message_len
        if len(message) > target_length:
            raise MessageLengthError(
                'the length {} bytes of the message is bigger than {} bytes, please use self.send_large_small and self.recv instead'.format(str(len(message)), target_length))
        pad_num = target_length-len(message)
        message += b' ' * pad_num
        return (message, pad_num)
    def pad_packets_to_mutiple(self, data: bytes, block_size: int == None) -> bytes:
        '''
        Pad the data to make the length of it become a mutiple of Blocksize, used in encrypted mode
        target_length = None : use self.BLOCK_SIZE
        '''
        padding_length = block_size - (len(data) % block_size)
        if padding_length == 0:
            padding_length = block_size
        padding = bytes([padding_length]) * padding_length
        padded_data = data + padding
        return padded_data
    def send_large(self, message) -> None:
        '''
        Send message with the socket
        can accept bytes, str, int, etc.
        every non-bytes message will be encoded with self.default_encoder
        Every packet is forced to be filled to {self.default_message_len} bytes
        '''
        message = self.turn_to_bytes(message)
        message = compress(message)
        message_list = [message[i:i + self.default_message_len]
                        for i in range(0, len(message), self.default_message_len)]
        message_list_len = len(message_list)
        self._send(self.padding_packets(
            self.turn_to_bytes(message_list_len))[0])
        message_index = 0
        for message in message_list:
            message_padded = self.padding_packets(message)
            message = message_padded[0]
            self._send(message)
            message_index += 1
            if message_index == message_list_len:
                pad_num = message_padded[1]
                self._send(self.padding_packets(
                    self.turn_to_bytes(str(pad_num)))[0])

    def send(self, message) -> None:
        '''
        Send a message with the socket
        can accept bytes, str, int, etc.
        The data should not be larger than 9999 bytes
        It can be used at any time 
        Use self.send_large and recv_large if you want to send a big message
        '''
        message = self.turn_to_bytes(message)
        try:
            message_len = self.padding_packets(
                self.turn_to_bytes(len(message)), target_length=4)[0]
        except MessageLengthError:
            raise MessageLengthError(
                'The length of message is longer than 9999 bytes({} bytes), please use send_large instead'.format(str(len(message))))
        self._send(message_len)
        self._send(message)


    def _send(self, message: bytes) -> None:
        '''
        The basic method to encrypt and send data 
        MUST BE A MUTIPLE OF THE BLOCK SIZE IN ENCRYPTED MODE
        '''
        if self.cipher_aes != None:
            output_message = self.cipher_aes.encrypt(self.pad_packets_to_mutiple(message, self.BLOCK_SIZE))
            # plainmessage = unpad(self.cipher_aes.decrypt(output_message), self.BLOCK_SIZE)
        else:
            output_message = message
        self.s.send(output_message)  # The TCP mode


    def recvfile(self) -> bytes:
        '''
        Only receive file sent using self.send_largefile
        '''
        output = b''
        while True:
            a = self.recv_large(is_decode=False)
            if a != 'EOF'.encode(encoding=self.default_encoder):
                output += a
            else:
                break
        return output
    def recv_large(self, is_decode: bool = True):
        '''
        The return type can be bytes or string
        The method to recv message WHICH IS SENT BY self.send_large
        is_decode : decode the message with {self.default_encoder}
        '''
        message_listlen = self._recv(self.default_message_len).decode(
            encoding=self.default_encoder).rstrip()
        message_listlen = int(message_listlen)
        message = b''
        for i in range(0, message_listlen):
            mes = self._recv(self.default_message_len)
            if i == message_listlen - 1:
                mes_padnum = int(self._recv(self.default_message_len).decode(
                    encoding=self.default_encoder))
            else:
                mes_padnum = 0
            mes = self.unpadding_packets(mes, mes_padnum)
            message += mes
        message = decompress(message)
        if is_decode:
            message = message.decode(encoding=self.default_encoder)
        return message
    def _recv(self, length: int) -> bytes:
        '''
        The basic method to decrypt and recv data
        '''
        if self.cipher_aes != None:
            if length % 16 == 0:
                length += 16
            length = (length + self.BLOCK_SIZE-1) // self.BLOCK_SIZE * self.BLOCK_SIZE # round up to multiple of 16
            message = self.s.recv(length)
            message = self.cipher_aes.decrypt(message)
            message = self.unpad_packets_to_mutiple(message, self.BLOCK_SIZE)
        else:
            message = self.s.recv(length)
        return message
    def unpad_packets_to_mutiple(self, padded_data: bytes, block_size: int == None) -> bytes:
        '''
        Unpad the data to make the length of it become a mutiple of Blocksize, used in encrypted mode
        target_length = None : use self.BLOCK_SIZE
        '''
        if block_size == None:
            block_size = self.BLOCK_SIZE
        padding = padded_data[-1]
        if padding > block_size or any(byte != padding for byte in padded_data[-padding:]):
            raise ValueError("Invalid padding")
        return padded_data[:-padding]
    
def main():
    Sock = SimpleTCP(password='LetsLament')
    Sock.s.bind(('0.0.0.0', 13337))
    Sock.s.listen(5) 
    while True:
        _ = Sock.accept()     
        Sock.send('Hello, THE flag speaking.')
        Sock.send('I will not let you to control Lament Jail forever.')
        Sock.send('But, my friend LamentXU has to control it, as he will rescue me out of this jail.')
        Sock.send('So here is the pyJail I build. Only LamentXU knows how to break it.')    
        a = Sock.recvfile().decode()
        waf = '''
import sys
def audit_checker(event,args):
    if not 'id' in event:
    	raise RuntimeError
sys.addaudithook(audit_checker)

'''
        content = waf + a
        name = uuid4().hex+'.py'
        with open(name, 'w') as f:
            f.write(content)
        try:
            cmd = ["python3", name]
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            for line in iter(p.stdout.readline, b''):
                Sock.send(line.decode('utf-8').strip())
            p.wait()
            Sock.send('Done, BYE.')
        except:
            Sock.send('Error.')
        finally:
            Sock.s.close()
        remove(name)
if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            pass
