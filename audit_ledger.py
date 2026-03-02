import json
import hashlib
import argparse
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


def canonical_serialize(entry: dict) -> bytes:
    return json.dumps(entry, sort_keys=True, separators=(',', ':')).encode('utf-8')


def compute_hash(entry: dict) -> str:
    return hashlib.sha3_384(canonical_serialize(entry)).hexdigest()


def load_public_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def audit_ledger(ledger_path: str, public_key_path: str):
    public_key = load_public_key(public_key_path)
    previous_hash = "genesis"
    line_number = 0

    with open(ledger_path, "r", encoding="utf-8") as f:
        for line in f:
            line_number += 1
            entry = json.loads(line.strip())

            signature_hex = entry.pop("signature")
            stored_hash = entry.pop("entry_hash")

            # 1️⃣ Verificar hash
            computed_hash = compute_hash(entry)
            if computed_hash != stored_hash:
                print(f"❌ Linha {line_number}: Hash inválido")
                return False

            # 2️⃣ Verificar encadeamento
            if entry["previous_hash"] != previous_hash:
                print(f"❌ Linha {line_number}: Chain quebrada")
                return False

            # 3️⃣ Verificar assinatura
            try:
                public_key.verify(bytes.fromhex(signature_hex),
                                  canonical_serialize({**entry, "entry_hash": stored_hash}))
            except InvalidSignature:
                print(f"❌ Linha {line_number}: Assinatura inválida")
                return False

            previous_hash = stored_hash
            print(f"✔ Linha {line_number} OK")

    print("\n✅ Ledger íntegro e verificável.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--pubkey", required=True)
    args = parser.parse_args()

    audit_ledger(args.ledger, args.pubkey)

