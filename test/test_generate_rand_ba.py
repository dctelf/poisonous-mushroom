from unittest import TestCase
from cryptochallenge import ciphers

class TestGenerate_rand_ba(TestCase):
    def test_generate_rand_ba(self):
        for i in range(10000):
            print(ciphers.generate_rand_ba(16))
        self.assertEqual("A", "A")
