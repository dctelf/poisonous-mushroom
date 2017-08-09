#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import optparse
from cryptochallenge import stringmanip, ciphers, textscore
import base64


def main():
    parser = optparse.OptionParser()

    parser.add_option(
        "-f",
        action="store",
        type="string",
        dest="filename",
        help="path to file of multiple equal length hex encoded text strings"
    )


    options, args = parser.parse_args()

    # might be worth trying to break some of this into methods in modules for re-use?
    with open(options.filename, 'r') as f:
        b64str = ""
        for line in f:
            b64str += line.strip()

    distances = []
    if stringmanip.isRFC6468b64String(b64str):
        i = 0
        for keysize in range(2,41):
            distances.append({})
            distances[i]['keysize'] = keysize
            abs_hd = textscore.str_hammingDist(b64str[0:keysize], b64str[keysize:(2*keysize)])
            distances[i]['norm_hd'] = abs_hd/keysize
            i += 1


        sorted_distances = sorted(distances, key=lambda k: k['norm_hd'])
        print(sorted_distances)



if __name__ == '__main__':
    main()
