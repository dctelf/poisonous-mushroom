# /usr/bin/python3

def englishAbsScore(test_ba):

    # make scores absolute
    # that is, the relative score and comparison of differing length strings
    # is handled above and outside this method
    string_abs_score = 0
    for test_char in test_ba:
        string_abs_score += singleCharacterScore(test_char)
    return string_abs_score


# going to allow a few A|B tests of this - outer method calls inner for simplicity
def singleCharacterScore(test_chr_val):
    # the more specific A version appears to produce more accurate results
    return singleCharacterScore_A(test_chr_val)

def singleCharacterScore_B(test_chr_val):
    # Type B: just score LC letters & space only
    # letter scores are taken from the wikipedia page on letter frequency
    # https://en.wikipedia.org/wiki/Letter_frequency

    # 97 - 122
    if (96 < test_chr_val < 123):
        lower_scores = [810, 140, 270, 420, 1270, 220, 200, 610, 700, 20, 80, 400, 240, 670, 750, 190, 10, 600, 630,
                        910, 280, 100, 240, 20, 200, 10]
        return lower_scores[(test_chr_val - 97)]

    # space is a valid character too - avg 200 points
    if ( test_chr_val == 32):
        return 300

    return 0


def singleCharacterScore_A(test_chr_val):
    # letter scores are taken from the wikipedia page on letter frequency
    # https://en.wikipedia.org/wiki/Letter_frequency

    # 97 - 122
    if (96 < test_chr_val < 123):
        lower_scores = [810, 140, 270, 420, 1270, 220, 200, 610, 700, 20, 80, 400, 240, 670, 750, 190, 10, 600, 630,
                        910, 280, 100, 240, 20, 200, 10]
        return lower_scores[(test_chr_val - 97)]

    # going to make a broad assumption that uppercase are 1/10 as likely as lower case equivalents
    # 65 - 90


    if (64 < test_chr_val < 91):

        lower_scores = [810, 140, 270, 420, 1270, 220, 200, 610, 700, 20, 80, 400, 240, 670, 750, 190, 10, 600, 630,
                        910, 280, 100, 240, 20, 200, 10]
        upper_scores = [x / 10 for x in lower_scores]
        return upper_scores[(test_chr_val - 65)]

    # space is a valid character too - avg 200 points
    if ( test_chr_val == 32):
        return 300

    # 33 - 47, 91 - 96, 123 - 127 are standard punctiation like symbols - 2 points
    if ( 32 < test_chr_val < 48 ) | ( 90 < test_chr_val < 97 ) | ( 122 < test_chr_val < 128 ): return 5

    # everything else is noise - 0 points
    return 0


