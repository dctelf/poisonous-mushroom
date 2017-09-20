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
        blank_ctext = ciphers.aes128ecb_enc_oracle(bytearray())
        blank_ctlen = len(blank_ctext)

        # rather than do a while True and have it run off forever by accident, create a range up to 1000

        for i in range(1000):
            test_block_ba = bytearray(i * "A", 'utf-8')
            inc_ctext = ciphers.aes128ecb_enc_oracle(test_block_ba)
            if len(inc_ctext) != blank_ctlen:
                blocklen = len(inc_ctext) - blank_ctlen
                break

        # now detect ECB by creating ptext of 4 * blocklen

        test_ptext = bytearray(4 * blocklen * "A", 'utf-8')
        ctext = ciphers.aes128ecb_enc_oracle(test_ptext)
        if ctext[blocklen:2*blocklen] != ctext[2*blocklen:3*blocklen]: exit("not ecb mode")

        # need to create a data structure of prior blocks so we don't lose
        # the chain of identified characters as the prepend string shortens
        ## NOTE: as each ctext block is independent of each other, this entire sequence to derive a block
        ## can be iterated over for "ctextlen // blocklen", that is we can solve for a block at a time
        ## need to  be slightly cautious though as the full ctext len will flip +/- by 1 block
        ## as we prefix or suffix the prepend string of A's
        ##
        # ctext block will have been generated from ptext block of
        # (blocklen - 1)* "A" + ?
        # cyle across (blocklen - 1)* "A" + [0-255] and encrypt
        # find matching full block
        # we know unknown byte 0 is the result of the cycle - call this Q'
        #
        # next ctext block will have been generated from ptext block of
        # (blocklen - 2)* "A" + Q' + ?
        # cyle across (blocklen - 2)* "A" + Q' + [0-255] and encrypt
        # find matching full block
        # we know unknown byte 1 is the result of the cycle - call this Q''
        #
        # next ctext block will have been generated from ptext block of
        # (blocklen - 3)* "A" + Q' + Q'' + ?
        # cyle across (blocklen - 2)* "A" + Q' + Q'' + [0-255] and encrypt
        # find matching full block
        # we know unknown byte 2 is the result of the cycle - call this Q'''
        # etc.

        # so - here goes...
        # identify the number of blocks generated when calling the oracle with an empty string
        ptext_blocks = []
        num_ctext_blocks = blank_ctlen // blocklen
        # iterate over each block to solve
        for i in range(num_ctext_blocks):
            ptext = bytearray()
            # obtain the block to solve plus the subsequent block
            # NOTE: need to do someting later here - haven't handled the case for the last block
            blank_block = blank_ctext[i*blocklen:(i+1)*blocklen]

            # now iterate over the length of the block

            for j in range(blocklen):
                feedlen = blocklen - j - 1 - len(ptext)
                prepend_str = feedlen * "A"
                prepend_ba = bytearray(prepend_str, 'utf-8')
                prepend_ba += ptext
                test_prepend_ba = bytearray()
                test_prepend_ba[:] = prepend_ba[:]

                pullback_ctext = ciphers.aes128ecb_enc_oracle(prepend_ba)

                for k in range(255):
                    test_prepend_ba.append(k)
                    print(test_prepend_ba)
                    compare_ctext = ciphers.aes128ecb_enc_oracle(test_prepend_ba)
                    if compare_ctext[0:blocklen] == pullback_ctext[0:blocklen]:
                        ptext.append(k)
                        print(chr(k))
                        break

            ptext_blocks.append(ptext)