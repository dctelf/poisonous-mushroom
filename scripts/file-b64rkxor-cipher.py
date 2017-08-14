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


    if stringmanip.isRFC6468b64String(b64str):
        distances = []
        # there's an issue in here - I'm using the b64 string to determine distances and transpositions
        # but I need to decode it from b64 into real data values first before operating upon it
        i = 0
        for keysize in range(2,41):
            distances.append({})
            distances[i]['keysize'] = keysize
            abs_hd = textscore.str_hammingDist(b64str[0:keysize], b64str[keysize:(2*keysize)])
            distances[i]['norm_hd'] = abs_hd/keysize
            i += 1


        sorted_distances = sorted(distances, key=lambda k: k['norm_hd'])

        low5_distances = sorted_distances[0:5]
        # build the transposed string
        ctext_len = len(b64str)

        for distance in low5_distances:
            distance['transpose'] = []
            for i in range(distance['keysize']): distance['transpose'].append("")
            for i in range(ctext_len): distance['transpose'][i % distance['keysize']] += b64str[i]
        print(low5_distances)

        # we now have transposed ctext strings in the data structure
        for distance in low5_distances:
            distance['transp_ptext'] = []
            for i in range(distance['keysize']):
                # distance['']
                print(i)
            # ciphers.reverseOneByteXOR()


if __name__ == '__main__':
    main()
