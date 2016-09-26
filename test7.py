#!/usr/bin/python

import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.backends import default_backend  # http://cryptography.io
import base64

key = b'YELLOW SUBMARINE'
print("keylength in bits: {0}".format(len(key) * 8))



ctFile = open("prob7_data.txt").read()
cipherText = base64.b64decode(ctFile)

backend = default_backend()


cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)

decryptor = cipher.decryptor()
decoded = decryptor.update(cipherText) + decryptor.finalize()


print(decoded)


