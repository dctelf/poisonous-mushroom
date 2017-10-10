#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from cryptochallenge import config, ciphers, stringmanip


def main():
    # initialise the global encryption key for all operations in this run
    config.oracle_enc_key = ciphers.generate_rand_ba(16)

    # call the oracle with an empty byte array, i.e. get only the ciphertext of the unknown suffix back
    blank_ctext = ciphers.aes128ecb_enc_oracle(bytearray())
    blank_ctlen = len(blank_ctext)


    # nudge an ever lengthening string of "A"'s into the oracle
    # at some length of "A"'s the oracle function will snap into another block
    # the moment this happens, we take the diference in lengths to determine what the marginal increase
    # in length of ctext is.
    # this difference is the blocklength of the oracle function
    #
    # (rather than do a while True and have it run off forever by accident, create a range up to 1000)

    for i in range(1000):
        test_block_ba = bytearray(i * "A", 'utf-8')
        inc_ctext = ciphers.aes128ecb_enc_oracle(test_block_ba)
        if len(inc_ctext) != blank_ctlen:
            blocklen = len(inc_ctext) - blank_ctlen
            break

    # now detect ECB by creating ptext of 4 * blocklen
    # "4 *" used to avoid any pre or post padding of the plaintext passed (assumes any padding does not extend
    # beyond a single block at either end - if it did , this wouldn't be a representative oracle function
    # there wil lbe at least 2 "sandwidched" middle blocks of plaintext with which to compare

    test_ptext = bytearray(4 * blocklen * "A", 'utf-8')
    ctext = ciphers.aes128ecb_enc_oracle(test_ptext)
    if ctext[blocklen:2*blocklen] != ctext[2*blocklen:3*blocklen]: exit("not ecb mode")


    # also of note: once the first block is solved, we just cycle the loop again
    # but instead of varying the last byte at the end of the "A"s, we use "A"s to nudge the oracle function back one
    # then create a string of, say, 15 of our just solved block 0 characters, plus 1 0-255 "to find" chars....
    # e.g. with a blocklen of 4 bytes (to ease illustration)
    # oracle encrypts:
    # {input bytes}[XBCD][EFGH][IJKL][MN~pad~~pad~]
    #
    # ## pass 0 - block 0 ##
    # so we feed in "AAA" so oracle encrypts:
    # [AAAX][BCDE][FGHI][JKLM][N~pad~~pad~~pad~]
    # we keep this ciphertext for comparison
    # then we feed in "AAA-chr(0-255)-" so oracle encrypts:
    # [AAA-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
    # we compare each iteration with the kept ctext from above
    # if the first block matches, we know that the first oracle added character is one of the values,
    # in this instance X
    #
    #  ## pass 1 - block 0
    # we feed in "AA" and know the next char is X so oracle encrypts
    # [AAXB][CDEF][GHIJ][KLMN]  <- note, 1 block less - would be a full padded block otherwise
    # we keep this ciphertext for comparison
    # then we feed in "AAX-chr(0-255)-" so oracle encrypts:
    # [AAX-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
    # we compare each iteration with the kept ctext from above
    # if the first block matches, we know that the second oracle added character is one of the values,
    # in this instance B
    #
    #  ## pass 2 - block 0
    # we feed in "A" and know the next chars are XB so oracle encrypts
    # [AXBC][DEFG][HIJK][LMN~pad~]  <- note, 1 block less - would be a full padded block otherwise
    # we keep this ciphertext for comparison
    # then we feed in "AXB-chr(0-255)-" so oracle encrypts:
    # [AXB-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
    # we compare each iteration with the kept ctext from above
    # if the first block matches, we know that the third oracle added character is one of the values,
    # in this instance C
    #
    #  ## pass 3 - block 0
    # we feed in "" and know the next chars are XBC so oracle encrypts
    # [XBCD][EFGH][IJKL][MN~pad~~pad~]  <- note, 1 block less - would be a full padded block otherwise
    # we keep this ciphertext for comparison
    # then we feed in "XBC-chr(0-255)-" so oracle encrypts:
    # [XBC-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
    # we compare each iteration with the kept ctext from above
    # if the first block matches, we know that the fourth oracle added character is one of the values,
    # in this instance D
    #
    ######
    # ## we now know the first block in entirety - onto the second block
    ######
    #
    #  ## pass 0 - block 1
    # so we feed in "AAA" so oracle encrypts:
    # [AAAX][BCDE][FGHI][JKLM][N~pad~~pad~~pad~]
    # note that we are focussing attention on the second block now
    # we know from this 'new' second block that the first 3 chars are "BCD"
    # we keep this ciphertext for comparison
    # then we feed in "BCD-chr(0-255)-" so oracle encrypts:
    # [BCD-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
    # we compare each iteration with the kept ctext from above
    # if the first block of this matches the second block above, we know that the 5th oracle added character is
    # in this instance E
    #
    #  ## and repeat
    # so - here goes...

    num_ctext_blocks = blank_ctlen // blocklen
    ptext = bytearray()
    for i in range(num_ctext_blocks):
        # determine the string we are going to use to compare with
        # for the 0th block, it's the synthetic set of As
        # for block > 0 it's the prior ptext block
        if(i == 0): compare_block = bytearray(blocklen * "A", 'utf-8')
        else: compare_block = ptext[(i-1)*blocklen:i*blocklen]

        for j in range(blocklen):
            # the feed string into the oracle is made up of "A" padding
            padding_len = blocklen - j - 1
            feedstr = bytearray(padding_len * "A", 'utf-8')
            pullback_ctext = ciphers.aes128ecb_enc_oracle(feedstr)

            for k in range(255):

                if j == 15: current_compare_block = ptext[-j:] + bytearray(chr(k), 'utf-8')
                elif j == 0: current_compare_block = compare_block[-(blocklen-j-1):] + bytearray(chr(k), 'utf-8')
                else: current_compare_block = compare_block[-(blocklen-j-1):] + ptext[-j:] + bytearray(chr(k), 'utf-8')

                test_ctext = ciphers.aes128ecb_enc_oracle(current_compare_block)
                standalone_test_block = test_ctext[0:blocklen]
                scan_pullback_test_block = pullback_ctext[i*blocklen:(i+1)*blocklen]
                if  standalone_test_block == scan_pullback_test_block:
                    ptext.append(k)
                    break
                else:
                    continue

    # this isn't as clear cut as first expected - the ptext returned is not necessarly a multiple of blocklen
    # this is due to the sliding window approach - the padding becomes variable as the text into the oracle
    # varies in lengths
    unpad_ptext = stringmanip.ba_pkcs7_remove(ptext, blocklen)
    print(unpad_ptext)




if __name__ == '__main__':
    main()

