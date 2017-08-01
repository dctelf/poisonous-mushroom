#!/usr/bin/python

from cryptochallenge import hex_to_b64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.backends import default_backend  # http://cryptography.io


lines = open("prob8_data.txt").readlines()

for line in lines:
	line = line.rstrip('\n')
	valueBA = hex_to_b64.hexStringToByteArray(line)
#	valueBA = bytearray.fromhex(line.rstrip('\n'))

	numBytes = len(valueBA)
	numBlocks = int(numBytes/16)

	for blockIndex in range(0,(numBlocks)):
		# we want to compare the block starting at the index with all subsequent blocks
		initBlockStartPos = blockIndex * 16
		initBlockEndPos = initBlockStartPos + 16
		initBlock = valueBA[initBlockStartPos:initBlockEndPos]

		for subsequentBlockIndex in range((blockIndex+1), (numBlocks)):
			testBlockStartPos = subsequentBlockIndex * 16
			testBlockEndPos = testBlockStartPos + 16
			#
			if(initBlock == valueBA[testBlockStartPos:testBlockEndPos]): 
				print("got it")
				print("[{0}:{1}] to [{2}:{3}]".format(initBlockStartPos, initBlockEndPos, testBlockStartPos, testBlockEndPos))
				print("{0} == {1}".format(initBlock, valueBA[testBlockStartPos:testBlockEndPos]))
				# try decrypting the line with YELLOW SUBMARINE
				key = b'YELLOW SUBMARINE'
				backend = default_backend()
				cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
				decryptor = cipher.decryptor()
				decoded = decryptor.update(bytes(valueBA)) + decryptor.finalize()
				print(decoded)

				print(line)

				