import cryptography
import itertools
from itertools import cycle
from codecs import encode, decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from os import urandom

BLOCK_SIZE = 16 # Bytes
message = b'abcdefghiklmno'
# key = urandom(BLOCK_SIZE)
key = b'YELLOW SUBMARINE'
suffixe = b'z'

def pkcs7_pad(message, block_size):
    padding_size = (block_size - len(message)) % block_size
    if padding_size == 0:
        padding_size = block_size
    padding = (chr(padding_size) * padding_size).encode()
    return message + padding

def encrypt(key, message):
    cipher = Cipher(algorithms.AES(key), mode=modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor() 
    return encryptor.update(pkcs7_pad(message, BLOCK_SIZE)) + encryptor.finalize()

# Why is AES-ECB-128 considered insecure ?

# This is mainly because blocks containing the same data will be encrypted in the same way
# So this is easy to "guess" data containing in some blocks

# How many attempts (in worst case) in order to brute force the key ?

# Since the key is coded in 128-bits, there 3.4 * 10^38 possibilities

def oracle(message, suffixe):
    return encrypt(key, message + suffixe)

message_oracle = oracle(message, suffixe)

def decrypt_oracle(message, decrypt):
    if (len(message) == 0):
        print("decrypted message :")
        print(decrypt)
        return
    for i in range(256):
        if (encrypt(key, message + bytes([i]) + decrypt) == message_oracle):
            temp = bytes([i]) + decrypt
            break
    decrypt = temp
    decrypt_oracle(message[0:len(message) - 1], decrypt)

# decrypt_oracle(message, b'')

# What does the IND-CPA definition say ?

# It says that a cryptosystem is considered secure in terms of indistinguishability if given a ciphertext randomly chosen from a 2 elements message space
# no adversary can determine the real message with a probability much better than 1/2

# Is AES used in this mode IND-CPA ?

# No because since blocks containing the same data have the same encryption. It is possible to determine or at least to guess a part of the message

def fast_modular_exponentiation(x, power, modulo):
    arr_of_2s_of_power = bin(power)[2:]
    res = 1
    for i in range(len(arr_of_2s_of_power) - 1, -1, -1):
        res = (res * x ** int(arr_of_2s_of_power[i])) % modulo
        x = (x ** 2) % modulo
    return res

# for i in range(100000, 1234567):
#     print(fast_modular_exponentiation(259, i, 19))