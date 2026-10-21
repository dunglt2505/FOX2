# FOX2 — CHAT Preflight Intake — Host Lifecycle Cert A01 PASS_TO_ASSIGN

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`
Stage: TEST / REAL OWNER-HOST PACKAGE LIFECYCLE
Actor: CODEX
Route: `gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL`

## Governance / source resolution

CHAT remote-read the projectwide Governance Registry and current source resolution on the owner-approved release branch.

Applicable governance remains:
- Policy v2.0.0 / commit `96175ac4f39197794a04e695f0046fa7ef9321fe`
- Dictionary v1.3 / commit `b25f7f728de67cf8595bf24f22fcbd79ef50babc`
- Routing v1.4.0 / commit `bcd008983b61349646a5198ff243069f81484fae`
- Git-first Task/Result Protocol v12 / commit `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`

The Governance Registry itself does not grant executable Agent rights. This assignment remains bounded by the Owner-authorized Whole-WP/task, exact task/prompt, route-specific PreExec PASS and Dispatch permissions.

## Immutable task chain

Accepted source/result base:
`2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`

Task:
- commit: `d95f08ceed2f5a25ad288b9630ffc87b698f329c`
- blob: `86e0afaec6f6e47c9d15b51564a38bf5167a892b`
- SHA-256: `95d64b3cb3999c55700ded2a6451cd9ffa23872fb87fd00c97df7edbb8c06221`

Prompt:
- commit: `250c8ab15bdfd8339e6332dc105a559dbd5b3151`
- blob: `2fd33dbef3fc327ca71844b1e05670b312eefc7d`
- SHA-256: `4a3cab3096b9eca8a65938e5b36d658ceaca5e684def26524ce44cedebe1a689`

PreExec v5 publication:
`27e79ef9266760807187ce90f451ffa26bc97e2f`

PreExec PASS receipt:
- commit: `208de84f39dcf783bd4ee9053c0288cda9aa0024`
- blob: `08056cb73333934a148cef2b4f1f3da11f6b9b3e`

## Historical PreExec states

- v1: rejected before execution, not executable;
- v2: rejected before execution, not executable;
- v3: rejected before execution, not executable;
- v4: executed and BLOCKED before receipt/Dispatch; historical, not reused;
- v5: fresh bound-build-environment identity, PASS with remote readback.

No prior host-lifecycle executable Dispatch exists.

## Remote receipt intake

CHAT independently verified:
- `status=PASS`;
- blockers empty;
- task/prompt exact identity;
- source code base `2faa33f9...`;
- route CODEX / gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL;
- pwsh7/python/git/CODEX login/CLI/one-writer/exact task-prompt/clean worktree/live route PASS;
- host state read-only PASS;
- installed Bridge current package observed;
- control state `STOPPED`;
- `paused=true`;
- setup complete;
- active runtime processes = 0;
- stable external uninstall script observed;
- durable config/database/manual-consumption hashes captured;
- existing isolated build Python accepted and bound by alias;
- Python 3.13 / pip 26.2.1 / setuptools 84.0.0 / wheel 0.48.0 / build 1.6.1;
- jsonschema 4.26.0 / attrs 26.1.0 / referencing 0.37.0 / rpds-py 2026.9.1 / jsonschema-specifications 2025.9.1;
- dotnet 8.0.426;
- live CODEX route probe PASS;
- implementation Agent started false;
- Dispatch published false;
- Dispatch consumed false;
- host lifecycle mutation false.

Receipt ancestry:
`27e79ef9... → 208de84f...`, exactly one receipt-only commit.

## Assignment gates

- POLICY_CHECK: PASS
- TASK_STATE_CHECK: PASS
- SOURCE_RESOLUTION: PASS
- ROUTING_R0_R7: PASS
- ASSIGNMENT_CHECK: PASS
- MATERIAL_CAPABILITY_CHECK: PASS
- TASK-SPECIFIC_PREEXEC: PASS
- ONE_WRITER: PASS at PreExec observation; launcher must recheck immediately before start
- BUILD_ENV: PASS existing capability; no provisioning
- HOST_SAFE_STATE: PASS at PreExec observation
- NO_REPLAY: PASS
- G3/G4/Canary: HOLD / out of scope

## Host mutation scope

The executable Agent may perform only the task-defined per-user Bridge lifecycle:

`exact package build → exact install/update → paused-state verification → corrected certification → stable external uninstall once → same-package reinstall → durable-state/final-state evidence`.

No product code/test edits are authorized.

Bounded same-package recovery is allowed only under task-defined failure semantics and does not convert a failed lifecycle into PASS.

Forbidden remain:
- AppLocker/AppIDSvc;
- F1 service/ProgramData authority ACL;
- reboot;
- G3/G4;
- Canary;
- main/PR/merge;
- provider/broker/LIVE.

## Verdict

**PASS_TO_ASSIGN**

Executable runtime start must be a fresh schema-valid Dispatch whose:
- `source.commit_sha = 2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`;
- `runtime_contract.base_sha = 208de84f39dcf783bd4ee9053c0288cda9aa0024`;
- max_runs = 1;
- code writes are disabled;
- report/evidence writes are enabled;
- one-writer/host-state/package provenance checks run again immediately before consumption.

Next: publish, remote-read and validate one fresh host-lifecycle Dispatch; then Owner may launch exactly once.
