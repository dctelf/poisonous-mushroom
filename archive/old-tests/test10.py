#!/usr/bin/python


from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.backends import default_backend  # http://cryptography.io

from cryptochallenge import hex_to_b64
from cryptochallenge import myAES
from cryptochallenge import padding
import os
import hexdump

# on thinking about this - mutable strings are a bad idea in the wider sense
# any function that uses mutable strings in loops for efficiency should
# copy to a bytearray in the first instance, otherwise a string is a string
'''
iv = b'0000000000000000'
key = b'YELLOW SUBMARINE'
ptextBlock = b'SOME 16 CHARS'
'''
iv = bytearray('0000000000000000','utf-8')
key = bytearray('YELLOW SUBMARINE','utf-8')
ptextBlock = bytearray('SOME 16 CHARS','utf-8')


print(hexdump.hexdump(iv))
print(hexdump.hexdump(key))





print(hexdump.hexdump(myAES.AES_CBCmode_encrypt(iv, key, ptextBlock)))

