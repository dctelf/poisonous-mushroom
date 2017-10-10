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

    def test_ba_pkcs7_unpad(self):

        test_str = "abc123"
        test_ba = bytearray(test_str, 'utf-8')
        blocklen =6
        print(test_ba)
        result_ba = stringmanip.ba_pkcs7_pad(test_ba, blocklen)
        print(result_ba)
        unpad_ba = stringmanip.ba_pkcs7_remove(result_ba, blocklen)
        print(unpad_ba)
        self.assertEqual(test_ba, unpad_ba)

