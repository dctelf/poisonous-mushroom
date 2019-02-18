from unittest import TestCase
import string
import random
from cryptochallenge import stringmanip
import codecs

class TestBytearrayToBase64(TestCase):

    def test_problemString(self):
        challenge_hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        print("challenge hex", challenge_hex)

        std_byte_conv = bytearray.fromhex(challenge_hex)
        print("std conv bytearray", std_byte_conv)

        expected_str = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        print("expected str", expected_str)

        conv_str = stringmanip.bytearrayToBase64(std_byte_conv)

        self.assertEqual(expected_str, conv_str)

    def test_singleChar(self):
        test_characters = string.digits + string.ascii_lowercase[:6]
        for j in test_characters:
            test_str = "0" + j
            ba = bytearray.fromhex(test_str)
            conv_str = stringmanip.bytearrayToBase64(ba)
            expected_str = codecs.encode(codecs.decode(test_str, 'hex'), 'base64').decode()

            expected_str = expected_str.rstrip()

            self.assertEqual(conv_str, expected_str)

    def test_randomString(self):
        for i in range(1, 100):
            # bit of an odd one this....  our conversion handles odd numbers of characters
            # but the bytearray.fromhex method appears to fall to bits on the last character if there
            # is an odd number of elements, so ensure the random hex string length is a multiple of 2

            test_string_len = random.randint(1,50)*2

            rand_hex_str = (''.join(random.choice(string.hexdigits) for i in range(test_string_len))).lower()
            print("testing: ", rand_hex_str)
            ba = bytearray.fromhex(rand_hex_str)

            expected_str = codecs.encode(codecs.decode(rand_hex_str, 'hex'), 'base64').decode()
            expected_str = expected_str.rstrip()
            print("expected b64: ", expected_str)

            conv_str = stringmanip.bytearrayToBase64(ba)
            print("conv str:  ", conv_str)

            self.assertEqual(expected_str, conv_str)

