# FOX2 — CHAT Preflight Intake — Presentation Lock Certifier Rework R3 PASS_TO_ASSIGN

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Whole feature stage: `TEST / IN_PROGRESS`
Residual task stage: `BUILD correction inside TEST`
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3`

## Verdict

**PASS_TO_ASSIGN — R3 CERTIFIER CORRECTION ONLY**

CHAT may publish exactly one fresh executable Dispatch:

`FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-CODEX-001`

This verdict does not certify the coding result and does not authorize A05 host lifecycle, G3, G4, Canary, main, PR, merge, provider, broker or LIVE.

## Route assessment

FOX2 Skills v0.3.7 task-level assessment:

- `COMPLEXITY=MEDIUM`
- `EXECUTION_RISK=MEDIUM`
- `SAFETY_OVERRIDE=NO`
- Actor: `CODEX`
- Model: `gpt-6.1-sol`
- Thinking: `medium`
- Permission profile: `FULL_ACCESS`, bounded by exact task paths

PreExec verifies this selected route; it does not choose or upgrade the route.

## Immutable task and prompt

Task:
- commit: `c5b8ccef94fc222bc2626209c74c074b827269f3`
- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r3/task.md`
- blob: `e66f8fc39add4024de3b242771d171e9b6b5bec3`
- SHA-256: `4dde2215f4095f26caa00bb6c0254cfb421d3d5d21086e5c1b6769b197acec5e`

Prompt:
- commit: `aed565cd230ccea9f7b8353ed72820c616985fd9`
- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r3/prompt.md`
- blob: `aee25625c67abf1a4ec5b8aa1cda22e517214a8e`
- SHA-256: `44f0138cf10ae96de0392d84f11b5151ad85496fa93d64aa056a3316ad42d75c`

Accepted Bridge product source remains:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

R3 is an external-certifier correction and does not create a new runtime package subject.

## PreExec v4 acceptance

PreExec v4 publication:
`4bdbe33ebcb0d03f261a7870f9e364a67f1fdfd7`

Remote receipt commit:
`7fcdfd19e0d9177b4d85e39fd249b5e65ccc0d49`

Receipt:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/presentation_lock_certifier_rework_r3_v4.json`
- blob: `8c21474702cf5160c37c14f43bce50e3c0089d8b`
- SHA-256: `722a53f840ce868bb8a2e59504c26ce56e9f925f9ab1bdc3921e1fa626608843`

CHAT independent intake:
- publication → receipt: exactly one commit ahead;
- changed path: receipt only;
- current Receipt Schema v1 blob: `25fe465f82a16edf29ebf773a220969192f546e8`;
- schema validation: PASS / 0 errors;
- receipt status: PASS;
- blockers: none;
- candidate route: `CODEX / PINNED / gpt-6.1-sol / medium / FULL_ACCESS`;
- Python test runner: Python 3.13 / pytest 8.3.5 / jsonschema 4.26.0;
- CODEX CLI: 0.162.1;
- selected Medium capacity probe: PASS;
- one-writer: PASS;
- Git push permission: PASS;
- executable R3 Dispatch: absent at intake;
- Agent execution started: false;
- product code drift before coding: none;
- package/Bridge host mutation: none.

## Historical recovery preserved

- PreExec v1 `ba9b8eda7de3c2aa53cf0e7aeee3249f60780b13`: BLOCKED test-Python binding defect; do not rerun.
- PreExec v2 receipt `5319554547aeb03b9a3faf8970794f21c9f97cb7`: material probes passed but receipt schema-invalid; do not use for assignment.
- PreExec v3 `c06a8ab9d1ca84a1bef41da354de5c3ea876a620`: read-only governance fetch failure; no receipt/Dispatch/Agent; do not rerun.
- PreExec v4 receipt above is the first schema-valid PASS receipt for R3.

No historical FAIL/BLOCKED is rewritten to PASS.

## Allowed code/test scope

Exactly:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Allowed result/evidence paths:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r3/**`

No third product/test file.

## Required execution behavior

CODEX must:
1. remotely verify exact task/prompt/receipt/PASS_TO_ASSIGN/Dispatch identities before editing;
2. preserve A04 reusable PASS evidence;
3. change only the two allowed code/test files;
4. run focused lifecycle-WPF-contract tests;
5. run full `agent_bridge/tests`;
6. run `git diff --check`;
7. produce changed-path allowlist, secret/privacy scan and K1 hunk classification with `UNEXPLAINED=0`;
8. commit/push result/evidence under the result contract;
9. return observed remote result SHA outside the committed report.

## Explicitly forbidden

R3 MUST NOT:
- rebuild the A04 package;
- install/update/uninstall/reinstall Bridge;
- launch/exit WPF for real host lifecycle;
- mutate current Bridge host state;
- touch Worker/F1;
- open A05 lifecycle execution;
- enable G3/G4/Canary;
- create PR or merge;
- touch main;
- provider/broker/LIVE.

## Assignment decision

CHAT may now publish exactly one fresh R3 CODEX Dispatch with:

- `CODEX`
- model `gpt-6.1-sol`
- reasoning `medium`
- `FULL_ACCESS` execution profile bounded by task
- `MANUAL_LOCAL`
- runtime base `7fcdfd19e0d9177b4d85e39fd249b5e65ccc0d49`
- accepted source `085cc8302e824dbccf9cbef80422ed48894b9cb4`
- max_runs = 1
- code push allowed only for the two allowed code/test files
- report/evidence push allowed only under exact R3 result paths
- no replay if Dispatch is consumed

Agent completion is at most `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

A05/G3/G4/Canary remain locked.
