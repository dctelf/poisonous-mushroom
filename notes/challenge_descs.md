# _poisonous-mushroom:_ 
# Matasano crypto challenge solutions in python

##<a name="challenge1" /> Convert hex to base64
[challenge 1](https://cryptopals.com/sets/1/challenges/1)

The string:
```
49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
```
Should produce:
```
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
```

### Approach:

* Top-level script "conv-hex-to-b64.py" taking single cmd line option of a hex string and returning to stdout the base64 encoded string
* A new module called stringmanip providing string manipulation methods;
    * hexStringToByteArray()
    * bytearrayToBase64()
    * hexToBase64()
* A suite of tests for each method validating these against the standard python methods

An interesting note on b64 conversion on the last 3 byte/4 word padded conversion

[b64note](notes/b64note.md)

## Fixed XOR
[challenge 2](https://cryptopals.com/sets/1/challenges/2)

Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

```
1c0111001f010100061a024b53535009181c
```
... after hex decoding, and when XOR'd against:

```
686974207468652062756c6c277320657965
```
... should produce:
```
746865206b696420646f6e277420706c6179
```

### My approach:

* Top-level script "xor-hex.py" taking two cmd line args as base64 strings and returning the base64 xor of the two values
* Addition of a method to the stringmanip module;
    * hexStrXOR()
    * byteArrayXOR()
    * bytearrayToHexStr()
* A suite of tests for these methods


## Single-byte XOR cipher
[challenge 3](https://cryptopals.com/sets/1/challenges/3)



The hex encoded string:

```
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
```

... has been XOR'd against a single character. Find the key, decrypt the message (use character frequency analysis to score output)

### My approach:

* Top-level script "byte-xor-cipher.py" taking one cmd line args - a hex encoded string which is the result of the xor cipher.
* New module textscore giving the following methods;
    * abc
* New module ciphers giving the following methods;  
    * reverseOneByteXOR()
* A suite of tests for these methods




