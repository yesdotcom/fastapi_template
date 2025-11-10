# (WIP) fastapi endpoint template by @panado, 2025

Message payloads are encrypted using AES, not necessary if this is being run behind HTTPS.
The API secret makes use of a HMAC shared secret (symmetric key) to ensure message integrity of incoming requests.
