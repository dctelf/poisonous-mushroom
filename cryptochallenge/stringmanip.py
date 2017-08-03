# /usr/bin/python3

import re

def hexStringToByteArray(hex_string):
    # convert hex string to bytearray of character values
    char_values = bytearray(hex_string, 'utf-8')

    for character in char_values:
        if character < 58:
            digit_value = character - 48
        else:
            digit_value = character - 87
        print(digit_value)
#    48: 0
#    49: 1
#    50: 2
#    51: 3
#    52: 4
#    53: 5
#    54: 6
#    55: 7
#    56: 8
#    57: 9
#
#   97: a
#   98: b
#    99: c
#    100: d
#    101: e
#    102: f


def bytearrayToBase64(bytearray):
    return ("def456")


def hexToBase64(hex_string):
    return bytearrayToBase64(hexStringToByteArray(hex_string))

def isHexString(input_string):
    m = re.match('^[a-f0-9]+$',input_string)
    if m: return True
    else: return False

def isRFC6468b64String(input_string):
    m = re.match('^[a-zA-Z0-9\+/=]+$',input_string)
    if m: return True
    else: return False