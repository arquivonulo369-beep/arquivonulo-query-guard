# Reproducibility and Verification
ArquivoNulo Global
Normative Operational Guidance

Status: Active
Category: Verification Standard

---

## 1. Purpose

This document defines the reproducibility and verification
procedures required to independently validate the integrity
of the QueryGuard repository state.

This guidance enables third-party auditability without
requiring trust in the original authors.

---

## 2. Repository Integrity Verification

To verify repository integrity:

1. Clone the repository from its canonical source.
2. Ensure the branch matches the declared canonical state.
3. Obtain the current commit hash using:

   git rev-parse HEAD

4. Compute the SHA3-384 hash of the commit reference:

   git rev-parse HEAD | tr -d '\n' | openssl dgst -sha3-384

5. Compare the resulting digest with the declared canonical anchor
   in STATE_CONSOLIDATION_v1.0.1 (or latest declared state).

Mismatch MUST be treated as integrity failure.

---

## 3. Deterministic Log Verification

To verify deterministic logging:

1. Reproduce identical input conditions.
2. Execute logging pipeline.
3. Confirm generated entry hashes match SHA3-384 outputs.
4. Validate ordering consistency.

Any divergence invalidates deterministic compliance.

---

## 4. Merkle Root Reproduction

1. Recompute individual log entry hashes.
2. Reconstruct the Merkle tree in deterministic order.
3. Compute Merkle root using SHA3-384.
4. Compare root against snapshot root.

Roots MUST match exactly.

---

## 5. Snapshot Signature Validation

1. Extract snapshot signature.
2. Verify using Ed25519 public key.
3. Confirm signature authenticity prior to accepting snapshot.

Invalid signature MUST invalidate the snapshot.

---

## 6. Replay Determinism Test

An implementation MUST support replay validation:

- Replaying the same log inputs MUST produce
  identical Merkle roots.
- Repeated verification cycles MUST yield identical results.

Non-deterministic behavior indicates protocol violation.

---

## 7. External Audit Conditions

An external auditor SHOULD verify:

- Cryptographic primitive conformity
- Hash function correctness (SHA3-384)
- Signature scheme compliance (Ed25519)
- Absence of mutable log operations

Auditors MAY use independent cryptographic libraries
to confirm results.

---

## 8. Canonical Verification Principle

Verification MUST rely on:

- Publicly reproducible commands
- Deterministic execution
- Cryptographic comparison

Trust is replaced by reproducibility.

---

End of Verification Standard
ArquivoNulo Global
Deterministic Governance Layer

