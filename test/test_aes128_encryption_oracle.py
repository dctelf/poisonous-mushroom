from unittest import TestCase
from cryptochallenge import ciphers

class TestAes128_encryption_oracle(TestCase):
    def test_aes128_encryption_oracle(self):
        test_ptext = bytearray("some random test text (whose length is not that important) to pass to the encryption Oracle - w00t!", 'utf-8')
        for i in range(100):
            ctext = ciphers.aes128_encryption_oracle(test_ptext)
            print(ctext)

        self.assertEqual("A", "A")

    def test_detect_aes128_ecbcbc(self):
        ciphers.detect_aes128_ecbcbc()