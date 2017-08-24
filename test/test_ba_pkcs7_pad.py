from unittest import TestCase
from cryptochallenge import stringmanip



class TestBa_pkcs7_pad(TestCase):
    def test_ba_pkcs7_pad(self):

        test_str = "YELLOW SUBMARINE"
        test_ba = bytearray(test_str, 'utf-8')
        pad_len = 20


        result_ba = stringmanip.ba_pkcs7_pad(test_ba, pad_len)

        print(result_ba)

        expected_ba = bytearray("YELLOW SUBMARINE\x04\x04\x04\x04", 'utf-8')

        self.assertEqual(expected_ba, result_ba)
