#/usr/bin/python

from modules import xor
from modules import hex_to_b64
import hexdump
import codecs


firstHexString = '1c0111001f010100061a024b53535009181c'
secondHexString = '686974207468652062756c6c277320657965'
print("firstHexString decoded: {0}".format(codecs.decode(firstHexString,"hex")))
print("secondHexString decoded: {0}".format(codecs.decode(secondHexString,"hex")))
expectedResult = '746865206b696420646f6e277420706c6179'


result = xor.hexStringXOR(firstHexString, secondHexString)

print("my result decoded: {0}".format(codecs.decode(result,"hex")))
print("expected result decoded: {0}".format(codecs.decode(expectedResult,"hex")))


if(result == expectedResult): print("test passed: w00t!")
else: print("abject failure")