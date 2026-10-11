# FOX2 — Vietnam Equities Investment Intelligence

Independent greenfield project for Vietnamese equity investment intelligence.

- **Current phase:** M0 — Product Foundation (Git bootstrap and first released-document mirror verified; M0 overall remains in progress).
- **M1 target:** Offline localhost MVP, subject to a separate scoped DEV authorization and acceptance gates.
- No broker order execution, margin, or live trading.

## Released document authority and Git mirror

The authoritative **released** Policy and BRDs are in the FOX2 Library at `/Trading/FOX2/`; Git is an **exact-content technical mirror**, not a place for Agents to approve or edit canonical BRDs.

Verified files on Git `main`:
- `docs/governance/FOX2_POLICY_V1.0.md`
- `docs/governance/FOX2_POLICY_V1.0_RELEASE_MANIFEST_20261011.json`
- `docs/brd_mirror/FOX2-BRD-00_v0.2.md`
- `docs/brd_mirror/FOX2-BRD-00_v0.2_RELEASE_RECEIPT_20261011.json`

The original immutable document-mirror commit is `60892265d752d773829139c50039f9d81530e849`. After any new Git commit, use the actual approved **full commit SHA** for each Agent handoff; do not treat the moving `main` label as an immutable source identity.

**BRD-00 v0.2** is the only Owner-approved/published BRD as of 2026-10-11. BRD-01..08 remain Candidates outside the released Git mirror. The released BRD-00 raw SHA-256 is `adf043885d4759b72cbd9fd161d8b5762af725495b5cbc59c5858df1f4cf4bf4` (9,498 bytes).

For every material BRD-based handoff, the receiving Agent must independently read the released Library file and the Git file at the pinned full commit, verify revision, receipt, raw byte count and SHA-256 match, and report evidence. A previous Agent's PASS does not replace that readback. Missing source access or mismatch means **STOP**. Source binding or presence on `main` does not grant DEV, merge, provider access, order-write or LIVE.
