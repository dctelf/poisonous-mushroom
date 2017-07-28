from unittest import TestCase
from modules import hex_to_b64

class TestHexStringToByteArray(TestCase):
    def test_hexStringToByteArray(self):
        self.assertEqual(hex_to_b64.hexStringToByteArray(""), "abc123")
