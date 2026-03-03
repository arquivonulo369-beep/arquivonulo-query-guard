# QueryGuard Protocol Specification
Draft v0.1
ArquivoNulo Global

Status: Draft
Category: Normative Specification

---

## 1. Introduction

This document defines the normative protocol specification
for QueryGuard as a deterministic governance layer.

This specification is independent of implementation details.
Implementations MUST conform to the requirements defined herein
to be considered protocol-compliant.

---

## 2. Terminology

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY"
are to be interpreted as normative requirement levels.

Deterministic Log:
An append-only sequence of entries whose ordering and content
are fully reproducible given identical inputs.

Snapshot:
A cryptographically anchored representation of the full log state
at a specific point in time.

Inclusion Proof:
A Merkle-based cryptographic proof that a specific entry
exists within a committed snapshot.

---

## 3. System Model

The protocol operates as a pre-execution governance layer.

It enforces structural validation before any agentic
or higher-layer execution is permitted.

The protocol assumes:

- Deterministic input processing
- Cryptographic hashing using SHA3-384
- Ed25519 signature scheme
- Immutable append-only logging

---

## 4. Deterministic Logging Requirements

4.1 Log entries MUST be append-only.

4.2 Each entry MUST be hashed using SHA3-384.

4.3 The log ordering MUST be deterministic and reproducible.

4.4 Log mutation or retroactive modification MUST NOT be permitted.

---

## 5. Merkle Proof Construction

5.1 Snapshots MUST construct a Merkle tree
from ordered log entry hashes.

5.2 The Merkle root MUST be computed using SHA3-384.

5.3 Inclusion proofs MUST allow independent verification
without access to the full log.

5.4 Any mismatch in proof validation MUST invalidate the snapshot.

---

## 6. Signature Requirements

6.1 Snapshots MUST be signed using Ed25519.

6.2 Signature verification MUST occur before accepting a snapshot
as canonical.

6.3 Invalid signatures MUST cause rejection of the snapshot.

---

## 7. Snapshot Integrity Model

7.1 Each snapshot MUST contain:

- Merkle root
- Timestamp
- Signature
- Deterministic reference to prior state (if applicable)

7.2 Snapshot verification MUST confirm:

- Root validity
- Inclusion proof correctness
- Signature authenticity

---

## 8. Security Considerations

The protocol guarantees:

- Tamper-evident logging
- Cryptographic inclusion verification
- Deterministic replay capability

The protocol does NOT guarantee:

- External system integrity
- Runtime behavioral compliance
- Protection against compromised signing keys

Key management security is the responsibility
of the deploying institution.

---

## 9. Compliance Criteria

An implementation is considered QueryGuard-compliant if:

- All MUST requirements are satisfied.
- Cryptographic primitives conform to SHA3-384 and Ed25519.
- Deterministic replay yields identical Merkle roots.
- Snapshot verification rejects altered logs.

---

End of Draft v0.1
ArquivoNulo Global
Deterministic Governance Layer

