# FOX2 — CHAT Preflight Intake — Host Lifecycle Cert A02 PASS_TO_ASSIGN

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02`
Stage: TEST / REAL OWNER-HOST PACKAGE LIFECYCLE
Actor: CODEX
Route: `gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL`

## Verdict

**PASS_TO_ASSIGN — HOST LIFECYCLE CERTIFICATION A02 ONLY**

This authorizes publication of exactly one fresh schema-v3 CODEX Dispatch for the re-scoped A02 TEST task. It does not certify the lifecycle result and does not authorize G3/G4/Canary/main/PR/merge/provider/broker/LIVE.

## Accepted product/source baseline

Accepted A02 BUILD result:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

CHAT BUILD acceptance:
`cdf9f9c919102a2337ef357f4b658dc9993f48e5`

No product/source/test changes are authorized by this TEST assignment.

## Current re-scoped task/prompt

Task R2:
- commit: `9ffa283034a4614e5cc5a60899f919e3f12d7a03`
- blob: `6bc93b8fa5e449c48881ebbaa45db5822a12fafa`
- SHA-256: `d0c6b8c3aaae3a72befa65d46d5e1cd81fd4ef062bd1104a6e0132712a06a320`

Prompt R2:
- commit: `292725f6aeeeb211d7d146de5c250b8518adb189`
- blob: `1b04f0be0811acbeebcb54f5ccff9e3d285f68e0`
- SHA-256: `85e5bc7e93ace9f3bae12da732486aace97128337735f7fb6dfcea131b106ec0`

Earlier pre-assignment task/prompt bindings are superseded for future execution only. No Host A02 executable Dispatch existed when R2 was published.

## Historical PreExec states

- v1 publication `db69ce19cda3ec68a73cc3e9c9ad05225f0178eb`: FAILED_PRECONSUME due PowerShell automatic-variable collision; no receipt/Dispatch/Agent/host mutation.
- v2 publication `39b0d5f609d629c9daa29a49751d5720e87d72bb`: BLOCKED_PRECONSUME because one exact-current WPF process was hidden/minimized and UI Automation had no visible top-level window; no receipt/Dispatch/Agent/host mutation.
- v3 publication `db989773b305f0a9453872aa328cc3385cf40286`: hidden/minimized-aware, executed successfully.

Historical failures remain historical and are not relabeled PASS.

## PreExec v3 receipt

Receipt commit:
`76913f36b461689a84e8b4acf57a9ef83a98828d`

Receipt:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/host_lifecycle_cert_a02.json`
- blob: `b00752e2ef1fadb3e50485492261399295f5c88b`
- SHA-256: `43ef8590b8c94bee7697b683578deadff7879cec09f376c5fc15f6038eed6b3f`
- schema: Dictionary-resolved Preflight Receipt v1
- status: PASS
- blockers: `[]`
- receipt ancestry: exactly one receipt-only commit after v3 publication.

CHAT remote-read verified:
- source/task/prompt binding PASS;
- current Governance bytes PASS;
- dedicated worktree clean;
- competing writer NONE_OBSERVED;
- installed host control state STOPPED;
- paused = true;
- setup_complete = true;
- no current dispatch;
- WPF count = 1;
- WPF exact current package = true;
- WPF presentation state = `HIDDEN_OR_MINIMIZED_EXACT_CURRENT`;
- WPF UI inspect = `WINDOW_UNAVAILABLE`;
- main window handle = 0;
- Worker/legacy process count = 0;
- existing isolated build Python PASS;
- dotnet 8.0.426 PASS;
- CODEX CLI 0.162.1 PASS;
- pinned `gpt-6.1-sol/high` live route/auth/capacity PASS;
- Git push dry-run PASS;
- executable Dispatch absent;
- Agent execution not started;
- host lifecycle mutation false;
- G3 false.

The hidden/minimized WPF state is consistent with accepted source semantics: WPF uses explicit shutdown; close/minimize may hide the window while the process remains. PreExec v3 does not surface or close it.

## Current Governance source resolution

- Policy 2.0.0: `96175ac4f39197794a04e695f0046fa7ef9321fe`
- Dictionary 1.3: `b25f7f728de67cf8595bf24f22fcbd79ef50babc`
- Routing Index 1.4.0: `bcd008983b61349646a5198ff243069f81484fae`
- Git-first Protocol v12: `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`
- Preflight Receipt Schema v1 blob: `25fe465f82a16edf29ebf773a220969192f546e8`
- CHAT Preflight Intake v1.1 blob: `e7b7772183c19e58d28d8c9d3851f283a9d9c22a`
- Dispatch Schema v3 blob: `1692061941e2bef498515cd0e96b9b3046119ebb`

Governance document authority does not itself grant runtime rights. This assignment is bounded by the Owner-authorized Whole-WP/task, immutable task/prompt, actual host PreExec PASS and Dispatch permissions.

## R0–R7 / assignment gates

- POLICY_CHECK: PASS
- TASK_STATE_CHECK: PASS
- SOURCE_RESOLUTION: PASS
- R0 task/evidence: PASS
- R1 TEST stage: PASS
- R2 source/authority/risk: PASS
- R3 route/capability: PASS
- R4 actor/cost: PASS — CODEX pinned; WORK not required
- R5 writer/worktree: PASS at PreExec; must recheck immediately before consumption
- R6 Git/result delivery: PASS
- R7 assignment contract: PASS
- ASSIGNMENT_CHECK: PASS
- MATERIAL_CAPABILITY_CHECK: PASS
- TASK-SPECIFIC_PREEXEC: PASS
- NO_REPLAY: PASS
- G3/G4/Canary: HOLD / out of scope

## Authorized runtime behavior

The fresh Dispatch may perform only the task-defined Owner-host TEST lifecycle.

If the one exact-current WPF remains hidden/minimized immediately before execution:
1. re-verify exactly one process, exact current package path and safe paused/setup/no-current-dispatch state;
2. invoke stable `BridgeRoot/launch.ps1` exactly once only to signal the existing singleton show event;
3. require process count remains one and PID/path remain unchanged;
4. require UI inspect to bind that same PID;
5. recheck safe control state;
6. invoke explicit graceful UI exit once;
7. require zero WPF presentations and presentation-lock release.

No force kill and no Worker/F1 fallback.

Only after safe stale-presentation cleanup may the TEST continue with exact package build/install-update, accepted lifecycle certification, stable external uninstall exactly once, exact-package reinstall and final durable-state verification.

## Git write scope

No product/source/test edits.

`permissions.code_allowed=false` and `git_code_push=false` are controlling.

Allowed result writes only:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a02/**`

Schema-v3 legacy field `decision_receipt.code_allowed` remains `YES` only because the schema requires that literal; it does not override `permissions.code_allowed=false`.

## No replay

Never replay:
- `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01-CODEX-001`
- `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-CODEX-001`
- `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-CODEX-001`

Historical Host A01 result remains FAIL/REWORK_REQUIRED.

## Assignment decision

CHAT may now publish exactly one fresh Dispatch:

`FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001`

with:
- target CODEX;
- pinned `gpt-6.1-sol`;
- reasoning `high`;
- FULL_ACCESS execution profile bounded by task;
- execution path `MANUAL_LOCAL`;
- runtime base = `76913f36b461689a84e8b4acf57a9ef83a98828d`;
- accepted product source = `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- max_runs = 1;
- no product/source/test Git writes;
- one-writer/host-state/immutable identity checks immediately before consumption.

Agent completion is at most `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.
