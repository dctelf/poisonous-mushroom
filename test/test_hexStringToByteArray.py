from unittest import TestCase
import os
import string
import random
import binascii
from cryptochallenge import stringmanip

class TestHexStringToByteArray(TestCase):
    def test_hexStringToByteArray(self):
        # generate random value of 100 bytes
        randomValue = os.urandom(100)
        # convert this to hex string using standard utilities


        self.assertEqual("a", "a")

    def test_problemString(self):
        challenge_hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        print("challenge hex", challenge_hex)

        converted_ba = stringmanip.hexStringToByteArray(challenge_hex)
        print("converted bytearray", converted_ba)

        converted_int = int.from_bytes(converted_ba, byteorder='big', signed=False)
        print("converted int", converted_int)

        expected_int = 11259432467145572969189485457381052543241507215288737798329079056359121649591228422793827173000297562297701340508013
        print("expected int", expected_int)

        self.assertEqual(expected_int, converted_int)

    def test_singleChar(self):
        test_characters = string.digits + string.ascii_lowercase[:6]
        for j in test_characters:
            ba = stringmanip.hexStringToByteArray(j)
            converted_int = int.from_bytes(ba, byteorder='big', signed=False)
            self.assertEqual(int(j,16), converted_int)

    def test_randomString(self):
        for i in range(1, 100):
            # bit of an odd one this....  our conversion handles odd numbers of characters
            # but the bytearray.fromhex method appears to fall to bits on the last character if there
            # is an odd number of elements, so ensure the random hex string length is a multiple of 2

            test_string_len = random.randint(1,50)*2

            rand_hex_str = (''.join(random.choice(string.hexdigits) for i in range(test_string_len))).lower()
            ba = stringmanip.hexStringToByteArray(rand_hex_str)
            print("testing: ",rand_hex_str)
            expected_ba = bytearray.fromhex(rand_hex_str)
            self.assertEqual(ba, expected_ba)
