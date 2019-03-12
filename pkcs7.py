message = b'Hello'
block_size = 20

def pkcs7_pad(message, block_size):
    padding_size = (block_size - len(message)) % block_size
    if padding_size == 0:
        padding_size = block_size
    padding = (chr(padding_size) * padding_size).encode()
    return message + padding

print(pkcs7_pad(message, block_size))