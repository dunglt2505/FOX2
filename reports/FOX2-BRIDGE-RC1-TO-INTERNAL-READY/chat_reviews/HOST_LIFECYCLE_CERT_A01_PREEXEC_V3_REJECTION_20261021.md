# FOX2 — Host Lifecycle Cert A01 PreExec v3 Rejection

Date: 2026-10-21
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`

Publication:
`45afc00b621f579202633fe705e2ec6f5ba4b5ed`

Path:
`docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/host_lifecycle_cert_a01_preexec_v3.ps1`

Blob:
`bd246b96709c918d4b7576e763525930d656c56e`

## Finding

V3 fixed source ancestry and historical v1/v2 lineage gates, but remote readback found an attribution mismatch:

- lingering-probe detection searches for prefix `FOX2-host-lifecycle-preexec-`;
- the actual CODEX live-probe temporary directory is still created with historical prefix `FOX2-package-lifecycle-preexec-`.

If a probe were interrupted, the next recovery/readiness check could fail to attribute the lingering process using the identity it expects.

## State

- Owner execution: NOT_RUN
- receipt: ABSENT
- Dispatch: NOT_PUBLISHED
- Agent: NOT_STARTED
- host mutation: FALSE

## Verdict

`HOLD — PUBLISHED_INVALID_NOT_EXECUTABLE`

Do not run or rebind v3.

A fresh v4 must use the same host-lifecycle prefix for both temp-probe creation and lingering-probe detection, preserve the accepted-source/no-product-drift gates, and allow exactly the historical v1/v2/v3 plus current v4 PreExec paths in publication lineage.
