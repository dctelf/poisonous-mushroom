#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from cryptochallenge import config, ciphers, userprofile, stringmanip

def main():
    # initialise the global encryption key for all operations in this run
    config.oracle_enc_key = ciphers.generate_rand_ba(16)

    # rather than detect the blocklength etc. lets just go for knowing it to be AES-128
    # similarly, rather than go over old ground, we know it's ECB

    # different this time, we don't want to break the unknown suffix inside the oracle
    # rather, we want to generate a ctext equivalent to a different ptext than the oracle prepares
    # without knowing the key

    # bytearray(b'email=2018_tests@bob.com&uid=10&role=user')
    # bytearray(b'email=2018_tests@bob.com&uid=10&role=admin')

    # right... want the block boundary to land so that the first character of the last block is the "u" of user
    # vary the length of the email address to position this at the right spot
    # and the "fake" final enc block can be derived by feeding in a faked padded block

    # feed in "{admin[pad][pad][pad][pad][etc.]}{aaaaaaaa*[i]@bob.com....}
    # so that the method encrypts
    # "{admin[pad][pad][pad][pad][etc.]}{aaaaaaaa*[i]@bob.com....}

    # nope, not quite... need to vary after the "email=" prefix, so we have to pad creatively (or maybe call the method twice?)
    # we want to force the method to encrypt the following string (with { as the block length boundary)
    # {first block, just pad with a's to 'avoid' the "email=" component}
    # {second block, create a fake "admin" + pkcs7 pad block}
    # {third block create a full block of pad + @bob.com&uid=10&role=}
    # {allow the 4th block to be created of "user[pad][pad][pad]..."
    # {admin=aaaaaaaa[*i]} {admin[pad][pad][etc.]} {@bob.com
    # then, combine the first + third + second cipher text blocks to get the "faked" ctext
    # then decrypt

    # admin= is 6 chars, so we need
    block1_ext = 10 * "a"

    block2 = stringmanip.bytearrayToUTF8Str(stringmanip.ba_pkcs7_pad(bytearray('admin', 'utf-8'), 16))
    block3 = "@co"

    insert_text = block1_ext + block2 + block3

    manipulated_enc_profile = userprofile.enc_profile_for(insert_text)
    restruct = b''.join([manipulated_enc_profile[0:16], manipulated_enc_profile[32:48], manipulated_enc_profile[16:32] ])

    print(restruct)

    print(userprofile.dec_profile_for(restruct))


if __name__ == '__main__':
    main()

