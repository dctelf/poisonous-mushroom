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

    if(stringmanip.isHexString(args[0])):
        top3_results = ciphers.reverseOneByteXOR(args[0])
        print("top 3 identified results:")
        for i in top3_results:
            print(top3_results[i])
        print("winning result:")
        print(stringmanip.bytearrayToUTF8Str(top3_results[i]['likely_res_ba']))
        print("winning key:")
        print(top3_results[i]['key_chr'])
    else:
        print("input is not hex")

if __name__ == '__main__':
    main()
