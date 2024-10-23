from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os


def encrypt_str(plain_text: str, key: bytes, iv: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long.")
    if len(iv) != 16:
        raise ValueError("IV must be 16 bytes long.")

    # Convert plaintext to bytes
    plain_text_bytes = plain_text.encode('utf-8')

    # Pad the plaintext to ensure it's a multiple of the block size (16 bytes)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plain_text = padder.update(plain_text_bytes) + padder.finalize()

    # Create AES-256 cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded plaintext
    cipher_bytes = encryptor.update(padded_plain_text) + encryptor.finalize()

    return cipher_bytes


def decrypt_bytes(cipher_text: bytes, key: bytes, iv: bytes) -> str:
    # Ensure the key is 32 bytes (256 bits) and IV is 16 bytes (AES block size)
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long for AES-256 decryption.")
    if len(iv) != 16:
        raise ValueError("IV must be 16 bytes long.")

    # Create AES-256 cipher in CBC mode for decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_plain_text = decryptor.update(cipher_text) + decryptor.finalize()

    # Unpad the plaintext to get the original message
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_text_bytes = unpadder.update(padded_plain_text) + unpadder.finalize()

    # Convert bytes back to string
    return plain_text_bytes.decode('utf-8')


if __name__ == '__main__':
    text = 'Mam ADHD'
    print(text)
    KEY = os.urandom(32)
    IV = os.urandom(16)
    text_en = encrypt_str(text, KEY, IV)
    print(text_en)
    text_de = decrypt_bytes(text_en, KEY, IV)
    print(text_de)