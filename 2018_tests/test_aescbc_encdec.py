from unittest import TestCase
from cryptochallenge import stringmanip, ciphers


class TestAescbc_encdec(TestCase):
    def test_aesecbcdc_fullcycle(self):

        ptext_str = "ABCDEFGHIJKLMNOP0A0B0C0D0E0F0G0H"
        ptext_ba = bytearray(ptext_str, 'utf-8')
        test_key = bytearray("YELLOW SUBMARINE", 'utf-8')
        test_iv = bytearray(16)
        ctext = ciphers.my_ba_aes_cbc128_enc(ptext_ba, test_key, test_iv)
        print("cipher text;", ctext)
        reverse_ptext = ciphers.my_ba_aes_cbc128_dec(ctext, test_key, test_iv)
        print("reversed;", reverse_ptext)
        self.assertEqual(ptext_ba, reverse_ptext)
