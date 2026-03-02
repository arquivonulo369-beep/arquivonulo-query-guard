import json
from engine.merkle import sha3_384_bytes
from engine.signer import verify_signature

if __name__ == "__main__":
    # Caminho do snapshot gerado
    snapshot_path = "snapshots/snapshot_20260227-115545.json"

    # Carrega o snapshot
    with open(snapshot_path, "r") as f:
        snapshot = json.load(f)

    # Remover a assinatura para reconstruir o payload
    payload = {k: v for k, v in snapshot.items() if k != "signature"}

    # Serializar deterministicamente o payload
    payload_bytes = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode("utf-8")

    # Verificar a assinatura
    valid = verify_signature(payload_bytes, snapshot["signature"])

    if valid:
        print("✅ Assinatura válida! Snapshot íntegro.")
    else:
        print("❌ Assinatura inválida! Snapshot comprometido.")
    
    # Opcional: Imprimir Merkle Root e outros dados
    print("Merkle Root:", snapshot["merkle_root"])
    print("Fingerprint da chave pública:", snapshot["pubkey_fingerprint"])

