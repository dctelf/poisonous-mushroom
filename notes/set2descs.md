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

## <a name="challenge12" /> Byte-at-a-time ECB decryption (Simple)

[challenge 12](https://cryptopals.com/sets/2/challenges/12)

Probably easiest to read the full challenge description on the site rather than summarise here...

### Approach:

* Created a script "aes_ecb_oracle_decrypt.py"

Initial stage - determine keylength

* first time round, I did this in an effective but slightly convoluted fashion
* to detect block size - I knew that valid AES options are: 128, 192 and 256  bits (16, 24 and 32 bytes respectively)
* I basically tried each potential keylength from longest to shortest
* then, assuming it was an ECB encrypted string, fed the oracle a ptext string of 4 * blocklen
* I then detected whether the 2nd and 2rd blocks of blocklen were identical
* thus identifying both ECB & the blocklen in one cycle
* I guess this was efficient (it only calls the oracle once per blocklen and bails out when it finds a match)
* issue is, the method isn't reusable and only works for ECB mode.
* I didn't follow the challenge guidance, but having re-read it and looked at another solution, there is an alternate approach
* for reference, original code below:

```python
for blocklen in 32, 24, 16:
    test_block_ba = bytearray((4 * blocklen * "A"), 'utf-8')
    test_ctext = ciphers.aes128ecb_enc_oracle(test_block_ba)
    if test_ctext[blocklen:2*blocklen] == test_ctext[2*blocklen:3*blocklen]: break
```            

```
# pass 0 - block 0 ##
so we feed in "AAA" so oracle encrypts:
[AAAX][BCDE][FGHI][JKLM][N~pad~~pad~~pad~]
we keep this ciphertext for comparison
then we feed in "AAA-chr(0-255)-" so oracle encrypts:
[AAA-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
we compare each iteration with the kept ctext from above
if the first block matches, we know that the first oracle added character is one of the values,
in this instance X
# pass 1 - block 0
we feed in "AA" and know the next char is X so oracle encrypts
[AAXB][CDEF][GHIJ][KLMN]  <- note, 1 block less - would be a full padded block otherwise
we keep this ciphertext for comparison
then we feed in "AAX-chr(0-255)-" so oracle encrypts:
[AAX-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
we compare each iteration with the kept ctext from above
if the first block matches, we know that the second oracle added character is one of the values,
in this instance B
# pass 2 - block 0
we feed in "A" and know the next chars are XB so oracle encrypts
[AXBC][DEFG][HIJK][LMN~pad~]  <- note, 1 block less - would be a full padded block otherwise
we keep this ciphertext for comparison
then we feed in "AXB-chr(0-255)-" so oracle encrypts:
[AXB-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
we compare each iteration with the kept ctext from above
if the first block matches, we know that the third oracle added character is one of the values,
in this instance C

# pass 3 - block 0
we feed in "" and know the next chars are XBC so oracle encrypts
[XBCD][EFGH][IJKL][MN~pad~~pad~]  <- note, 1 block less - would be a full padded block otherwise
we keep this ciphertext for comparison
then we feed in "XBC-chr(0-255)-" so oracle encrypts:
[XBC-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
we compare each iteration with the kept ctext from above
if the first block matches, we know that the fourth oracle added character is one of the values,
in this instance D
######
## we now know the first block in entirety - onto the second block
######
# pass 0 - block 1
so we feed in "AAA" so oracle encrypts:
[AAAX][BCDE][FGHI][JKLM][N~pad~~pad~~pad~]
note that we are focussing attention on the second block now
we know from this 'new' second block that the first 3 chars are "BCD"
we keep this ciphertext for comparison
then we feed in "BCD-chr(0-255)-" so oracle encrypts:
[BCD-chr(0-255)-][XBCD][EFGH][IJKL][MN~pad~~pad~]
we compare each iteration with the kept ctext from above
if the first block of this matches the second block above, we know that the 5th oracle added character is
in this instance E

and repeat
```
