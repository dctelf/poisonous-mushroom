# /usr/bin/python3

import re

def hexStringToByteArray(hex_string):
    # convert hex string to bytearray of character values
    char_values = bytearray(hex_string, 'utf-8')

    # hex strings use 2 characters to represent a byte
    # if there are an odd number of characters, the left most character represents
    # the lower word of a byte
    # if there are an even number of characters, the left most character represents
    # the upper word of a byte
    string_bytes_count = len(char_values)
    if string_bytes_count % 2 == 1: upperWord = False
    else upperWord = True

    # iterate over the characters passed and convert the encoded values to representative values
    # in utf-8/Ascii: 0-9 => 48-47; a-f => 97-102
    for i in range(string_bytes_count):

        character = char_values.pop()

        if character < 58:
            digit_value = character - 48
        else:
            digit_value = character - 87

# a0 => 16*10 + 0 = 160
# a => 16*0 + 10 = 10
# abc
# len 3
# 10, 11, 12
# 2748 => bc: 188 + a00 => 2560

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