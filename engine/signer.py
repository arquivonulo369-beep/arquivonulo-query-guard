import hashlib
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey
)
from cryptography.hazmat.primitives import serialization


PRIVATE_KEY_PATH = Path("security/keys/private_key.pem")
PUBLIC_KEY_PATH = Path("security/keys/public_key.pem")


def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(
            f.read()
        )


def sign_data(data: bytes) -> str:
    private_key = load_private_key()
    signature = private_key.sign(data)
    return signature.hex()


def verify_signature(data: bytes, signature_hex: str) -> bool:
    public_key = load_public_key()
    try:
        public_key.verify(bytes.fromhex(signature_hex), data)
        return True
    except Exception:
        return False


def get_pubkey_fingerprint() -> str:
    public_key = load_public_key()

    raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    return hashlib.sha3_384(raw).hexdigest()

