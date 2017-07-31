# poisonous-mushroom: Matasano crypto challenge solutions in python

## Convert hex to base64
[challenge 1](https://cryptopals.com/sets/1/challenges/1)

The string:
```
49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
```
Should produce:
```
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
```

So go ahead and make that happen. You'll need to use this code for the rest of the exercises.

### Rule
Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.

### My approach:

* Script "scripts/conv-hex-to-b64.py" taking single cmd line option of a hex strign and returning to stdout the base64 encoded string
* A new module called stringmanip providing string manipulation methods;
    * hexStringToByteArray()
    * bytearrayToBase64()
    * hexToBase64()
* A suite of tests for each method validating these against the standard python methods
