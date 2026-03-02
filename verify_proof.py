import json
import sys
from engine.merkle import verify_inclusion_proof


def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_proof.py <proof.json>")
        return

    with open(sys.argv[1], "r") as f:
        data = json.load(f)

    valid = verify_inclusion_proof(
        data["leaf"],
        data["proof"],
        data["merkle_root"]
    )

    if valid:
        print("VALID inclusion proof.")
    else:
        print("INVALID proof.")


if __name__ == "__main__":
    main()
