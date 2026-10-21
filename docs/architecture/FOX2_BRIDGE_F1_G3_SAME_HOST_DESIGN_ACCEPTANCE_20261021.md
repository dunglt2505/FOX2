# FOX2 — CHAT Design Acceptance — G3 Same-Host Guarded Enforcement

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`

## Inputs

- Owner physical-host-only directive: `438169d5728a4b5b5da19b737e79db3fc6515ce0`.
- Same-host design candidate: `docs/architecture/FOX2_BRIDGE_F1_G3_SAME_HOST_GUARDED_ENFORCEMENT_CANDIDATE_20261021.md` @ `c8307980362a1ab64b93ba7d7e020d979017c849`.
- Accepted G2 code: `66e8f0a8b3a93140b5f908628b55ac965e15b96e`.
- Historical BLOCKED G3 PreExec receipt: `14a02ab5f42a7659efd2b1e60324c49ff70695b5`.

## Compatibility finding

The accepted isolated-host G2 policy model cannot be safely applied unchanged to the Owner's only Windows host.

Current G2 policy behavior:
- Exe / Script / Msi / Dll collections are always emitted in Enforce mode;
- the canonical validator accepts only the isolated exact-hash model;
- unknown application identities are not covered by an allow rule;
- the HostFence binds one monolithic policy digest.

For a daily-use single host, that model does not provide a host-compatibility baseline and can block unrelated required applications.

## Accepted same-host design

CHAT accepts the candidate design with these mandatory constraints:

1. **Audit-first** before any new enforcement.
2. **Exe + Script** are the mandatory final F1 AppLocker enforcement surfaces.
3. **Msi + Dll are conditional**, not mandatory for same-host G3 without concrete audited need.
4. Preserve a bounded host-safe baseline:
   - Windows/SystemApps;
   - non-user-writable Windows/Program Files paths where justified;
   - reviewed publisher rules;
   - exact hashes for required unsigned host applications.
5. Reject broad trust in user-writable locations.
6. Bind two distinct identities:
   - full expected effective host-policy digest;
   - canonical F1 control-subset digest.
7. HostFence must deny on drift of either identity.
8. Rollback artifacts/state must exist and validate before Enforce.
9. Same physical machine may host both G3 and later G4, but G3 evidence and G4 adoption remain distinct.
10. Historical G2/G3 receipts remain factual and are not replayed/relabelled.

## Required implementation rework

Minimum:
- `f1_policy.py`: composite-policy parsing/canonicalization + F1 subset digest + conditional collection enforcement;
- `f1_service.py`: bind/verify both policy identities;
- policy artifact/generation support;
- focused tests for host-safe baseline, subset drift, collection modes and broad user-writable-path rejection;
- full regression.

No physical-host enforcement is authorized from this design acceptance alone.

## Verdict

**CHAT ACCEPT — SAME-HOST DESIGN REWORK**

This acceptance opens a new BUILD task. It does not reopen G2 A01, does not change the old G3 PreExec from BLOCKED, and does not authorize AppLocker/service host mutation.

NEXT_SAFE_ACTION: new source-bound BUILD task for same-host policy compatibility, then CHAT result review, then a new physical-host PreExec identity.
