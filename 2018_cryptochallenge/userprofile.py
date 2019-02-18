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

def admin_profile_for(email):
    # going to intentionally not try to validate the string passed in any way as an email address
    # will escape = and & chars though

    escape_email = email.replace("&", "%26").replace("=","%3D")

    uid = "10"
    role = "admin"

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

def admin_enc_profile_for(email):
    prof_str = kvbuild(admin_profile_for(email))
    return profile_encrypt(prof_str)

def enc_profile_for(email):
    prof_str = kvbuild(profile_for(email))
    return profile_encrypt(prof_str)

def dec_profile_for(encstr):
    profstr_bytes = profile_decrypt(encstr)
    unpad_profbytes = stringmanip.ba_pkcs7_remove(profstr_bytes, 16)
    print(unpad_profbytes)
    plain_str = stringmanip.bytearrayToUTF8Str(unpad_profbytes)
    profobj = kvparse(plain_str)
    return profobj

def profile_encrypt(profile_str):

    str_bytes = bytearray(profile_str, 'utf-8')

    pad_str = stringmanip.ba_pkcs7_pad(str_bytes, 16)

    encstr = ciphers.my_ba_aesecb128_enc(pad_str, config.oracle_enc_key)

    return encstr


def profile_decrypt(str_bytes):

    plain_bytes = ciphers.my_ba_aesecb128_dec(str_bytes, config.oracle_enc_key)

    return plain_bytes