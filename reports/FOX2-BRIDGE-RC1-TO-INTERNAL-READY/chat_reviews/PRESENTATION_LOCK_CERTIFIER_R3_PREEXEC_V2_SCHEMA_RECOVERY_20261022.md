# FOX2 — Presentation Lock Certifier R3 PreExec v2 Schema Recovery

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3`

## Observed v2 delivery

PreExec v2 publication:
`39f0993c62896c576c03fd9ed4694b1101004f82`

Remote receipt commit:
`5319554547aeb03b9a3faf8970794f21c9f97cb7`

Receipt:
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/presentation_lock_certifier_rework_r3_v2.json`

Receipt blob:
`b2de022ea3f65f9062d7c24e0a7535bf8f958ed6`

Raw SHA-256:
`154d82f91c0f2d5b0f5f609ad42a449f7b8ab0be2bf99ec52a4a239af6a050eb`

The receipt commit is exactly one commit after v2 publication and changes only the receipt path.

## FIRST_FAILURE

CHAT Preflight Intake validated the delivered receipt against the Dictionary-resolved current contract:

`docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json`

Schema blob:
`25fe465f82a16edf29ebf773a220969192f546e8`

The receipt contains:

`candidate_route.model_policy = "TASK_ROUTE_ASSESSMENT_SELECTED"`

but Receipt Schema v1 permits only:

- `PINNED`
- `NATIVE_AUTO`
- `CURRENT_CONFIG`
- `PINNED_PREFERRED`

Therefore the v2 receipt is **schema-invalid** even though its material host probes passed.

## Evidence preserved from v2

Observed material checks remain factual and reusable where freshness is not invalidated:

- source/task/prompt binding: PASS;
- R3 route assessment: MEDIUM / MEDIUM risk / no safety override;
- selected route: CODEX / `gpt-6.1-sol` / `medium`;
- existing Python 3.13 test runner: PASS;
- pytest 8.3.5 / jsonschema 4.26.0: PASS;
- CODEX CLI/auth/capacity: PASS at v2 observation;
- clean dedicated worktree / no competing writer: PASS at v2 observation;
- Git push permission: PASS;
- no package build/install/host mutation: TRUE;
- no executable Dispatch: TRUE;
- Agent execution not started: TRUE.

These PASS observations do **not** make the invalid receipt a valid PreExec receipt.

## Side-effect reconciliation

Current R3 branch after v2:
- remote head: `5319554547aeb03b9a3faf8970794f21c9f97cb7`;
- executable R3 Dispatch: ABSENT;
- Agent start: FALSE;
- code edit: FALSE;
- package build/install/uninstall/reinstall: NOT_RUN;
- Bridge host lifecycle mutation: FALSE;
- G3/G4/Canary: HOLD.

No executable attempt was consumed.

## Verdict

`RECOVERED / PREEXEC_V2_SCHEMA_INVALID / NO_AGENT_SIDE_EFFECT`

Do not use v2 receipt for `PASS_TO_ASSIGN`.

Do not edit or relabel the immutable v2 receipt.

Do not change R3 task/prompt/model/thinking.

## Next safe action

Publish R3 PreExec v3 under the same immutable R3 task/prompt.

v3 must:
1. preserve route `CODEX / gpt-6.1-sol / medium`;
2. encode schema-supported `candidate_route.model_policy="PINNED"`;
3. keep v0.3.7 route-assessment semantics in capability evidence/notes, not by inventing a new schema enum;
4. bind v1 BLOCKED and v2 schema-invalid histories;
5. recheck current one-writer, existing test Python, CODEX auth/capacity and push permission;
6. install/upgrade nothing;
7. publish a fresh receipt only if the current Receipt Schema v1 contract is satisfied.

Historical v1 and v2 states remain factual.
