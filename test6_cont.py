#!/usr/bin/python

from modules import text_analysis
from modules import xor
import base64
import hexdump
import pprint
import os

pp = pprint.PrettyPrinter()

# plainText = bytearray("How much is that doggy in the window, the one with the waggly tail?  How much is that doggy in the window, I do hope that doggy's for sale...", 'utf-8')

'''
# for keylengths 2 to 22
# generate 100 keys and encrypt then HD test each ciphertex
for l in range(2,21):
	winCount = 0
	for i in range(1,100):
		key = bytearray(os.urandom(l))
		keylen = len(key)
		#print("keysize: {0}".format(keylen))

		hexCtext = xor.varLengthRKXOR(plainText, key)
		cipherText = bytearray.fromhex(hexCtext)
		
		sortedLowHD = text_analysis.mostLikelyXORKeyLen(cipherText, 1, 20)
		if( [item for item in sortedLowHD[:5] if item[0] == keylen] ): winCount += 1
		else: winCount -= 1
		#pp.pprint(sortedLowHD)
	print("keylen: {0}, winCount: {1}".format(l,winCount))

'''
'''				
key = bytearray('I*d&ddi&*gvJ','utf-8')


hexCtext = xor.varLengthRKXOR(plainText, key)
cipherText = bytearray.fromhex(hexCtext)
'''

b64text = open("prob6_data.txt").read()
cipherText = bytearray(base64.b64decode(b64text))

ctLen = len(cipherText)

sortedLowHD = text_analysis.mostLikelyXORKeyLen(cipherText, 1, 41)


# the 5 lowest keylength scores are worth taking into the loop
resultData = []
for i in range(0,5):
	
	keylen = sortedLowHD[i][0]
	resultData.append({})
	resultData[i] = {'keylen':keylen,'char':bytearray(),'highScore':0,'ptext':[]}
	# we now have the keylength we want to try
	transposeCT = text_analysis.transposeOverLength(cipherText,keylen)
	

	# we now have, on each pass for the different most likely keylengths,
	# a list of keylength length,transposing the ciphertext by each char

	# we can now treat each of these individual transposed strings as something encrypted by a single byte
	# xor cipher
	for j in range(0,keylen):
		highScore = 0		
		for l in range(0,255):
			testByteArray = bytearray()
			for x in transposeCT[j]:
				testByteArray.append(l ^ x)
			score = text_analysis.latinAlphaTextScore(testByteArray)/(len(transposeCT[j]))
			if(score > highScore):
				highScore = score
				winningKey = l
				winningPlainText = testByteArray
				winningCipherText = transposeCT
		resultData[i]['char'].append(winningKey)
		resultData[i]['highScore'] = highScore
		resultData[i]['ptext'].append(winningPlainText)
	rcptext = bytearray()

	# rghhh... if ptext is not integer multiple of keylen then some of the transposed plaintext strings will be shorter than [0]
	# need to find a better way to iterate over these and recombine

	
	for z in range(0, ( len(transposeCT[0]) -1 ) ):
		for q in range(0,keylen):
			rcptext.append(resultData[i]['ptext'][q][z])
	resultData[i]['recombinedPtext'] = rcptext



pp.pprint(sorted(resultData, key=lambda key: key["highScore"])) 