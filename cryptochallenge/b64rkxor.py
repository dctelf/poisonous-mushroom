#!/usr/bin/python

from cryptochallenge import ciphers
from cryptochallenge import stringmanip
from cryptochallenge import textscore
import math

class B64rkxor(object):

    def __init__(self, b64string):
        if not (type(b64string) == str
                and b64string != ""
                and stringmanip.isRFC6468b64String(b64string)):
            exit("argument passed must be a valid b64 string of length > 0")

        self.b64ciphertext = b64string
        self.baciphertext = stringmanip.base64ToBytearray(b64string)
        self.ctextlen = len(self.baciphertext)

        self.lowKeyLength = 2
        self.longKeyLength = 40
        self.hammingDistances = dict.fromkeys(range(self.lowKeyLength, self.longKeyLength))

        self.likely_key_lengths = []
        self.transpositions = {}
        self.results = {}

    def generate_hamming_distances(self):
        for keylength in self.hammingDistances.keys():
            self.hammingDistances[keylength] = {}
            firstblock = self.baciphertext[0:keylength]
            secondblock = self.baciphertext[keylength:(2*keylength)]
            thirdblock = self.baciphertext[(2 * keylength):(3 * keylength)]
            fourthblock = self.baciphertext[(3 * keylength):(4 * keylength)]
            abs_hd1 = textscore.ba_hammingDist(firstblock, secondblock)
            abs_hd2 = textscore.ba_hammingDist(secondblock, thirdblock)
            abs_hd3 = textscore.ba_hammingDist(thirdblock, fourthblock)

            abs_hd = (abs_hd1 + abs_hd2 + abs_hd3) / 3

            self.hammingDistances[keylength]['absolute_distance'] = abs_hd
            self.hammingDistances[keylength]['normalised_distance'] = abs_hd / keylength

    def get_likely_key_lengths(self, keycount):
        self.generate_hamming_distances()

        sorted_normalised_distances = sorted(
                                            self.hammingDistances,
                                            key=lambda x: (
                                                self.hammingDistances[x]['normalised_distance']
                                                            )
                                            )

        snd = sorted_normalised_distances[0:keycount]
        return snd

    def transpose_ctext_by_keylengths(self, keylengths):
        for keylength in keylengths:
            self.transpositions[keylength] = []
            for i in range(keylength): self.transpositions[keylength].append(bytearray())
            for i in range(self.ctextlen): self.transpositions[keylength][i % keylength].append(self.baciphertext[i])

    def reverse_bytexors_on_transpositions(self):
        for keylength in self.transpositions:
            self.results[keylength] = {}
            self.results[keylength]['ptext_parts'] = []
            self.results[keylength]['key_parts'] = []
            self.results[keylength]['combined_baptext'] = ""
            self.results[keylength]['combined_bakey'] = ""
            for ctext_part in self.transpositions[keylength]:
                results = ciphers.reverseOneByteXORba(ctext_part)
                highscore_result = results.pop()
                self.results[keylength]['ptext_parts'].append(highscore_result['likely_res_ba'])
                self.results[keylength]['key_parts'].append(highscore_result['key_chr'])
                self.results[keylength]['combined_bakey'] += highscore_result['key_chr']

            combined_baptext = bytearray(self.ctextlen)

            # which transposition we want to use
            transposition_index = 0

            # which position in the transposition we want to extract
            transposition_position = 0

            for i in range(self.ctextlen):
                transposition_index = i % keylength
                combined_baptext[i] = self.results[keylength]['ptext_parts'][transposition_index][transposition_position]

                if (transposition_index == (keylength - 1)):
                    transposition_position += 1

            self.results[keylength]['combined_baptext'] = combined_baptext

        return self.results




