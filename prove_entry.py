import sys
import json
from pathlib import Path
from datetime import datetime

from engine.merkle import (
    get_leaf_hashes,
    build_merkle_root,
    generate_inclusion_proof
)

from engine.signer import (
    sign_data,
    get_pubkey_fingerprint
)


LEDGER_PATH = "logs/query_guard.jsonl"


def main():
    if len(sys.argv) != 2:
        print("Usage: python prove_entry_v4.py <index>")
        sys.exit(1)

    index = int(sys.argv[1])

    leaves = get_leaf_hashes(LEDGER_PATH)

    if not leaves:
        print("Ledger vazio.")
        sys.exit(1)

    if index < 0 or index >= len(leaves):
        print("Index inválido.")
        sys.exit(1)

    merkle_root = build_merkle_root(leaves)

    proof = generate_inclusion_proof(leaves, index)

    timestamp = datetime.utcnow().isoformat() + "Z"

    # Assinatura determinística do payload da root
    payload = json.dumps(
        {
            "merkle_root": merkle_root,
            "timestamp": timestamp
        },
        sort_keys=True,
        separators=(',', ':')
    ).encode("utf-8")

    signature = sign_data(payload)

    output = {
        "index": index,
        "leaf": leaves[index],
        "tree_size": len(leaves),
        "merkle_root": merkle_root,
        "snapshot_timestamp": timestamp,
        "pubkey_fingerprint": get_pubkey_fingerprint(),
        "root_signature": signature,
        "proof": proof
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
