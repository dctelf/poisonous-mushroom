#!/usr/bin/python

import re
from cryptochallenge import stringmanip, textscore
from Crypto.Cipher import AES
import secrets
from random import randint


def repkeyXOR(plaintext, key):
    plaintextlen = len(plaintext)
    keylen = len(key)

    if keylen > plaintextlen:
        exit("not really prepared for padding plaintext yet :)")

    plaintext_ba = bytearray(plaintext, 'utf-8')
    key_ba = bytearray(key, 'utf-8')

    ciphertext_ba = ba_repkeyXOR(plaintext_ba, key_ba)

    return ciphertext_ba


def ba_repkeyXOR(ba_ptext, ba_key):
    keylen = len(ba_key)
    i = 0
    ciphertext_ba = bytearray()
    for byte in ba_ptext:
        keypos = i % keylen
        ciphertext_ba.append(byte ^ ba_key[keypos])
        i += 1
    return ciphertext_ba

def reverseOneByteXOR(hex_str):
    # obtain bytearray of the hex string
    ba = stringmanip.hexStringToByteArray(hex_str)
    return reverseOneByteXORba(ba)

def reverseOneByteXORba(ba):
    # iterate over all the possible single byte values
    ciphertext_len = len(ba)
    characterscore = {}
    for i in range(255):
        testkey = bytearray([i]) * ciphertext_len
        test_plain_ba = stringmanip.byteArrayXOR(testkey, ba)
        # we can't covert to a string, as some resultant bytes may not be valid utf-8
        # instead, we score the bytearray in absolute terms first
        abs_score = textscore.englishAbsScore(test_plain_ba)
        characterscore[i] = abs_score

    score_desc_keys = sorted(characterscore, key=characterscore.get)

    result_structure = []

    top3_keys = score_desc_keys[-3:]

    i = 0
    for key in top3_keys:
        result_structure.append({})
        result_structure[i]['length_norm_score'] = characterscore[key]
        result_structure[i]['key_int'] = key
        result_structure[i]['key_chr'] = chr(key)

        testkey = bytearray([key]) * ciphertext_len

        result_structure[i]['likely_res_ba'] = stringmanip.byteArrayXOR(testkey, ba)

        i+= 1

    return result_structure

def my_ba_aesecb128_dec(ba_ctext, enckey_str):
    aes128obj = AES.new(bytes(enckey_str), AES.MODE_ECB)
    ptext = aes128obj.decrypt(bytes(ba_ctext))
    return ptext

def my_ba_aesecb128_enc(ba_ptext, enckey_str):
    aes128obj = AES.new(bytes(enckey_str), AES.MODE_ECB)
    ctext = aes128obj.encrypt(bytes(ba_ptext))
    return ctext


def my_ba_aes_cbc128_dec(ba_ctext, ba_key, ba_iv):

    keylen = 16
    ptext = bytearray(len(ba_ctext))
    if len(ba_iv) != keylen: exit("iv length not 16 bytes")
    if len(ba_key) != keylen: exit("key length not 16 bytes")
    if (len(ba_ctext) % keylen) != 0: exit("ciphertext length not a multiple of 16 bytes")

    num_blocks = len(ba_ctext) // keylen

    for i in range(num_blocks):

        end_pos = (num_blocks - i) * keylen
        str_pos = end_pos - keylen

        prior_block_end_pos = str_pos
        prior_block_str_pos = prior_block_end_pos - keylen

        ctext_block = ba_ctext[str_pos:end_pos]
        ctext_block = my_ba_aesecb128_dec(ctext_block, ba_key)

        if i == (num_blocks - 1):
            prior_block = ba_iv
        else:
            prior_block = ba_ctext[prior_block_str_pos:prior_block_end_pos]

        ptext_block = ba_repkeyXOR(ctext_block, prior_block)

        ptext[str_pos:end_pos] = ptext_block

    return ptext



def my_ba_aes_cbc128_enc(ba_ptext, ba_key, ba_iv):

    keylen = 16
    ctext = bytearray()
    if len(ba_iv) != keylen: exit("iv length not 16 bytes")
    if len(ba_key) != keylen: exit("key length not 16 bytes")
    if (len(ba_ptext) % keylen) != 0: exit("plaintext length not a multiple of 16 bytes")

    num_blocks = len(ba_ptext) // keylen

    iniv = True
    for i in range(num_blocks):
        str_pos = i * keylen
        end_pos = str_pos + keylen

        if iniv:
            prior_block = ba_iv
            iniv = False

        ctext_block = ba_repkeyXOR(ba_ptext[str_pos:end_pos], prior_block)
        aes_block = my_ba_aesecb128_enc(ctext_block, ba_key)
        prior_block = aes_block
        ctext += aes_block


    return ctext


def lib_ba_aes_cbc128_dec(ba_ctext, ba_key, ba_iv):
    aes_cbc128obj = AES.new(bytes(ba_key), AES.MODE_CBC, bytes(ba_iv))
    ptext = aes_cbc128obj.decrypt(bytes(ba_ctext))
    return ptext

def generate_rand_ba(numbytes):
    # looks like there's already a cryptographically robust rng in the python std lib
    return secrets.token_bytes(numbytes)

def aes128_encryption_oracle(ba_ptext):
    rand_key = generate_rand_ba(16)
    rand_prefix = generate_rand_ba(randint(5,10))
    rand_suffix = generate_rand_ba(randint(5,10))
    rand_iv = generate_rand_ba(16)

    ba_ptext = rand_prefix + ba_ptext + rand_suffix

    pkcs_padded = stringmanip.ba_pkcs7_pad(ba_ptext, 16)
    print("rand key", rand_key)
    print("rand prefix len", len(rand_prefix))
    print("rand suffix len", len(rand_suffix))

    if randint(0,1) == 0:
        print("going for ecb this time round")
        ctext = my_ba_aesecb128_enc(pkcs_padded, rand_key)
    else:
        print("going for cbc this time round")
        ctext = my_ba_aes_cbc128_enc(pkcs_padded, rand_key, rand_iv)

    return ctext


def detect_aes128_ecbcbc():
    # hmm, right....
    # so...
    # ummm ...
    # we have a function above that;
    # - takes a string
    # - sticks on a random set of bytes between 5 and 10 bytes long on the front
    # - sticks on a random set of bytes between 5 and 10 bytes long on the front
    # - PKCS#7 pads it
    # - generates a random 16 byte key (and for CBC mode, a random 16 byte iv)
    # - then picks ECB or CBC mode at random and encrypts the string
    #
    # we want this function to call that function and detect which of ECB or CBC it called..
    # we don't know the key so we can't pretend to be the real function and then compare
    # but, we do know that for ECB mode, 2 identical blocks of input will always encrypt
    # to the same ciphertext block under the same key
    # so, we could construct a string where the non-ammended bytes (so, not the last block, not the first)
    # are identical, then try it

    test_str = 64 * "A"
    test_ba = bytearray(test_str, 'utf-8')

    print(test_ba)

    for i in range(100):
        ctext = aes128_encryption_oracle(test_ba)
        if ctext[16:32] == ctext[32:48]:
            print("detected ECB mode")
        else:
            print("detected CBC mode")

