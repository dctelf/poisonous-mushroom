#!/usr/bin/python

import optparse
from modules import stringmanip

def main():
    parser = optparse.OptionParser()

    parser.add_option(
        "-h",
        "--hexstr",
        action="store",
        type="string",
        dest="input_hex",
        help="Hex string to convert to base64"
    )
    options, args = parser.parse_args()

    print(stringmanip.hexToBase64(options.input_hex))

if __name__ == '__main__':
    main()
