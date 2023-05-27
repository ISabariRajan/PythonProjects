import binascii
import base64
encryption_key = "90|243|63|133|230|21|195|125|173|249|168|78|251|9|208|31"
# Convert ENC key to bit string
encryption_key = encryption_key.split("|")
print(f"Original KEY: {encryption_key}, {len(encryption_key)}")
new_key = ""
for key in encryption_key:
    bin_val = format(int(key), "b").rjust(8, "0")
    new_key += bin_val 
print(f"Bit Key: {new_key}m {len(new_key)}")
# Convert Bit to byte, then HEX
key_bytes = bytes(int(new_key[i:i+8], 2) for i in range(0, len(new_key), 8))
hex_key = binascii.hexlify(key_bytes).decode()
print(f"Byte Key: {key_bytes}, {len(key_bytes)}")
print(f"Hex Key: {hex_key}, {len(hex_key)}")

print()
encrypted_string = "NIrQMMouQp4BSIcRh622fg=="
print(f"Encrypted String: {encrypted_string}, {len(encrypted_string)} ")
# Base 64 Enc string & its HEX
encrypted_data = base64.b64decode(encrypted_string)
hex_encrypted_string = binascii.hexlify(encrypted_data).decode()
print(f"Base64 Decode Encrypted String: {encrypted_data}, {len(encrypted_data)}")
print(f"Hex Decode Encrypted String: {hex_encrypted_string}, {len(hex_encrypted_string)}")

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

import threading
# AES-128 encrypted data
# encrypted_data = b'TklkDUNseWluZyBBZG1pbg=='

# Base64 decode the encrypted data
# encrypted_data = base64.b64decode(encrypted_data)

# AES-128 key
# key = b'SuperSecretKey123'
key = key_bytes

key_bytes = bytes(int(new_key[i:i+8], 2) for i in range(0, len(new_key), 8))
# Assume a default IV of all zeros
iv = b'\x00' * 16
def run_n_times(start, end):
    for key in range(start, end):
        try:
            # print(key)
            # print(val, key)

            val = format(int(key), "b").rjust(128, "0")
            val = bytes(int(val[i:i+8], 2) for i in range(0, len(val), 8))
            # Create a Cipher object with AES-128 algorithm, CBC mode, and PKCS7 padding
            cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(key_bytes), backend=default_backend())

            # Create a decryptor object from the Cipher
            decryptor = cipher.decryptor()

            # Decrypt the data
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            # Remove padding from the decrypted data
            unpadder = padding.PKCS7(128).unpadder()
            decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()
            print(val, key, decrypted_data.decode())
            break
        except:
            pass
            continue
start = 0
key = 0
while key < (2 ** 128):
# for key in range(2, 7):
        old = key
        key = key + 10000000
        t = threading.Thread(target=run_n_times, args=(old, key))
        t.daemon = True
        t.start()
# Print the decrypted data
