from unittest import TestCase
import string
import random
from cryptochallenge import stringmanip
import codecs

class TestHexStringToBase64(TestCase):

    def test_problemString(self):
        challenge_hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        print("challenge hex", challenge_hex)

        converted_str = stringmanip.hexToBase64(challenge_hex)
        print("converted base64", converted_str)

        expected_str = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        print("expected str", expected_str)

        self.assertEqual(expected_str, converted_str)


    def test_randomString(self):
        for i in range(1, 100):
            # bit of an odd one this....  our conversion handles odd numbers of characters
            # but the bytearray.fromhex method appears to fall to bits on the last character if there
            # is an odd number of elements, so ensure the random hex string length is a multiple of 2

            test_string_len = random.randint(1,50)*2

            rand_hex_str = (''.join(random.choice(string.hexdigits) for i in range(test_string_len))).lower()
            print("testing: ",rand_hex_str)

            conv_str = stringmanip.hexToBase64(rand_hex_str)
            print("conv str: ", conv_str)

            expected_str = codecs.encode(codecs.decode(rand_hex_str, 'hex'), 'base64').decode()
            expected_str = expected_str.rstrip()
            print("expected str: ", expected_str)

            self.assertEqual(expected_str, conv_str)
