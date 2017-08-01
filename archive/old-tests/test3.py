#/usr/bin/python

from cryptochallenge import xor
from cryptochallenge import hex_to_b64
from cryptochallenge import text_analysis
import hexdump
import codecs


encodedHexString = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

print("encodedHexString decoded: {0}".format(codecs.decode(encodedHexString,"hex")))

# turn hex string into byte array of ascii it represents
# loop through `keys`
	# loop through and xor byte by byte
	# score entire byte array

bytearrayRepr = hex_to_b64.hexStringToByteArray(encodedHexString)
print(bytearrayRepr)
highScore = 0
for i in range(0,255):
	testByteArray = bytearray()
	for x in bytearrayRepr:
		testByteArray.append(i ^ x)
	score = text_analysis.latinAlphaTextScore(testByteArray)
	if(score > highScore):
		highScore = score
		winningKey = i
		winningPlainText = testByteArray
	print("test key: {0}".format(i))
	print("score: {0}".format(score))
	print("resultant string: {0}".format(testByteArray))
	print("resultant string type: {0}".format(type(testByteArray)))

print("winning key: {0}".format(winningKey))
print("winning score: {0}".format(highScore))
print("winning plain text: {0}".format(winningPlainText))

