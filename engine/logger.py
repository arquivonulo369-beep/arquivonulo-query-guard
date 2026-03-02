import json
import os
import hashlib
from .config import LOG_PATH
from .signer import sign_data

def canonical_serialize(entry: dict) -> bytes:
    return json.dumps(entry, sort_keys=True, separators=(',', ':')).encode('utf-8')

def compute_entry_hash(entry: dict) -> str:
    serialized = canonical_serialize(entry)
    return hashlib.sha3_384(serialized).hexdigest()

def get_last_hash(log_path: str) -> str:
    if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
        return "genesis"

    with open(log_path, "r", encoding="utf-8") as f:
        last_line = f.readlines()[-1].strip()

    if not last_line:
        return "genesis"

    last_entry = json.loads(last_line)
    return last_entry.get("entry_hash", "genesis")

def log_result(data: dict, log_path: str = LOG_PATH):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # 1️⃣ Encadeamento
    previous_hash = get_last_hash(log_path)
    data["previous_hash"] = previous_hash

    # 2️⃣ Calcula hash determinístico (sem signature)
    entry_hash = compute_entry_hash(data)
    data["entry_hash"] = entry_hash

    # 3️⃣ Assina os dados canônicos (incluindo entry_hash, mas sem signature)
    serialized = canonical_serialize(data)
    signature = sign_data(serialized)
    data["signature"] = signature.hex()

    # 4️⃣ Grava em NDJSON determinístico
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(',', ':')) + "\n")

    return entry_hash

import os

LOG_DIR = "logs"


def load_log_hashes():
    """
    Returns list of log leaf hashes ordered deterministically.
    Each file in logs/ must contain a single SHA3-384 hash.
    """
    if not os.path.exists(LOG_DIR):
        raise Exception("logs/ directory not found")

    files = sorted(os.listdir(LOG_DIR))

    hashes = []

    for filename in files:
        path = os.path.join(LOG_DIR, filename)

        if os.path.isfile(path):
            with open(path, "r") as f:
                value = f.read().strip()
                if value:
                    hashes.append(value)

    return hashes

