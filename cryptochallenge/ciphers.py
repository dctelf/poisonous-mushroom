#!/usr/bin/python

import re
from cryptochallenge import stringmanip, textscore


def reverseOneByteXOR(hex_str):
    # obtain bytearray of the hex string
    ba = stringmanip.hexStringToByteArray(hex_str)

    # iterate over all the possible single byte values
    ciphertext_len = len(ba)
    characterscore = {}
    for i in range(255):
        testkey = bytearray([i]) * ciphertext_len
        test_plain_ba = stringmanip.byteArrayXOR(testkey, ba)
        # we can't covert to a string, as some resultant bytes may not be valid utf-8
        # instead, we score the bytearray in absolute terms first
        abs_score = textscore.englishAbsScore(test_plain_ba)
        characterscore[i] = abs_score

    score_desc_keys = sorted(characterscore, key=characterscore.get)

    result_structure = []

    top3_keys = score_desc_keys[-3:]

    i = 0
    for key in top3_keys:
        result_structure.append({})
        result_structure[i]['length_norm_score'] = characterscore[key]
        result_structure[i]['key_int'] = key
        result_structure[i]['key_chr'] = chr(key)

        testkey = bytearray([key]) * ciphertext_len

        result_structure[i]['likely_res_ba'] = stringmanip.byteArrayXOR(testkey, ba)

        i+= 1

    return result_structure






