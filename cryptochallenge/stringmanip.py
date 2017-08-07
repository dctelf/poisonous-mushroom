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
        numpadchars = 2 - padgrouplen
        padstr = numpadchars * '='
    else:
        padblock = False
        padstr = ''

    
    # consider popping the to be padded bytes off the end of the input bytearray
    # that way the entire byte array can be iterated through first then only if there
    # is a group to be padded do we enter that clause

    # identify the number of 6 bit words in the last group to be converted
    # does this depend on trailing 0's? i.e. do I need to do the conversion to b64 first before deciding?

# hmm - none of this feels very elegant, it's neither concise for efficiency, or verbose but clear
# might need a bit of a refactor
def old_bytearrayToBase64(in_bytes):

    # identify the total number of 3 byte groups to handle
    # bearing in mind that the last group may have 1, 2 or 3 bytes to convert
    # in which case this last group requires padding consideration
    numbytes = len(in_bytes)
    numbytes_modulo3 = numbytes % 3
    num_padchars = 2 - numbytes_modulo3

    full_groups = (numbytes - numbytes_modulo3) / 3

    # establish the base64 sting to return
    b64string = ''

    # eat away groups of 3 bytes from the LHS of the provided byte array
    for group in range(full_groups):
        startpos = group * 3
        endpos = startpos + 3
        inbuf = in_bytes[startpos:endpos]
        # we are in a full group which will require no padding
        # do some bit shifting to pull apart 6 bit words
        b64string += valueToBase64Char( ( inbuf[0] & 0b11111100 ) >> 2 )
        b64string += valueToBase64Char(( ( (inbuf[0] << 8) | inbuf[1]) & 0b0000001111110000 ) >> 4 )
        b64string += valueToBase64Char(( ( (inbuf[1] << 8) | inbuf[2]) & 0b0000111111000000 ) >> 6 )
        b64string += valueToBase64Char( inbuf[2] & 0b00111111 )

        print(b64string)

    if numbytes_modulo3 > 0:
        # we have some padding to consider
        padstr = num_padchars * '='
        #
    # stretch out the input buffer with 0's as appropriate and prepare the pad string
    for i in range(3 - remaining_characters):
        inbuf.append(0)
        padstr += "="

    # mask out the 3 byte input buffer into 4 * 6 bit words
    op_word1 = (inbuf[0] & 0b11111100) >> 2
    op_word2 = (((inbuf[0] << 8) | inbuf[1]) & 0b0000001111110000) >> 4
    op_word3 = (((inbuf[1] << 8) | inbuf[2]) & 0b0000111111000000) >> 6
    op_word4 = inbuf[2] & 0b00111111

    print(inbuf)


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