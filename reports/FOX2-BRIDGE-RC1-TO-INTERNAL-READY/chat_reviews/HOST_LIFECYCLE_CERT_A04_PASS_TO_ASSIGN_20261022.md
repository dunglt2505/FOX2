# FOX2 — CHAT Preflight Intake — Host Lifecycle Cert A04 PASS_TO_ASSIGN

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04`
Stage: TEST / REAL OWNER-HOST PACKAGE LIFECYCLE
Actor: CODEX
Route: `gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL`

## Verdict

**PASS_TO_ASSIGN — HOST LIFECYCLE CERTIFICATION A04 ONLY**

CHAT may publish exactly one fresh A04 CODEX Dispatch. This does not certify the lifecycle result and does not authorize G3/G4/Canary/main/PR/merge/provider/broker/LIVE.

## Why A04 exists

Historical A03 Dispatch
`FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001`
is permanently consumed/no-replay.

A03 delivered truthful report/evidence at result
`883ea51a429baf6749fa3fd412cc9ebb044f6efc`.

CHAT review:
`eced60bc22e7294bf49b367791c122ad91a97f43`.

A03 lifecycle remained NOT_RUN. The deterministic blocker was an execution/provenance contract contradiction: the accepted package builder binds `manifest.source_git_commit` to the HEAD of the worktree containing the builder, while the A03 orchestration worktree necessarily had later task/prompt/PreExec/receipt commits.

A04 corrects this without any product/source/test edit by separating the orchestration worktree from a dedicated detached accepted-source package worktree.

## Accepted product/source baseline

Accepted BUILD result:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

CHAT BUILD acceptance:
`cdf9f9c919102a2337ef357f4b658dc9993f48e5`

Accepted package builder:
- path: `agent_bridge/scripts/build_user_package.py`
- blob: `2417212e5677a2061e3957544a99e2ba80f46f4d`

No product/source/test writes are authorized by this TEST assignment.

## Immutable A04 task/prompt

Task:
- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert_a04/task.md`
- commit: `8fdc2f7181e7f3e9a7f56ea72472fe3d2d2cea43`
- blob: `50d77f3039d2a8f9ce40105457da8e18b639289d`
- SHA-256: `397e179c63666ce611e2c03cfb988ccbd9290a72b9643014fe1ff0588bfb7aa8`

Prompt:
- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert_a04/prompt.md`
- commit: `43abc5a8a988d93e3ccdd09b72f14fa4feae4d24`
- blob: `51a422a8140d3789064ff6cafb763d3a1a5241ee`
- SHA-256: `5ed59d6fe681ffdd15cc2e41cf88ac2a478717499f7d1b8e7812259be44ca5ef`

## A04 PreExec

Publication:
`3fb31e03f5317bc975119d164736e7785c46243c`

PASS receipt commit / runtime base:
`6d1d2a70f2d1cc47e44f70a0ba6cd07cd3985713`

Receipt:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/host_lifecycle_cert_a04.json`
- blob: `e074016a0780942cd1968942c51b9ecf43eac987`
- SHA-256: `c3505039d6b89fba324d4c4354f29e5b106026d2be5bee1dab50ce8d5378eb25`
- Preflight Receipt Schema v1: PASS / zero validation errors
- blockers: `[]`

CHAT remote readback verified:
- receipt commit is exactly one receipt-only commit after A04 publication;
- task branch remote head equals the receipt commit;
- accepted product source is an ancestor;
- no `agent_bridge` drift between accepted source and A04 publication;
- current Governance bytes remain unchanged;
- orchestration worktree clean;
- one-writer NONE_OBSERVED;
- host state STOPPED / paused / setup-complete / current_dispatch=null;
- WPF count=1, exact current package;
- WPF state=`HIDDEN_OR_MINIMIZED_EXACT_CURRENT`;
- Worker/legacy count=0;
- existing isolated build Python 3.13 PASS;
- dotnet 8.0.426 PASS;
- CODEX CLI 0.162.1 PASS;
- pinned `gpt-6.1-sol/high` auth/capacity PASS;
- Git push dry-run PASS;
- fresh A04 Dispatch absent;
- Agent execution not started;
- host lifecycle mutation=false.

## A04 provenance correction gate

PreExec independently verified:

Package-source worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04`

State:
- detached HEAD;
- HEAD exactly `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- clean;
- same Git repository;
- no task/report commits;
- accepted builder blob exactly `2417212e5677a2061e3957544a99e2ba80f46f4d`;
- accepted builder `source_git_commit()` read-only probe returned exactly `085cc8302e824dbccf9cbef80422ed48894b9cb4`.

This resolves the A03 provenance contradiction before assignment.

The executable Agent must reverify this package-source worktree immediately before package build. It may not rewrite the manifest, override the source identity, or patch the builder.

## Current Governance source set

