from unittest import TestCase
from cryptochallenge import config, ciphers

class TestAes128ecb_enc_oracle(TestCase):
    def test_aes128ecb_enc_oracle(self):
        config.oracle_enc_key = ciphers.generate_rand_ba(16)
        ba_ptext = bytearray(128)
        ctext = ciphers.aes128ecb_enc_oracle(ba_ptext)
        print(ctext)
        self.assertEqual("A", "A")

    def test_decryptSuffix(self):
        config.oracle_enc_key = ciphers.generate_rand_ba(16)

        # detect block size - valid AES options are: 128, 192 and 256  bits (16, 24 and 32 bytes respectively)
        # to check, generate a ptext string of 4 * the block len characters
        # encrypt the string with the ECB function
        # then identify whether the 2nd and 3rd block ciphertets are identical

        for blocklen in 32, 24, 16:
            test_block_ba = bytearray((4 * blocklen * "A"), 'utf-8')
            test_ctext = ciphers.aes128ecb_enc_oracle(test_block_ba)
            if test_ctext[blocklen:2*blocklen] == test_ctext[2*blocklen:3*blocklen]: break

        # this isn't working
        print(blocklen)





        for i in range(256):
            test_str = i * "A"
            ctext = ciphers.aes128ecb_enc_oracle(bytearray(test_str, 'utf-8'))



