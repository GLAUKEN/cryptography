import cryptography
from codecs import encode, decode

message = b'hello'
print(encode(message, 'hex'))

message_encoded = encode(message, 'hex')
print(decode(message_encoded, 'hex'))