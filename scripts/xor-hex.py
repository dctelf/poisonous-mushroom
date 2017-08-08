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
        "--stra",
        action="store",
        type="string",
        dest="str_a",
        help="First hex string"
    )

    parser.add_option(
        "--strb",
        action="store",
        type="string",
        dest="str_b",
        help="Second hex string"
    )
    options, args = parser.parse_args()

    if(stringmanip.isHexString(args[0]) & stringmanip.isHexString(args[1])):
        print(stringmanip.hexStrXOR(args[0], args[1]))
    else:
        print("input is not hex")

if __name__ == '__main__':
    main()
