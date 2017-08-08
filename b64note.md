# identify the number of 6 bit words in the last group to be converted
    # does this depend on trailing 0's? i.e. do I need to do the conversion to b64 first before deciding?
    # no, as it happens;
    # if there are 2 input bytes:
    #   we always encode into 3 * 6 bit words, even if the last word is all 0's and converts to an A
    # if there is 1 input byte:
    #   we also always encode into 2 * 6 bit words, even if the last one is all 0s and converts to an A

    if padgrouplen == 1:
        b64string += valueToBase64Char((inbuf[0] & 0b11111100) >> 2)
        b64string += valueToBase64Char((((inbuf[0] << 8)) & 0b0000001111110000) >> 4)
    elif padgrouplen == 2:
        b64string += valueToBase64Char((inbuf[0] & 0b11111100) >> 2)
        b64string += valueToBase64Char((((inbuf[0] << 8) | inbuf[1]) & 0b0000001111110000) >> 4)
        b64string += valueToBase64Char((((inbuf[1] << 8)) & 0b0000111111000000) >> 6)
    else:
        exit("somethign went wrong with the length of the padding group")

    # there's an interesting footnote here (I think)....
    # certain ranges of input values at the end of the sequence of data rwesult in conversion of
    # a 6 bit word of 0s into b64 - these strings appear as xA= or xA==.  I need to check, but I don't
    # think there is any ambiguity even if the "A" is discarded, but this does then require the "="
    # apparently, some encodings discard the "=" padding, hence the A's are then required to give clarity on the
    # final 2 bits of the first input byte, or there may be some ambiguity (not entirley sure this is correct though
    # needs some validation...
    
    single bytes
------------


2 bytes
-------


str 5 5
0x 35 35

[ 0011 0101 ] [ 0011   0100 ] [0]

{001101} 	 {010011} {010000} {000000}

NTU=

str 5 4	
0x 35 34

[ 0011 0101 ] [ 0011   0101 ] [0]

{001101} 	 {010011} {010100} {000000}

NTQ=

str 5 @
0x 35 40

[ 0011 0101 ] [ 0100   0000 ] [0]

{001101} 	 {010010} {000000} {000000}

NUA=

so:
    if there are 2 characters, we always encode into 3 * 6 bit words, even if the last one is all 0's and converts to an A
    if there is 1 character, we also always encode into 2 * 6 bit words, even if the last one is all 0s and converts to an A
