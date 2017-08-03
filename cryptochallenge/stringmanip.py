# /usr/bin/python3

import re


def hexStringToByteArray(hex_string):
    # convert hex string to bytearray of character values
    char_values = bytearray(hex_string, 'utf-8')

    string_bytes_count = len(char_values)

    # perhaps lazy, but if there is an odd number of characters in the hex string
    # prepend the string with a "0" character

    if string_bytes_count % 2 == 1:
        # aware I could do away with the string to byte conversion by setting this to be integer value 48
        # but this would just look like an arbitrary magic number here
        char_values[:0] = bytearray('0', 'utf-8')
        string_bytes_count += 1

    # iterate over the characters passed and convert the encoded values to representative values

    ba = bytearray()
    for i in range(int(string_bytes_count/2)):
        upper_word = hexCharToValue(char_values[i*2])
        lower_word = hexCharToValue(char_values[(i*2)+1])
        byte_value = (upper_word * 16) + lower_word
        ba.append(byte_value)

    return ba


def hexCharToValue(hex_char):
    # in utf-8/Ascii: 0-9 => 48-47; a-f => 97-10
    if hex_char < 58: return hex_char - 48
    else: return hex_char - 87

def bytearrayToBase64(in_bytes):

    # identify the total number of 3 byte groups to handle
    # bearing in mind that the last group may have 1, 2 or 3 bytes to convert
    # this last group requires padding consideration
    numbytes = len(in_bytes)
    groups = int((numbytes-1)/3) + 1

    for group in range(groups):
        startpos = group * 3
        endpos = startpos + 3
        inbuf = in_bytes[startpos:endpos]
        print(inbuf)
        if group != groups:
            # we are in a full group which will require no padding
            # do some bit shifting to pull apart 6 bit words
            
        else:
            # we are in the last group, which may require padding


    return True

def valueToBase64Char(b64_value):
    # 0 - 25 => A - Z (ASCII 65 - 90)
    # 26 - 51 => a - z (ASCII 97 - 122)
    # 52 - 61 => 0 - 9 (ASCII 48 - 57)
    # 62 => + (ASCII 43)
    # 63 => / (ASCII 47)
    if b64_value < 26:
        return chr(b64_value + 65)
    if b64_value < 52:
        return chr(b64_value + 71)
    if b64_value < 62:
        return chr(b64_value - 4)
    if b64_value == 62:
        return chr(43)
    if b64_value == 63:
        return chr(47)
    else:
        exit(1)


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