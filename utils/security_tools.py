import base64
import hashlib
import hmac
import json
import os
from typing import Optional

from Crypto.Cipher import AES
from fastapi import HTTPException, Request

# Type of API Secret:
# https://www.geeksforgeeks.org/computer-networks/what-is-hmachash-based-message-authentication-code/

# Type of payload encryption:
# https://medium.com/@raditya.mit/api-payload-security-encryption-strategies-every-developer-should-know-e9eb051c1ef9


class Verify:
    def __init__(self, secret: Optional[str] = None):
        api_secret = os.getenv("SECRET")
        if not api_secret:
            raise ValueError("SECRET environment variable is not set.")
        self.api_secret = api_secret

    def verify_received_request(self, request: Request, body: bytes) -> bool:
        header = request.headers.get("x-signature")
        if not header:
            raise HTTPException(status_code=400, detail="Missing X-Signature header")

        try:
            parts = dict(part.split("=", 1) for part in header.split(","))
            timestamp = parts["t"]
            signature = parts["s"]
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid signature format")

        message = f"{timestamp}.{body.decode('utf-8')}"
        expected_signature = hmac.new(
            key=self.api_secret.encode("utf-8"),
            msg=message.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            raise HTTPException(status_code=403, detail="Invalid signature")

        return True


class MyEncryption:
    def __init__(self):
        secret = os.getenv("SECRET")
        if secret is None:
            raise ValueError("SECRET environment variable is not set.")
        self.key = hashlib.sha256(secret.encode()).digest()

    def decrypt(self, encrypted: str) -> dict:
        data = base64.b64decode(encrypted)
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return json.loads(decrypted)
