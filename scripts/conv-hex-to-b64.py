#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import optparse
from cryptochallenge import stringmanip


def main():
    parser = optparse.OptionParser()

    parser.add_option(
        "-i",
        "--instr",
        action="store",
        type="string",
        dest="input_hex",
        help="Hex string to convert to base64"
    )
    options, args = parser.parse_args()

    if(stringmanip.isHexString(options.input_hex)):
        print(stringmanip.hexToBase64(options.input_hex))
    else:
        print("input is not hex")

if __name__ == '__main__':
    main()
