import json
from engine.logger import compute_entry_hash
from engine.config import LOG_PATH


def audit_chain():
    with open(LOG_PATH, "r") as f:
        lines = f.readlines()

    previous_hash = "genesis"

    for index, line in enumerate(lines):
        entry = json.loads(line.strip())

        if entry.get("previous_hash") != previous_hash:
            print(f"Chain broken at entry {index}")
            return False

        previous_hash = compute_entry_hash(entry)

    print("Ledger integrity verified.")
    return True


if __name__ == "__main__":
    audit_chain()
