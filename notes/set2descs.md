## <a name="challenge9" /> Implement PKCS#7 padding

[challenge 9](https://cryptopals.com/sets/2/challenges/9)

Implement PKCS#7 padding

### Approach:

* Didn't bother with an outer script, just created a function in cryptochallenge.stringmanip
* created a test to validate the function

## <a name="challenge10" /> Implement CBC mode

[challenge 10](https://cryptopals.com/sets/2/challenges/10)

Implement CBC mode using ECB mode as the underlying cipher core.  Basically, do the XOR-ing and iv work around AES to implement CBC mode.

### Approach:

* Created the following methods in the cryptochallenge.ciphers module
    * my_ba_aes_cbc128_enc()
    * my_ba_aes_cbc128_dec()
    * Cheated, didn't follow the rules, but later used the PyCrypto library CBC routine wrapped up in lib_ba_aes_cbc128_dec() - just curious as I didn't believe this was "real" crypto :)
* created a test to validate that when I used my method to encrypt and decrypt, the PyCrypto routine also decrypted my ctrext to the real ptext - which it did :)


