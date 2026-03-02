from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from pathlib import Path

PRIVATE_KEY_PATH = Path("security/keys/private_key.pem")
PUBLIC_KEY_PATH = Path("security/keys/public_key.pem")

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# salvar private
with open(PRIVATE_KEY_PATH, "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# salvar public
with open(PUBLIC_KEY_PATH, "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Chaves geradas com sucesso.")

