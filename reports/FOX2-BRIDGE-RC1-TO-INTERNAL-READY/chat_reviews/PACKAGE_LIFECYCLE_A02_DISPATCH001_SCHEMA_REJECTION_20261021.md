# FOX2 — A02 Dispatch001 Schema Rejection

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A02`

## Candidate Dispatch

ID:
`FOX2-DISPATCH-BRIDGE-RC1-PACKAGE-LIFECYCLE-A02-CODEX-001`

Publication commit:
`e4a58760efba32c4f4da5f6d82b9421354ef349e`

Blob:
`f40b925702395de83f750f5cc86c5fd5a4abdfa9`

## Validation

Current Dispatch Schema v3:
- path: `docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v3.json`
- release source: `d34da1e3b4918a902646621b487ca8ad3e05b0e0`
- blob: `1692061941e2bef498515cd0e96b9b3046119ebb`

The schema sets:
`runtime_contract.additionalProperties=false`

and permits only:
- repo
- branch
- worktree
- base_sha
- allowed_code_paths
- allowed_report_paths
- required_capabilities
- stop_conditions

Dispatch001 added three non-schema fields:
- `product_source_base_sha`
- `previous_consumed_dispatch`
- `previous_consumed_dispatch_replay_forbidden`

Therefore Dispatch001 is invalid and MUST NOT be executed.

## State

- Agent started: false
- Dispatch consumed: false
- task branch unchanged at A02 PreExec PASS runtime base
- no product code changed
- no host lifecycle mutation

## Correct representation

Product source baseline is already represented by schema-valid:
`source.commit_sha=b065a468279cbf63ae4bbfad7a0efaad1e6046e4`.

Executable starting HEAD is represented by:
`runtime_contract.base_sha=036de99a6d649bfcf9a427aa914809a9d53592c3`.

Historical A01 no-replay can be expressed in `decision_receipt.dev_grant_ref` and `runtime_contract.stop_conditions`, without adding schema fields.

## Verdict

`HOLD — PUBLISHED_INVALID_NOT_EXECUTABLE`

Do not update/rebind this published identity. Issue a fresh schema-valid A02 Dispatch identity instead.
