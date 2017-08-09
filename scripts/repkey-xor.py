#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import optparse
from cryptochallenge import stringmanip, ciphers


def main():
    parser = optparse.OptionParser()

    options, args = parser.parse_args()

    cipher_ba = ciphers.repkeyXOR(args[0], args[1])
    print(args[0])
    print(stringmanip.bytearrayToHexStr(cipher_ba))


if __name__ == '__main__':
    main()
