#!/usr/bin/python

from modules import text_analysis
import base64
import hexdump
import pprint

pp = pprint.PrettyPrinter()


b64text = open("prob6_data.txt").read()
cipherText = bytearray(base64.b64decode(b64text))
# cipherText = bytearray.fromhex("0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")
# ctLen = len(cipherText)

print(type(cipherText))
print(hexdump.hexdump(cipherText))
keyNormHamDist = []
for keysize in range(1,40):
	hamDist = text_analysis.stringBitwiseHammingDist(cipherText[0:keysize],cipherText[keysize:(2*keysize)])
	normHamDist = hamDist/keysize
	keyNormHamDist.append((keysize,normHamDist))



sortedLowHD = sorted(keyNormHamDist, key=lambda tup: tup[1])
pp.pprint(sortedLowHD)

# we now have the 4 most likely key lengths
# iterate over these keylengths and perform the transposition of blocks
# for each keylength we want to create a list, with the position equal to the char position in the prospective key

# remember, the purpose is to find the keylength where the sum of the scores for each transposition is highest
# and also to keep a not of which charactersin which position resulted in the highest score

# at the end, want to show for each keylength:
# the length value,
# the key value (so, all characters of the winning key, in order) 
# each transposed string as plaintext
# the un-transposed plaintext string
resultData = []
for i in range(0,4):
	
	keylen = sortedLowHD[i][0]
	resultData.append({})
	resultData[i] = {'keylen':keylen,'char':bytearray(),'highScore':0,'ptext':[]}
	# we now have the keylength we want to try
	transposeCT = []
	for k in range(0,keylen): transposeCT.append(bytearray())
	j = 0
	for el in cipherText:
		transposeCT[(j%keylen)].append(el)
		j += 1


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
	# strlen= 60
	# klen = 3
	# str 0 pos 0
	# str 1 pos 0
	# str 2 pos 0
	# str 0 pos 1
	for z in range(0, ( len(transposeCT[0])-1) ):
		for q in range(0,keylen):
			rcptext.append(resultData[i]['ptext'][q][z])
	resultData[i]['recombinedPtext'] = rcptext 

pp.pprint(resultData)