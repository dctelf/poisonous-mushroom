from unittest import TestCase
import string
import random
from cryptochallenge import stringmanip, ciphers

class TestRepkeyXOR(TestCase):

    def test_repkeyXOR(self):

        plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
        key = "ICE"

        my_result = ciphers.repkeyXOR(plaintext, key)
        my_result_hex = stringmanip.bytearrayToHexStr(my_result)

        expected_ctext_hex = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

        self.assertEqual(my_result_hex, expected_ctext_hex)