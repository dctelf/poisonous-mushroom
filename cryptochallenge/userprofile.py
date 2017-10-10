#!/usr/bin/python3

from cryptochallenge import ciphers
from cryptochallenge import stringmanip
from cryptochallenge import config
config.oracle_enc_key = ciphers.generate_rand_ba(16)


def kvparse(kvstring):
    pairs = kvstring.split('&')
    obj = {}
    for pairstr in pairs:
        kvpair = pairstr.split("=")
        if len(kvpair) > 0 and kvpair[0] != "":
            obj[ kvpair[0] ] = kvpair[1] if len(kvpair) > 1 else ""
    return obj

def profile_for(email):
    # going to intentionally not try to validate the string passed in any way as an email address
    # will escape = and & chars though

    escape_email = email.replace("&", "%26").replace("=","%3D")

    uid = "10"
    role = "user"

    obj = {
        "email": escape_email,
        "uid": uid,
        "role": role
    }

    return obj


def kvbuild(obj):
    # fucntion to collapse a dictionary into an ampersand joined set of k=v strings
    pairs = []
    for keyval in obj.items():
        pairs.append("=".join(keyval))
    return "&".join(pairs)

def profile_encrypt(profile_str):

    str_bytes = bytearray(profile_str, 'utf-8')

    pad_str = stringmanip.ba_pkcs7_pad(str_bytes, 16)

    encstr = ciphers.my_ba_aesecb128_enc(pad_str, config.oracle_enc_key)

    return encstr

def profile_decrypt(str_bytes):

    plain_str = ciphers.my_ba_aesecb128_dec(str_bytes, config.oracle_enc_key)
    return plain_str