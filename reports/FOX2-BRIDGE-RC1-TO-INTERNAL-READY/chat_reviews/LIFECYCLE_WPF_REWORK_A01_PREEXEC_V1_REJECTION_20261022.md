# FOX2 — Lifecycle/WPF Rework A01 PreExec v1 Rejection

Date: 2026-10-22
Task: `FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01`

Publication:
`544c1a39861966b3d589f692bb8e0b27c6f329c3`

Path:
`docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework/preexec_a01.ps1`

Blob:
`ef329ab0bc5ecf88048734012c0d66e292f84f43`

## Finding

Remote readback found a CODEX probe identity mismatch before Owner execution:

- lingering-probe detection expects prefix `FOX2-lifecycle-wpf-rework-preexec-`;
- temp-probe creation still uses historical prefix `FOX2-package-lifecycle-preexec-`.

This would weaken interrupted-probe attribution/recovery.

## State

- Owner execution: NOT_RUN
- PreExec receipt: ABSENT
- executable Dispatch: NOT_PUBLISHED
- implementation Agent: NOT_STARTED
- product code mutation: FALSE
- real host lifecycle mutation: FALSE
- G3 mutation: FALSE

## Verdict

`HOLD — PUBLISHED_INVALID_NOT_EXECUTABLE`

Do not run or reuse v1.

Publish a fresh v2 under a distinct path, preserving v1 as historical invalid evidence, with exact v1 blob binding and one consistent temp-probe prefix.
