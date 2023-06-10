from datetime import datetime
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
encrypted_string = "dpuY83svYbHnw1HVfNVByg=="
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
from concurrent.futures import ThreadPoolExecutor
import threading

def encrypt_string(text, key_bytes, iv):
    # Convert the key from Base64 to bytes
    # key_bytes = base64.b64decode(key_base64)
    
    # Initialize the AES cipher with the key and mode
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(initialization_vector=iv), backend=default_backend())
    
    # Create a padder for PKCS7 padding
    padder = padding.PKCS7(128).padder()
    
    # Pad the input text
    padded_data = padder.update(text.encode('utf-8')) + padder.finalize()
    
    # Create an encryptor object
    encryptor = cipher.encryptor()
    
    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Convert the encrypted data to hexadecimal representation
    encrypted_hex = binascii.hexlify(encrypted_data).decode('utf-8')
    print(f"Text: {text}, Encrypted:{encrypted_data}")
    return encrypted_hex
    
    # return encrypted_hex

# Example usage
# text = "Hello, world!"
# key_base64 = "s6dh48RwaD8SDybjg12bqA=="
for i in range(500000000):
    text = f"{i}"
    output = encrypted_text = encrypt_string("123456789", key_bytes, text)
    # if text.startswith("4"):
    #     if(output == hex_encrypted_string):
    #         break
# print("Encrypted text (hex):", encrypted_text)


# # Assume a default IV of all zeros
# iv = b'\x00' * 16
# def run_n_times(start, end):
#     print(f"Running Between {start} and {end}")
#     for key in range(start, end):
#         try:
#             # print(key)
#             # print(val, key)

#             val = format(int(key), "b").rjust(128, "0")
#             val = bytes(int(val[i:i+8], 2) for i in range(0, len(val), 8))
#             # Create a Cipher object with AES-128 algorithm, CBC mode, and PKCS7 padding
#             cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(key_bytes), backend=default_backend())

#             # Create a decryptor object from the Cipher
#             decryptor = cipher.decryptor()

#             # Decrypt the data
#             decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

#             # Remove padding from the decrypted data
#             unpadder = padding.PKCS7(128).unpadder()
#             decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()
#             print(val, key, decrypted_data.decode())
#             break
#         except:
#             pass
#             continue
# start = 0
# key = 0
# print(2**128)
# start_time = datetime.now()
# run_n_times(0, 1000000)
# print(f"{datetime.now() - start_time}")
# def mainfun():
#     with ThreadPoolExecutor(500) as pool:
#         while key < (2 ** 128):
#         # for key in range(2, 7):
#                 old = key
#                 key = key + 1000
#                 pool.submit(run_n_times, old, key)
#                 # t = threading.Thread(target=run_n_times, args=(old, key))
#                 # t.daemon = True
#                 # t.start()
#     # Print the decrypted data
