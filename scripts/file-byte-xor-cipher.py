#!/usr/bin/python

# setup the ability to import modules from a sibling directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import optparse
from cryptochallenge import stringmanip, ciphers


def main():
    parser = optparse.OptionParser()

    parser.add_option(
        "-f",
        action="store",
        type="string",
        dest="filename",
        help="path to file of multiple equal length hex encoded text strings"
    )


    options, args = parser.parse_args()

    with open(options.filename, 'r') as f:
        i = 0
        highscorers = []
        for line in f:
            line = line.strip()
            if stringmanip.isHexString(line):
                top3_results = ciphers.reverseOneByteXOR(line)
                top_result = top3_results[-1]

                highscorers.append({})

                highscorers[i]['score'] = top_result['length_norm_score']
                highscorers[i]['line'] = i
                highscorers[i]['cipher_text'] = line
                highscorers[i]['plain_text'] = top_result['likely_res_ba']
                highscorers[i]['key_int'] = top_result['key_int']
                highscorers[i]['key_chr'] = top_result['key_chr']
            else:
                print("line ", i, " isn't hex")



            i += 1

    sorted_scores = sorted(highscorers, key=lambda k: k['score'])
    top_result = sorted_scores[-1]

    print("top result line:", top_result['line'])
    print("top result score:", top_result['score'])
    print("top result key int:", top_result['key_int'])
    print("top result key chr:", top_result['key_chr'])
    print("top result ciphertext:", top_result['cipher_text'])
    print("top result plaintext:", stringmanip.bytearrayToUTF8Str(top_result['plain_text']) )

    print("next highest score: ", sorted_scores[-2])
    print("next highest score: ", sorted_scores[-3])

if __name__ == '__main__':
    main()
