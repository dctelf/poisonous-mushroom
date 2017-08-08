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

    # determine number of entire groups of 3 bytes to be converted
    numbytes = len(in_bytes)

    # identify whether there is a final group of 1 or 2 input bytes which requires padding
    # and hence, identify the number of "=" characters to append
    padgrouplen = numbytes % 3
    if (padgrouplen) > 0:
        padblock = True
        numpadchars = 3 - padgrouplen
        padstr = numpadchars * '='
    else:
        padblock = False
        padstr = ''

    numgroups = int((numbytes - padgrouplen) / 3)

    # initialise an empty base64 string to subsequently return
    b64string = ''

    # iterate over all the full 3 byte groups
    for group in range(numgroups):
        startpos = group * 3
        endpos = startpos + 3
        inbuf = in_bytes[startpos:endpos]
        # we are in a full group which will require no padding
        # do some bit shifting to pull apart 6 bit words
        b64string += valueToBase64Char((inbuf[0] & 0b11111100) >> 2)
        b64string += valueToBase64Char((((inbuf[0] << 8) | inbuf[1]) & 0b0000001111110000) >> 4)
        b64string += valueToBase64Char((((inbuf[1] << 8) | inbuf[2]) & 0b0000111111000000) >> 6)
        b64string += valueToBase64Char(inbuf[2] & 0b00111111)

    if padblock:
        # we also need to consider a padded block of 1 or 2 bytes
        # identify the index from the end of the input we care about
        negativepos = 0 - padgrouplen

        # and stick those bytes into inbuf
        inbuf = in_bytes[negativepos:]

        # if there is 1 input byte:
        #   we always encode into 2 * 6 bit words, even if the last one is all 0s and converts to an A
        # if there are 2 input bytes:
        #   we always encode into 3 * 6 bit words, even if the last word is all 0's and converts to an A

        if padgrouplen == 1:
            b64string += valueToBase64Char((inbuf[0] & 0b11111100) >> 2)
            b64string += valueToBase64Char((((inbuf[0] << 8)) & 0b0000001111110000) >> 4)
        elif padgrouplen == 2:
            b64string += valueToBase64Char((inbuf[0] & 0b11111100) >> 2)
            b64string += valueToBase64Char((((inbuf[0] << 8) | inbuf[1]) & 0b0000001111110000) >> 4)
            b64string += valueToBase64Char((((inbuf[1] << 8)) & 0b0000111111000000) >> 6)
        else:
            exit("something went wrong with the length of the padding group")

    b64string += padstr
    return b64string


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