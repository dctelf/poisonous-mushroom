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
* created a test to validate that when I used my method to encrypt and decrypt, the PyCrypto routine also decrypted my ctrext to the real ptext - which it did....

Yaaaaaasssssssss :)

## <a name="challenge11" /> An ECB/CBC Detection Oracle

[challenge 11](https://cryptopals.com/sets/2/challenges/11)

Write a function that encrypts a given string with either ECB or CBC mode, both pre and suffixing the plain text with a random set of bytes (between 5 and 10 bytes at either end).  Use a random key (and for CBC mode a random iv) then AES encrypt as appropriate, randomly icking either mode.

Then, write a function that calls this prior function with a plaintext string crafted to allow detection of the mode (CBC or ECB).

### Approach:

* Created the following methods in the cryptochallenge.ciphers module
    * aes128_encryption_oracle()
    * detect_aes128_ecbcbc()
* Used a unittest rather than building up a full script to invoke these methods
* Smpler than expected - ensure the plaintext is long enough to have 2 * repeating 16 byte blocks in the middle neither imapcted by the random bytes at the start or end (so, at least 4 * 16 byte blocks)
* make the plaintext all repeat - I used "A"s but any value will do
* the ECB mode is the one with the repeating cipher text, by process of elimination the CBC mode is the other one