Resolved bytes remain:
- Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`;
- current-source-resolution blob `186fdbc72dc1b22e97330895142d68600591ac21`;
- Dictionary v1.3 blob `6c8f30e2e6b07f2e65e45c14faab99672d036083`;
- Policy 2.0.0 blob `2d373f374f906bf7959062050bbeae5350b0c482`;
- Routing Index 1.4.0 blob `14d2e95e419cc67c3e0cf851cc806a96cf885b7e`;
- Git-first Protocol v12 blob `d34a022f2bda39a167a404c8530e57b30f337cb9`;
- Preflight Receipt Schema v1 blob `25fe465f82a16edf29ebf773a220969192f546e8`;
- CHAT Preflight Intake v1.1 blob `e7b7772183c19e58d28d8c9d3851f283a9d9c22a`;
- Dispatch Schema v3 blob `1692061941e2bef498515cd0e96b9b3046119ebb`.

Governance publication/effectivity and installed runtime adoption remain distinct. This task is bounded by the Owner-authorized Bridge Whole-WP and exact immutable A04 sources.

## R0–R7 / assignment gates

- POLICY_CHECK: PASS
- TASK_STATE_CHECK: PASS
- SOURCE_RESOLUTION: PASS
- R0 task/evidence: PASS
- R1 TEST stage: PASS
- R2 authority/source/risk: PASS
- R3 actual CODEX/Owner-host capability: PASS
- R4 actor/cost: PASS — CODEX pinned; WORK not required
- R5 worktree/writer: PASS at PreExec; must be rechecked immediately before consume
- R6 Git/result delivery: PASS
- R7 Role/Model/Thinking/Scope/STOP/result contract: PASS
- ASSIGNMENT_CHECK: PASS
- MATERIAL_CAPABILITY_CHECK: PASS
- TASK-SPECIFIC_PREEXEC: PASS
- PACKAGE_SOURCE_PROVENANCE_GATE: PASS
- NO_REPLAY: PASS
- G3/G4/Canary: HOLD / out of scope

## Runtime authorization envelope

The immutable prompt intentionally does not hard-code future PASS_TO_ASSIGN or Dispatch commit SHAs.

The Owner-visible launcher MUST inject at actual CODEX process start:

- `FOX2_DISPATCH_ID`
- `FOX2_DISPATCH_COMMIT`
- `FOX2_RUNTIME_BASE`
- `FOX2_ACCEPTED_SOURCE`
- `FOX2_PASS_TO_ASSIGN_COMMIT`
- `FOX2_PASS_TO_ASSIGN_PATH`
- `FOX2_PREEXEC_RECEIPT_COMMIT`
- `FOX2_CONTROL_BRANCH`
- `FOX2_STATUS_BRANCH`
- `FOX2_PACKAGE_SOURCE_WORKTREE`
- `FOX2_OWNER_LAUNCHER_VERIFIED=TRUE`

CODEX must independently remote-verify the supplied immutable Git refs and package-source worktree before any package build or host mutation.

Fixed identities:
- planned Dispatch ID: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001`;
- control branch: `work/FOX2-DISPATCH-chat`;
- status branch: `work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021`;
- this PASS_TO_ASSIGN path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_CERT_A04_PASS_TO_ASSIGN_20261022.md`;
- package-source worktree: `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04`;
- runtime base / PreExec receipt commit: `6d1d2a70f2d1cc47e44f70a0ba6cd07cd3985713`.

Any mismatch must STOP before package build or host mutation.

## Host TEST permission boundary

Fresh A04 Dispatch may execute only the lifecycle defined by task/prompt:
- reverify split-worktree provenance;
- optionally surface the single exact-current hidden/minimized WPF through stable `BridgeRoot/launch.ps1`, requiring same PID/path/count=1 before graceful cleanup;
- build exactly one package from the detached accepted-source package worktree;
- package output outside BridgeRoot and both Git worktrees;
- install/update exact package;
- certify WPF presentation-only lifecycle;
- graceful WPF exit;
- stable external uninstall exactly once;
- reinstall same exact package;
- verify durable/final safe state against a fresh A04 pre-mutation baseline;
- bounded same-package recovery reinstall only if task rules require it after post-mutation failure.

No force kill. No Worker/F1 fallback.

No product/source/test Git edits.

Controlling permissions:
- `permissions.code_allowed=false`;
- `permissions.git_code_push=false`;
- report/evidence write+push only.

Allowed result paths:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04/**`.

## Historical no replay

Never replay:
- `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001`.

Historical A01 FAIL, A02 consumed/no-result and A03 provenance-blocked NOT_RUN remain factual.

## Assignment decision

CHAT may publish exactly one fresh Dispatch:

`FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001`

with:
- CODEX;
- `gpt-6.1-sol`;
- reasoning `high`;
- FULL_ACCESS execution profile bounded by task;
- `MANUAL_LOCAL`;
- runtime base `6d1d2a70f2d1cc47e44f70a0ba6cd07cd3985713`;
- accepted source `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- package-source worktree exact detached accepted source;
- max_runs=1;
- report/evidence-only Git writes;
- runtime authorization envelope required;
- exact one-writer/host-state/no-drift/provenance rechecks immediately before consume.

Agent completion is at most `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

G3 remains locked.
