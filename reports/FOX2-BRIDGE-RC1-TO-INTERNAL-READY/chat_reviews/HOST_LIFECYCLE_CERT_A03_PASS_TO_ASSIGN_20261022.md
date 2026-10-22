# FOX2 — CHAT Preflight Intake — Host Lifecycle Cert A03 PASS_TO_ASSIGN

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03`
Stage: TEST / REAL OWNER-HOST PACKAGE LIFECYCLE
Actor: CODEX
Route: `gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL`

## Verdict

**PASS_TO_ASSIGN — HOST LIFECYCLE CERTIFICATION A03 ONLY**

This authorizes publication of exactly one fresh schema-v3 CODEX Dispatch for A03. It does not certify the lifecycle result and does not authorize G3/G4/Canary/main/PR/merge/provider/broker/LIVE.

## Why A03 exists

Historical A02 Dispatch `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001` is permanently consumed/no-replay.

A02 certification remained `NOT_RUN`: CODEX started but blocked before package build or host mutation because the immutable prompt required later-created PASS_TO_ASSIGN/Dispatch/Owner-launch evidence that was not visible in the Agent execution context.

Recovery review: `53c3913899f87ad867c04c14d1da52b27d3cdbec`.

A03 corrects only that execution-envelope visibility defect. Product/source/test semantics remain the accepted BUILD result below.

## Accepted product/source baseline

Accepted A02 BUILD result:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

CHAT BUILD acceptance:
`cdf9f9c919102a2337ef357f4b658dc9993f48e5`

No product/source/test edits are authorized by this TEST assignment.

## Immutable A03 task/prompt

Task:
- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert_a03/task.md`
- commit: `33f6176dff86b00df6c9b8b0ef6f8eefce00578e`
- blob: `687dfc109ed438db5a5b69b75486f1a32994eb9d`
- SHA-256: `f9e2fe4e285f703edabd8ec1266b0244d520ee2e1be876daf45b332bfcfc1f0f`

Prompt:
- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert_a03/prompt.md`
- commit: `db9902a1adbe21f801707ed9680fe38524e92dfc`
- blob: `ccffde862e11490743e5aabb5c79a4a0986ab9a1`
- SHA-256: `170f48485aa44deee24c4e3af1529273343dd5cef3d94489e7e24b11bf1c38ee`

## PreExec A03

Publication:
`7abaf0657b6e0c1f848daddf6432477d5962b9b1`

PASS receipt commit / runtime base:
`534204d5cc39a17fb4b3beb948b9b472d6e550b5`

Receipt:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/host_lifecycle_cert_a03.json`
- blob: `847dd0f6c2ee5b5ebecc96a1808640aa0d9e0228`
- SHA-256: `0fd19aeee99092a82cd2beac4fbca7fd7fb0cc274d9063a3c94ce850d85ea9a8`
- Preflight Receipt Schema v1: PASS / zero validation errors
- blockers: `[]`

CHAT remote readback verified:
- receipt commit is exactly one receipt-only commit after A03 publication;
- task branch remote head equals receipt commit;
- source/task/prompt binding PASS;
- current Governance bytes PASS;
- dedicated worktree clean;
- one-writer NONE_OBSERVED;
- host state STOPPED / paused / setup_complete / current_dispatch=null;
- WPF count=1;
- WPF exact current package=true;
- WPF state=`HIDDEN_OR_MINIMIZED_EXACT_CURRENT`;
- UI inspect=`WINDOW_UNAVAILABLE`;
- Worker/legacy count=0;
- existing isolated build Python 3.13 PASS;
- dotnet 8.0.426 PASS;
- CODEX CLI 0.162.1 PASS;
- pinned `gpt-6.1-sol/high` auth/capacity PASS;
- Git push dry-run PASS;
- fresh A03 Dispatch absent;
- Agent execution not started;
- host lifecycle mutation=false;
- G3=false.

## Current Governance source set

