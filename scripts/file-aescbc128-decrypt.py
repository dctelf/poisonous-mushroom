#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import optparse
from cryptochallenge import stringmanip, ciphers


def main():
    parser = optparse.OptionParser()

    parser.add_option(
        "-f",
        action="store",
        type="string",
        dest="filename",
        help="path to file of base64 encoded ciphertext"
    )

    parser.add_option(
        "-k",
        action="store",
        type="string",
        dest="key",
        help="path to file of multiple equal length hex encoded text strings"
    )

    parser.add_option(
        "-i",
        action="store",
        type="string",
        dest="iv",
        help="hex string of initialisation vector"
    )


    options, args = parser.parse_args()

    with open(options.filename, 'r') as f:
        b64str = ""
        for line in f:
            b64str += line.strip()

    ctext_ba = stringmanip.base64ToBytearray(b64str)
    iv_ba = stringmanip.hexStringToByteArray(options.iv)
    key_ba = bytearray(options.key, 'utf-8')
    ptext = ciphers.my_ba_aes_cbc128_dec(ctext_ba, key_ba, iv_ba)
    print(ptext)


if __name__ == '__main__':
    main()
