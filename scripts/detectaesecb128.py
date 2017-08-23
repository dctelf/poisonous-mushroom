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
        help="path to file of hex encoded AES128 ECB encrypted message"
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
    i = 0
    with open(options.filename, 'r') as f:
        ecbline = False
        for line in f:
            # convert the hex string into a bytearray
            ctextba = stringmanip.hexStringToByteArray(line.strip())

            # going to assume here that the window is 128 bits (16 bytes)
            # although, the problem statement calls out only AES, which could be 128, 192 or 256 bit modes
            windowlen = 16

            ctextlen = len(ctextba)
            if ctextlen % windowlen != 0:
                print(f"line {i} length is not a multiple of {windowlen} bytes.")
                continue

            numwindows = ctextlen // windowlen

            k = 1
            for j in range(numwindows):
                for l in range(k, numwindows):
                    block_a_strpos = j * windowlen
                    block_a_endpos = block_a_strpos + windowlen

                    block_b_strpos = l * windowlen
                    block_b_endpos = block_b_strpos + windowlen

                    ctext_block_a = ctextba[block_a_strpos:block_a_endpos]
                    ctext_block_b = ctextba[block_b_strpos:block_b_endpos]

                    if ctext_block_a == ctext_block_b: ecbline = True
                k += 1

            if ecbline:
                print("likely ECB encrypted string (hex):")
                print(line)
                aes128obj = AES.new(options.enckey, AES.MODE_ECB)
                ptext = aes128obj.decrypt(bytes(ctextba))
                print("decrypted with key gives:")
                print(ptext)
                ecbline = False

            i += 1


if __name__ == '__main__':
    main()

