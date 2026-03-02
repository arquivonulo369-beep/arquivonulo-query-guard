
import json
from engine.merkle import generate_snapshot

if __name__ == "__main__":
    ledger_path = "logs/query_guard.jsonl"  # Caminho do ledger atual
    snapshot_dir = "snapshots"  # Diretório onde o snapshot será salvo



    # Gerar o snapshot (assinatura ativa)
    snapshot = generate_snapshot(
        ledger_path=ledger_path,
        snapshot_dir=snapshot_dir
    )


    print("Snapshot gerado:")
    print(json.dumps(snapshot, indent=2))

import os
import json

SNAPSHOT_DIR = "snapshots"


def load_latest_snapshot():
    files = sorted(os.listdir(SNAPSHOT_DIR))
    if not files:
        raise Exception("No snapshots found")

    latest = files[-1]

    with open(os.path.join(SNAPSHOT_DIR, latest), "r") as f:
        return json.load(f)
