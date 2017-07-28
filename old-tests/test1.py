#/usr/bin/python3
""" cryptopals.org set 1 challenge 1 test.py """

from modules import hex_to_b64


# this is a string represntation of a hex value
# we're using python 3, so this is a str type object
# encoded as utf-8 rather than (binary) data

Hexstring = '49276d206b696c6c' \
            '696e6720796f7572' \
            '20627261696e206c' \
            '696b65206120706f' \
            '69736f6e6f757320' \
            '6d757368726f6f6d'

HexvalByteArray = hex_to_b64.hexStringToByteArray(Hexstring)
print(HexvalByteArray)
Base64val = hex_to_b64.bytearrayToBase64(HexvalByteArray)
print(Base64val)

if Base64val == "SSdtIGtpbGxpbmcg" \
                "eW91ciBicmFpbiBs" \
                "aWtlIGEgcG9pc29u" \
                "b3VzIG11c2hyb29t":
    print("test passed: w00t!")