Resolved Governance bytes remain:
- Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`;
- source-resolution blob `186fdbc72dc1b22e97330895142d68600591ac21`;
- Dictionary v1.3 blob `6c8f30e2e6b07f2e65e45c14faab99672d036083`;
- Policy 2.0.0 blob `2d373f374f906bf7959062050bbeae5350b0c482`;
- Routing Index 1.4.0 blob `14d2e95e419cc67c3e0cf851cc806a96cf885b7e`;
- Git-first Protocol v12 blob `d34a022f2bda39a167a404c8530e57b30f337cb9`;
- Preflight Receipt Schema v1 blob `25fe465f82a16edf29ebf773a220969192f546e8`;
- CHAT Preflight Intake v1.1 blob `e7b7772183c19e58d28d8c9d3851f283a9d9c22a`;
- Dispatch Schema v3 blob `1692061941e2bef498515cd0e96b9b3046119ebb`.

Governance document authority and installed runtime adoption remain separate. This assignment is bounded by the Owner-authorized Whole-WP, immutable A03 task/prompt, actual PreExec PASS and fresh Dispatch permissions.

## R0–R7 / assignment gates

- POLICY_CHECK: PASS
- TASK_STATE_CHECK: PASS
- SOURCE_RESOLUTION: PASS
- R0 task/evidence: PASS
- R1 TEST stage: PASS
- R2 authority/source/risk: PASS
- R3 actual route/capability: PASS
- R4 actor/cost: PASS — CODEX pinned; WORK not required
- R5 worktree/writer: PASS at PreExec; must be rechecked immediately before consume
- R6 Git/result delivery: PASS
- R7 role/model/thinking/scope/STOP/result contract: PASS
- ASSIGNMENT_CHECK: PASS
- MATERIAL_CAPABILITY_CHECK: PASS
- TASK-SPECIFIC_PREEXEC: PASS
- NO_REPLAY: PASS
- G3/G4/Canary: HOLD / out of scope

## A03 runtime authorization envelope

The immutable prompt intentionally does not hard-code future PASS_TO_ASSIGN or Dispatch commit SHAs.

The Owner-visible launcher MUST inject at actual CODEX process start:
- `FOX2_DISPATCH_ID`;
- `FOX2_DISPATCH_COMMIT`;
- `FOX2_RUNTIME_BASE`;
- `FOX2_ACCEPTED_SOURCE`;
- `FOX2_PASS_TO_ASSIGN_COMMIT`;
- `FOX2_PASS_TO_ASSIGN_PATH`;
- `FOX2_PREEXEC_RECEIPT_COMMIT`;
- `FOX2_CONTROL_BRANCH`;
- `FOX2_STATUS_BRANCH`;
- `FOX2_OWNER_LAUNCHER_VERIFIED=TRUE`.

CODEX must independently fetch/read the supplied immutable Git refs and verify them before any package build or host mutation.

Expected fixed artifact identities:
- planned Dispatch ID: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001`;
- control branch: `work/FOX2-DISPATCH-chat`;
- status branch: `work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021`;
- this PASS_TO_ASSIGN path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_CERT_A03_PASS_TO_ASSIGN_20261022.md`;
- runtime base / PreExec receipt commit: `534204d5cc39a17fb4b3beb948b9b472d6e550b5`.

The envelope transports evidence only; Git remains authoritative. Any mismatch must STOP before host mutation.

## Host TEST permission boundary

Fresh A03 Dispatch may execute only the lifecycle in task/prompt:
- optionally surface the one exact-current hidden/minimized WPF singleton once via stable `BridgeRoot/launch.ps1`, requiring same PID/path/count=1 before graceful cleanup;
- build one exact accepted package outside BridgeRoot;
- install/update exact package;
- certify WPF presentation-only lifecycle;
- graceful WPF exit;
- stable external uninstall exactly once;
- reinstall the same exact package;
- durable/final safe-state verification;
- bounded same-package recovery reinstall only if task conditions permit after post-mutation failure.

No force kill. No Worker/F1 fallback.

No product/source/test Git edits.

Controlling permissions:
- `permissions.code_allowed=false`;
- `permissions.git_code_push=false`;
- report/evidence write+push only.

Allowed result paths:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a03/**`.

## No replay

Never replay:
- `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001`.

Historical failures/consumed attempts remain factual.

## Assignment decision

CHAT may publish exactly one fresh Dispatch:

`FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001`

with:
- CODEX;
- `gpt-6.1-sol`;
- reasoning `high`;
- FULL_ACCESS execution profile bounded by task;
- `MANUAL_LOCAL`;
- runtime base `534204d5cc39a17fb4b3beb948b9b472d6e550b5`;
- accepted source `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- max_runs=1;
- report/evidence-only Git writes;
- runtime authorization envelope required;
- exact one-writer/host-state/no-drift checks immediately before consume.

Agent completion is at most `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

G3 remains locked.
