import hashlib
import json
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime

from engine.signer import sign_data, get_pubkey_fingerprint


# =========================================================
# HASH BASE
# =========================================================

def sha3_384_bytes(data: bytes) -> str:
    return hashlib.sha3_384(data).hexdigest()


def hash_pair(left: str, right: str) -> str:
    return sha3_384_bytes((left + right).encode("utf-8"))


# =========================================================
# LEAF HASHES (baseado em entry_hash encadeado)
# =========================================================

def get_leaf_hashes(ledger_path: str) -> List[str]:
    leaves: List[str] = []

    ledger_file = Path(ledger_path)
    if not ledger_file.exists():
        return leaves

    with open(ledger_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            entry = json.loads(line.strip())

            # leaf baseada no entry_hash já encadeado
            leaf_hash = sha3_384_bytes(
                entry["entry_hash"].encode("utf-8")
            )

            leaves.append(leaf_hash)

    return leaves


# =========================================================
# MERKLE ROOT
# =========================================================

def build_merkle_root(leaves: List[str]) -> str:
    if not leaves:
        return "0" * 96  # SHA3-384 vazio

    current_level = leaves[:]

    while len(current_level) > 1:
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])  # duplicação determinística

        next_level: List[str] = []

        for i in range(0, len(current_level), 2):
            parent_hash = hash_pair(
                current_level[i],
                current_level[i + 1]
            )
            next_level.append(parent_hash)

        current_level = next_level

    return current_level[0]


# =========================================================
# INCLUSION PROOF
# =========================================================

def generate_inclusion_proof(
    leaves: List[str],
    index: int
) -> List[Tuple[str, str]]:
    """
    Returns list of (sibling_hash, position)
    position: 'left' or 'right'
    """

    if index < 0 or index >= len(leaves):
        raise IndexError("Invalid leaf index.")

    proof: List[Tuple[str, str]] = []
    current_level = leaves[:]
    idx = index

    while len(current_level) > 1:
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        sibling_index = idx ^ 1
        sibling_hash = current_level[sibling_index]

        position = "left" if sibling_index < idx else "right"
        proof.append((sibling_hash, position))

        # Build next level
        next_level: List[str] = []
        for i in range(0, len(current_level), 2):
            parent_hash = hash_pair(
                current_level[i],
                current_level[i + 1]
            )
            next_level.append(parent_hash)

        idx //= 2
        current_level = next_level

    return proof


def verify_inclusion_proof(
    leaf_hash: str,
    proof: List[Tuple[str, str]],
    root: str
) -> bool:
    computed = leaf_hash

    for sibling_hash, position in proof:
        if position == "left":
            computed = hash_pair(sibling_hash, computed)
        else:
            computed = hash_pair(computed, sibling_hash)

    return computed == root


# =========================================================
# SNAPSHOT GENERATION (ENCadeado + Assinado)
# =========================================================

def generate_snapshot(
    ledger_path: str,
    snapshot_dir: str,
    previous_root: Optional[str] = None
) -> dict:

    snapshot_path_obj = Path(snapshot_dir)
    snapshot_path_obj.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------
    # AUTO-DETECT PREVIOUS SNAPSHOT
    # -----------------------------------------------------

    if previous_root is None:
        snapshot_files = sorted(
            snapshot_path_obj.glob("snapshot_*.json")
        )

        if snapshot_files:
            latest_snapshot_file = snapshot_files[-1]

            with open(latest_snapshot_file, "r", encoding="utf-8") as f:
                latest_snapshot = json.load(f)

            previous_root = latest_snapshot.get("merkle_root", "0" * 96)
        else:
            previous_root = "0" * 96

    # -----------------------------------------------------
    # BUILD CURRENT MERKLE ROOT
    # -----------------------------------------------------

    leaves = get_leaf_hashes(ledger_path)
    merkle_root = build_merkle_root(leaves)

    snapshot_id = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    snapshot = {
        "snapshot_id": snapshot_id,
        "tree_size": len(leaves),
        "merkle_root": merkle_root,
        "previous_root": previous_root,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "pubkey_fingerprint": get_pubkey_fingerprint()
    }

    # -----------------------------------------------------
    # SERIALIZAÇÃO DETERMINÍSTICA PARA ASSINATURA
    # -----------------------------------------------------

    payload = json.dumps(
        snapshot,
        sort_keys=True,
        separators=(',', ':')
    ).encode("utf-8")

    signature = sign_data(payload)
    snapshot["signature"] = signature

    # SAVE
    snapshot_file = snapshot_path_obj / f"snapshot_{snapshot_id}.json"

    with open(snapshot_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    return snapshot

