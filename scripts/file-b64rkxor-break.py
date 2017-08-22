#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import optparse
from cryptochallenge import b64rkxor



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

    b64solver = b64rkxor.B64rkxor(b64str)
    likelykeys = b64solver.get_likely_key_lengths(5)
    b64solver.transpose_ctext_by_keylengths(likelykeys)
    results = b64solver.reverse_bytexors_on_transpositions()
    for result in results:
        print("##############################################")
        print("### identified key")
        print(results[result]['combined_bakey'])
        print("### yields ptext")
        print(results[result]['combined_baptext'])
        print("\n\n")



if __name__ == '__main__':
    main()
