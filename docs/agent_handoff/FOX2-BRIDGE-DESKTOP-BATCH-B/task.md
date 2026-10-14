# FOX2-BRIDGE-DESKTOP-BATCH-B — Whole-WP Task

**Status:** SOURCE_READY / PREEXEC_HOLD  
**Project phase:** Bridge second execution phase  
**Governance:** Project Dictionary v1 -> Policy V1.8.7 -> Routing Index V1.2.8  
**Protocol:** Dispatch Schema v3 + Git-first Protocol v10  
**Final Agent assignment:** PENDING R3/R5 MATERIAL PREFLIGHT  
**Execution path:** MANUAL_LOCAL candidate for implementation; installed Bridge path is the certification target  
**Delivery owner:** AGENT candidate

## Source binding

- Owner-accepted Batch-A code head: `3013f34d7ad91d1462e44495c873a84c41297b6b`
- Parent validated Batch-A result: `b2de4a10f259c4baf40a83372783e11fc7edd64a` with 243 PASS / 0 fail / 0 skip.
- Owner waiver record: Issue #10 comment `6165391726`.
- Current Master Plan: `f109d16f78da4a412cc30b512f152f79616b872c:docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md`
- Project Dictionary/source set: `544cd7003972e6a29ff25de1062231c3769affbf`
- Bridge Technical Spec v0.7 Candidate REV8;
- Usage/CHAT Routing Contract Candidate REV5.

Batch A's separate post-patch Windows rerun was waived by Owner. Do not falsify it as PASS and do not reopen Batch A. Batch B final certification carries the current-schema validation debt once, as part of the final installed-runtime certification.

## Whole-WP objective

Turn the accepted Bridge codebase into an **internally usable installed per-user FOX2 Bridge** and certify one real eligible FOX2 dispatch/result flow.

Implement/test together:

1. first-run setup and configuration;
2. per-user installed runtime;
3. deterministic installer/package;
4. update/upgrade path;
5. uninstall/cleanup path preserving/sanitizing intended data according to spec;
6. startup/login integration and single-instance behavior;
7. sanitized diagnostics/support bundle;
8. installed Tray/Worker integration;
9. exact Project Dictionary / Dispatch-v3 current binding in installed runtime;
10. one real eligible FOX2 WP/certification canary through installed Bridge;
11. exact selected Agent/model/tier/reasoning/permission application;
12. Agent/Bridge delivery-owner behavior and CHAT-readable remote result;
13. usage/configuration snapshot persisted for next routing;
14. restart after completed certification proves no replay;
15. one final full Bridge certification cycle over the current code head.

## Carry-forward certification debt

The final Batch-B certification MUST include current-code execution of:

- `DISPATCH_V3_SCHEMA_BINDING`
- `DISPATCH_V3_STRUCTURAL_CONFORMANCE`
- `PROJECT_DICTIONARY_BINDING`
- `DISPATCH_V3_RUNTIME_COMPATIBILITY`
- `V2_COMPATIBILITY`
- `V06_COMPATIBILITY`

This satisfies the current release-readiness obligation once inside Batch B. It is not a separate Batch-A rerun.

## Writable scope

Allowed:
- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-BATCH-B/**`

Everything else READ-ONLY.

The certification canary may use a task/result fixture or bounded real FOX2 certification artifact entirely inside the authorized Batch-B test/report scope. It must not mutate application/backend/frontend/provider/broker code.

## Required acceptance

At minimum:

- `FIRST_RUN_SETUP=PASS`
- `PER_USER_INSTALL=PASS`
- `INSTALLER_PACKAGE=PASS`
- `UPDATE_PATH=PASS`
- `UNINSTALL_PATH=PASS`
- `STARTUP_SINGLE_INSTANCE=PASS`
- `SANITIZED_DIAGNOSTICS_BUNDLE=PASS`
- `INSTALLED_TRAY_WORKER=PASS`
- `PROJECT_DICTIONARY_BINDING=PASS`
- `DISPATCH_V3_SCHEMA_BINDING=PASS`
- `DISPATCH_V3_STRUCTURAL_CONFORMANCE=PASS`
- `DISPATCH_V3_RUNTIME_COMPATIBILITY=PASS`
- `V2_COMPATIBILITY=PASS`
- `V06_COMPATIBILITY=PASS`
- `REAL_ELIGIBLE_FOX2_DISPATCH=PASS`
- `EXACT_AGENT_CONFIGURATION=PASS`
- `FULL_ACCESS_PERMISSION=PASS`
- `RESULT_REMOTE_READBACK=PASS`
- `USAGE_SNAPSHOT=PASS_OR_NOT_EXPOSED_WITH_EXECUTION_PROOF`
- `RESTART_NO_REPLAY=PASS`
- `FULL_BRIDGE_TESTS=PASS`
- `CHANGED_PATH_ALLOWLIST=PASS`
- `SECRET_SCAN=PASS`
- `GIT_DIFF_CHECK=PASS`

Exit target:
`INTERNAL_FOX2_BRIDGE_READY`.

## Material pre-execution gates

Before executable Dispatch v3:

1. exact branch/worktree ownership = PASS;
2. selected Agent CLI + FULL_ACCESS compatibility = PASS;
3. current Agent execution capacity/auth must be demonstrably usable or validly classified by Policy;
4. required Windows packaging/install capabilities = PASS;
5. no competing writer on `agent_bridge/**`.

Until those are evidenced:
`CODE_ALLOWED_FOR_EXECUTION=HOLD`.

## Routing candidates — not final assignment

- CODEX CLI / PINNED / gpt-6.1-sol / Medium by default; High only if installer/restart/recovery/concurrency debugging becomes material.
- COPILOT CLI / NATIVE_AUTO / Balance is a valid comparison candidate for clear packaging/scripts if current capacity is demonstrated and no safety/concurrency complexity favors Codex.
- CHAT owns source binding/routing/acceptance.
- WORK may enter only at final installed-runtime/release-readiness audit if materially useful.

No Agent is assigned while R3/R5 remain unresolved.

## Git authority after executable dispatch

Candidate delivery owner = AGENT, exact non-main task branch only.

No PR/main/merge/deploy/provider/broker/LIVE authority.

## STOP

Stop for:
- source/base/branch/worktree mismatch;
- packaging/install capability missing;
- actual Agent capacity/auth failure;
- overlapping `agent_bridge/**` writer;
- required test/security failure;
- secret/private exposure;
- out-of-scope write;
- push/readback failure.

## Delivery

Expected after execution:
- `reports/BRIDGE-DESKTOP-BATCH-B/report.md`
- `reports/BRIDGE-DESKTOP-BATCH-B/evidence_manifest.json`
- material evidence under `reports/BRIDGE-DESKTOP-BATCH-B/evidence/**`

Final marker:
`FOX2_BRIDGE_DESKTOP_BATCH_B_PUSHED_UNREVIEWED`
