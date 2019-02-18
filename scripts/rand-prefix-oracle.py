#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from cryptochallenge import config, ciphers, userprofile, stringmanip

import random, string

def main():
    # initialise the global encryption key for all operations in this run
    config.oracle_enc_key = ciphers.generate_rand_ba(16)

    # set a bound on the length of the random prefix to a max of 1000 characters (this will cover all use cases, just makes
    # debugging and walk through of the code a bit more managable.)

    rand_prefix_len = random.randint(1,1000)

    config.rand_prefix = ''.join(random.choices(string.printable, k=rand_prefix_len))

    # so, we don't know the length of either the prefix or the suffix
    # assume we know that the cipher operates in 128 bit (16 char, 16 byte) blocks
    # so, first off, determine the length of the prefix and suffix combined

    # initially, pass an empty string

    ptext = ""
    ba_ptext = bytearray(ptext, 'utf-8')
    no_ptext_ctext = ciphers.aes128ecb_pre_post_oracle(ba_ptext)

    len_pre_and_post = len(no_ptext_ctext)

    # hmm - I'm trying to find the length of the prefix and suffix
    # I can get close to this by a few means
    # if I generate a 31 byte block of plaintext and push this into the oracle
    # I know that somewhere in the ctext there will be a ciphertext of a known 16 byte block
    # (note, risk that my plaintext collides with the random prefix and suffix - fairly unlikely so not going to get too vexed)
    # if the ctext for no string is compared with the ctext for this string block by block,


    # there are some interesting conditions...
    # ''''
    # condition 0a - less than 16 byte prefix & suffix (a+b < 16)
    # [aB-block-prefix]^insert^[bB-block-suffix]
    # in no value passed state, block will be pkcs#7 padded by one or more bytes
    # tests for confirmation of this state:
    # no bytes passed should return 1 block of ctext
    # continue passing bytes until ctext trips over into 2 blocks
    # the number of iterations gives (16-(a+b))
    # ''''
    # condition 0b - exactly 16 bytes of prefix and suffix
    # [aB-block-prefix]^insert^[bB-block-suffix]
    # in no value passed state, block will have no padding
    # tests for confirmation of this state:
    # no bytes passed should return 1 block of ctext
    # one byte (to 16 bytes) passed should return 2 blocks of ctext
    # ''''
    # condition 1b - prefix is less than
    # [aB-block-prefix]^insert^[bB-block-suffix]
    # in no value passed state, block will have no padding
    # tests for confirmation of this state:
    # no bytes passed should return 1 block of ctext
    # one byte (to 16 bytes) passed should return 2 blocks of ctext

    for i in range(16):
        insert_ba = bytearray((i*"a"), 'utf-8')
        ctext = ciphers.aes128ecb_pre_post_oracle(insert_ba)
        print(len(ctext))


    # => if insert == 1B,
    # condition 1 - window block alignment
    # [16B-block-prefix]^insert^[16B-block-suffix]
    #

    print(len_pre_and_post)
    # the purpose is only to decrypt the suffix, not the prefix
    # we don't as yet know the suffix length, but something happens here
    # i.e. the suffix will solely exist in the ctext somewhere between len(ptext) == 0 and len(ptext) == 15

    # if we pass 16 bytes then 32 bytes into the oracle, working back from the end, the like for like ctext blocks
    # must contain the suffix - the blocks that vary are the 1 or 2 passed blocks

    single_block_ba = bytearray(16*"a",'utf-8')
    single_block_ctext = ciphers.aes128ecb_pre_post_oracle(single_block_ba)
    print("#### pushing single 16 byte block ####")
    print(single_block_ctext)
    print(len(single_block_ctext))

    double_block_ba = bytearray(32 * " b", 'utf-8')
    double_block_ctext = ciphers.aes128ecb_pre_post_oracle(double_block_ba)
    print("#### pushing double 16 byte block ####")
    print(double_block_ctext)
    print(len(double_block_ctext))


    match = True
    num_suffix_blocks = 0
    i = 1
    blocklen = 16
    while match:
        if single_block_ctext[-(i*blocklen):] != double_block_ctext[-(i*blocklen):]:
            match = False
            continue
        num_suffix_blocks += 1
        i += 1
    print(num_suffix_blocks)

    if in

    """
    ptext = bytearray()
    for i in range(num_ctext_blocks):
        # determine the string we are going to use to compare with
        # for the 0th block, it's the synthetic set of As
        # for block > 0 it's the prior ptext block
        if (i == 0):
            compare_block = bytearray(blocklen * "A", 'utf-8')
        else:
            compare_block = ptext[(i - 1) * blocklen:i * blocklen]

        for j in range(blocklen):
            # the feed string into the oracle is made up of "A" padding
            padding_len = blocklen - j - 1
            feedstr = bytearray(padding_len * "A", 'utf-8')
            pullback_ctext = ciphers.aes128ecb_enc_oracle(feedstr)

            for k in range(255):

                if j == 15:
                    current_compare_block = ptext[-j:] + bytearray(chr(k), 'utf-8')
                elif j == 0:
                    current_compare_block = compare_block[-(blocklen - j - 1):] + bytearray(chr(k), 'utf-8')
                else:
                    current_compare_block = compare_block[-(blocklen - j - 1):] + ptext[-j:] + bytearray(chr(k),
                                                                                                         'utf-8')

                test_ctext = ciphers.aes128ecb_enc_oracle(current_compare_block)
                standalone_test_block = test_ctext[0:blocklen]
                scan_pullback_test_block = pullback_ctext[i * blocklen:(i + 1) * blocklen]
                if standalone_test_block == scan_pullback_test_block:
                    ptext.append(k)
                    break
                else:
                    continue
    """


if __name__ == '__main__':
    main()

