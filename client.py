import base64
import hashlib
import json

from Crypto.Cipher import AES

secret = "my_shared_secret"
key = hashlib.sha256(secret.encode()).digest()


def encrypt(data: dict) -> str:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(json.dumps(data).encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()
