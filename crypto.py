import secrets

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class CipherError(Exception):
    def __init__(self, message='This key cannot decrypt the file.'):
        self.message = message
        super().__init__(self.message)


class KeyLengthError(Exception):
    def __init__(self, message='Invalid key.'):
        self.message = message
        super().__init__(self.message)


def generate_key() -> bytes:
    return secrets.token_urlsafe(36).encode()


def validate_key(src_file_path: str, key: bytes) -> bool:
    with open(src_file_path, 'rb') as file:
        data_file = file.read()
    verificator, accounts = data_file.split(b'<0>')

    try:
        decrypt_bytes(verificator, key)
        return True
    except CipherError or ValueError:
        return False


def decode_key(full_key: bytes) -> tuple[bytes, bytes]:
    return full_key[:32], full_key[32:]


def pad_key(key: bytes) -> bytes:
    if not len(key) == 48:
        if len(key) < 48:
            user_key = f'{key:a<48}'
        else:
            user_key = key[:48]

    return key


def encrypt_str(plain_text: str, encryption_key: bytes) -> bytes:
    if len(encryption_key) != 48:
        raise KeyLengthError

    key, iv = decode_key(encryption_key)

    # Convert plaintext to bytes
    plain_text_bytes = plain_text.encode('utf-8')

    # Pad the plaintext
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plain_text = padder.update(plain_text_bytes) + padder.finalize()

    # Create AES-256 cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded plaintext
    cipher_bytes = encryptor.update(padded_plain_text) + encryptor.finalize()

    return cipher_bytes


def decrypt_bytes(cipher_text: bytes, full_decryption_key: bytes) -> str:
    # Ensure the key is 32 bytes (256 bits) and IV is 16 bytes (AES block size)
    if len(full_decryption_key) != 48:
        raise KeyLengthError

    decryption_key, iv = decode_key(full_decryption_key)

    try:
        # Create AES-256 cipher in CBC mode for decryption
        cipher = Cipher(algorithms.AES(decryption_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the ciphertext
        padded_plain_text = decryptor.update(cipher_text) + decryptor.finalize()

        # Unpad the plaintext to get the original message
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plain_text_bytes = unpadder.update(padded_plain_text) + unpadder.finalize()

        # Convert bytes back to string
        return plain_text_bytes.decode('utf-8')
    except ValueError:
        raise CipherError


if __name__ == '__main__':
    KEY = generate_key()
    print(KEY)
    text = 'Beautiful is better than ugly.'
    text_en = encrypt_str(text, KEY)
    print(text)
    print(text_en)
    text_de = decrypt_bytes(text_en, KEY)
    print(text_de)
