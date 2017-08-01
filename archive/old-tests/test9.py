#!/usr/bin/python

from cryptochallenge import padding

inputBA = bytearray("YELLOW SUBMARINEYELLOW SUBMARINEYELLOW SUBMARINE",'utf-8')
blockLen = 17
padded = padding.PKCS7_pad(inputBA, blockLen)

print(padded)