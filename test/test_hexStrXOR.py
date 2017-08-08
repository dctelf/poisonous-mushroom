from unittest import TestCase
from cryptochallenge import stringmanip



class TestHexStrXOR(TestCase):
    def test_hexStrXOR(self):
        str_a = "1c0111001f010100061a024b53535009181c"
        str_b = "686974207468652062756c6c277320657965"

        result_str = stringmanip.hexStrXOR(str_a, str_b)
        print("XOR result: ", result_str)
        expected_str = "746865206b696420646f6e277420706c6179"
        print("expected result: ", expected_str)
        self.assertEqual(expected_str, result_str)
