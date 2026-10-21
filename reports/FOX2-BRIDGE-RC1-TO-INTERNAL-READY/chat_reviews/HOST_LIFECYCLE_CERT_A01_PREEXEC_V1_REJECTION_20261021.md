# FOX2 — Host Lifecycle Cert A01 PreExec v1 Rejection

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`

## Artifact

Branch:
`work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021`

Publication commit:
`c1772c9f51f03425c865198329b2740921b6df51`

Path:
`docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/host_lifecycle_cert_a01_preexec.ps1`

Blob:
`d13a6688b65f68c671ed4ea1eb3409b4fa2da203`

## Finding

CHAT remote-readback found the generated PowerShell artifact malformed:
- duplicated execution/receipt blocks;
- duplicated source-binding blocks;
- syntactically broken splice boundaries;
- total size inflated to 955 lines.

The defect was introduced during CHAT artifact transformation. It was detected before Owner execution.

## State

- Owner execution: **NOT_RUN**
- PreExec receipt: **ABSENT**
- CODEX live probe for this artifact: **NOT_RUN**
- Dispatch for host lifecycle task: **NOT_PUBLISHED**
- implementation/host-cert Agent: **NOT_STARTED**
- host mutation: **FALSE**

## Verdict

`HOLD — PUBLISHED_INVALID_NOT_EXECUTABLE`

Do not run, modify, rebind or reuse this PreExec identity.

## Correction

Publish a new immutable PreExec v2 artifact under a distinct path. The new artifact must be written as one coherent script, remote-readback before Owner delivery, and must treat this v1 file as historical non-executable evidence only.
