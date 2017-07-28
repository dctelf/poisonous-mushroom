#/usr/bin/python

from modules import xor
from modules import hex_to_b64
from modules import text_analysis
import hexdump
import codecs


#plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
#expectedCipherTextHex = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

plaintext = "repeat your key over this mofo!"
key = "KEYZZZ"



ptba = bytearray(plaintext, 'utf-8')
keyba = bytearray(key, 'utf-8')

ciphertextHex = xor.varLengthRKXOR(ptba, keyba)



print("plaintext: {0}".format(ptba))
print("key: {0}".format(keyba))
print("ciphertext: {0}".format(ciphertextHex))
#print("expected ct hex: {0}".format(expectedCipherTextHex))
#if(ciphertextHex == expectedCipherTextHex): print("test passed: w00t!")