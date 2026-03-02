import sys
import json
from pathlib import Path

from engine.merkle import (
    get_leaf_hashes,
    build_merkle_root
)

from engine.signer import (
    verify_signature,
    get_pubkey_fingerprint
)


def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_snapshot.py <snapshot_file>")
        sys.exit(1)

    snapshot_file = Path(sys.argv[1])

    if not snapshot_file.exists():
        print("Snapshot file not found.")
        sys.exit(1)

    with open(snapshot_file, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    ledger_path = "logs/query_guard.jsonl"

    # --------------------------------------------------
    # 1️⃣ Rebuild Merkle Root
    # --------------------------------------------------

    leaves = get_leaf_hashes(ledger_path)
    recalculated_root = build_merkle_root(leaves)

    if recalculated_root != snapshot["merkle_root"]:
        print("INVALID: Merkle root mismatch.")
        sys.exit(1)

    # --------------------------------------------------
    # 2️⃣ Verify Fingerprint
    # --------------------------------------------------

    current_fingerprint = get_pubkey_fingerprint()

    if current_fingerprint != snapshot["pubkey_fingerprint"]:
        print("INVALID: Public key fingerprint mismatch.")
        sys.exit(1)

    # --------------------------------------------------
    # 3️⃣ Verify Signature
    # --------------------------------------------------

    payload = {
        "snapshot_id": snapshot["snapshot_id"],
        "tree_size": snapshot["tree_size"],
        "merkle_root": snapshot["merkle_root"],
        "previous_root": snapshot["previous_root"],
        "timestamp": snapshot["timestamp"],
        "pubkey_fingerprint": snapshot["pubkey_fingerprint"]
    }

    payload_bytes = json.dumps(
        payload,
        sort_keys=True,
        separators=(',', ':')
    ).encode("utf-8")

    if not verify_signature(payload_bytes, snapshot["signature"]):
        print("INVALID: Signature verification failed.")
        sys.exit(1)

    print("VALID SNAPSHOT ✓")


if __name__ == "__main__":
    main()

