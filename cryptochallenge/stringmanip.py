# /usr/bin/python3

import re

def hexStringToByteArray(hex_string):
    # convert hex string to bytearray of character values
    char_values = bytearray(hex_string, 'utf-8')


    #

    #


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