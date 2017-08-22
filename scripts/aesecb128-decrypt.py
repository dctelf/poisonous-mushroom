#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import optparse
from cryptochallenge import stringmanip
from Crypto.Cipher import AES



def main():
    parser = optparse.OptionParser()

    parser.add_option(
        "-f",
        action="store",
        type="string",
        dest="filename",
        help="path to file of base64 encoded AES128 ECB encrypted message"
    )

    parser.add_option(
        "-k",
        action="store",
        type="string",
        dest="enckey",
        help="encryption key string"
    )

    options, args = parser.parse_args()

    # might be worth trying to break some of this into methods in modules for re-use?
    with open(options.filename, 'r') as f:
        b64str = ""
        for line in f:
            b64str += line.strip()

    baciphertext = stringmanip.base64ToBytearray(b64str)
    aes128obj = AES.new(options.enckey, AES.MODE_ECB)
    ptext = aes128obj.decrypt(bytes(baciphertext))
    print(ptext)

if __name__ == '__main__':
    main()

