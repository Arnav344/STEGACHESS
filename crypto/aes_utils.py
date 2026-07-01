from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import base64
import os


def generate_aes_key(user_key):

    return hashlib.sha256(
        user_key.encode()
    ).digest()


def encrypt_message(message, user_key):

    aes_key = generate_aes_key(user_key)

    iv = os.urandom(16)

    cipher = AES.new(
        aes_key,
        AES.MODE_CBC,
        iv
    )

    encrypted_bytes = cipher.encrypt(
        pad(
            message.encode(),
            AES.block_size
        )
    )

    final_bytes = iv + encrypted_bytes

    encrypted_base64 = base64.b64encode(
        final_bytes
    ).decode()

    return encrypted_base64


def decrypt_message(encrypted_text, user_key):

    aes_key = generate_aes_key(user_key)

    encrypted_bytes = base64.b64decode(
        encrypted_text
    )

    iv = encrypted_bytes[:16]

    ciphertext = encrypted_bytes[16:]

    cipher = AES.new(
        aes_key,
        AES.MODE_CBC,
        iv
    )

    decrypted = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

    return decrypted.decode()