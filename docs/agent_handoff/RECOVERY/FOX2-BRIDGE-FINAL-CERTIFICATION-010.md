# FOX2 Bridge Batch B — Final Installed-Runtime Certification 010

## Role

Replacement certification controller for the EXISTING `FOX2-BRIDGE-DESKTOP-BATCH-B` whole-WP after consumed Controller 009 stopped fail-closed in Phase 0.

This is **certification-only**. Production code mutation is NOT authorized.

## Immutable lineage and current source state

Bridge task branch:
`work/FOX2-BRIDGE-DESKTOP-BATCH-B`

Current controller source head:
`3e8f47a28bc66a78442059f0b0d1d3ccd4663a06`

Certified production-code/package source head:
`501822a33ef08c7365154913bbc677544856eee5`

Installed certified package SHA-256:
`6d6b66b6fa8d1b986835e3bf4368a9f7a8749a37f687c79d2ed4d95d88f3d5a6`

The only delta from `501822a...` to `3e8f47a...` is Controller-009 stop evidence under:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/**`

No product source changed in that delta.

Dispatches 001–009 are CONSUMED and MUST NOT be replayed.

Controller 009 stop:
`CONTROLLER_PROMPT_SHA256_BINDING_MISMATCH`

009 safety facts:
- stopped in Phase 0;
- runtime_mutated=false;
- product_source_mutated=false;
- intake remained PAUSED;
- Worker remained STOPPED;
- real Worker canary 009 remained UNCLAIMED and UNEXECUTED;
- canary branch remained exactly `501822a...`;
- no canary result exists.

The Controller-009 prompt Git blob was correct and unchanged. Only the SHA-256 metadata bound by CHAT was wrong.

Correct SHA-256 for the exact 009 controller prompt blob:
`7e83a5c6ee9440c17d0d50fb729813408f241a2fba7d791bce4140bc4981c000`

Do not modify or rewrite any final009 evidence.

## Carry-forward accepted product/runtime facts

From 007/008:
- installer environment isolation PASS;
- Windows self-uninstall PASS;
- 29 focused tests PASS;
- 373 full Bridge tests PASS;
- deterministic package PASS;
- complete disposable lifecycle including uninstall/reinstall/restart/no-replay PASS;
- real owned damaged versions safely reconciled;
- durable config/data/logs/reports and ledger values preserved;
- exact certified package installed in the real per-user root;
- repeated setup PASS;
- intake PAUSED;
- SID-qualified startup task registered/enabled;
- Worker STOPPED before final certification.

008's startup assertion stop was a certification-harness case-sensitive comparison of `pwsh.EXE` vs `pwsh.exe`; read-only evidence proved the same resolved executable and all other ownership fields matched.

## Normative schema/canary semantics

### Current Dispatch v3 compatibility

Use the exact non-auto-executable v3 fixture:

`cd2a1bd0d2a4e851a79c17f538f70734277d5ad5:docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-FINAL-CERT-V3-009.json`

It exists only for installed:
- Project Dictionary binding;
- Dispatch-v3 schema binding;
- structural conformance;
- common runtime/normalizer compatibility.

Do NOT claim or execute this v3 fixture.

### Real Worker auto-execution canary

Reuse the exact still-unclaimed legacy canary identity:

`FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`

Exact artifact:

`cd2a1bd0d2a4e851a79c17f538f70734277d5ad5:docs/agent_handoff/FOX2-BRIDGE-FINAL-CANARY-009/dispatch/FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001.json`

Canary branch:
`work/FOX2-BRIDGE-FINAL-CANARY-009`

Canary base:
`501822a33ef08c7365154913bbc677544856eee5`

Canary worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-FINAL-CANARY-009`

Expected Worker route:
`CODEX / PINNED / gpt-6.1-sol / Medium / FULL_ACCESS`

Delivery owner:
`BRIDGE`

Canary Agent writable scope only:
`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/**`

Expected canary result path:
`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/agent_result.json`

Expected marker:
`FOX2_BRIDGE_FINAL_CANARY_009_AGENT_OK`

Do not create another canary identity.

## Controller writable scope

Controller 010 may write on the Bridge task branch only:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/**`

Do NOT modify:
- `agent_bridge/**`;
- any application/backend/frontend/provider/broker code;
- governance/policy/BRD/spec source;
- final009 evidence;
- core001–core008 evidence.

Temporary local helpers may exist only outside the repository in temp/runner-cache locations.

## Phase 0 — immutable binding and lineage safety

Before runtime mutation:

1. prove Bridge task branch HEAD is exactly `3e8f47a...`;
2. prove `501822a..3e8f47a` changes only `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/**`;
3. prove no product-source diff from the certified `501822a...` code state;
4. prove controller worktree clean except the controller-010 claim artifact created by the launcher;
5. independently read exact Controller 010 Dispatch and this prompt;
6. independently compute raw-byte prompt SHA-256 and compare to the Dispatch binding;
7. prove Dispatches 001–009 consumed/non-replayable;
8. prove Worker canary 009 unclaimed/unexecuted;
9. prove canary remote branch remains exactly `501822a...`;
10. prove no remote canary result exists;
11. prove exact v3 fixture and legacy canary blobs at `cd2a1bd...`;
12. prove canary prompt raw SHA-256 equals:
`dd9f45c5ac5f62bc8c65c53fe629a15d67381fe794e18956347fd1e9999ba3e0`.

Any failure: publish bounded final010 STOP evidence when safe, then STOP before runtime mutation.

## Phase 1 — startup ownership reconciliation

Read the real SID-qualified Task Scheduler entry.

Compare executable paths with Windows path equivalence:
- canonical/full path;
- case-insensitive comparison;
- same resolved executable.

Record raw strings and normalized comparison.

Required:
- exact SID;
- exact task name;
- exact arguments;
- Limited run level;
- Interactive logon;
- IgnoreNew multiple-instance policy;
- same resolved pwsh executable.

Do not rewrite the task merely for filename case.

## Phase 2 — installed v3 / v2 / v0.6 compatibility

Use the installed certified Bridge runtime, not source imports.

### v3

Read exact v3 fixture at bundle `cd2a1bd...`.

Prove through installed modules:
- Dictionary v1.2 identity/hash;
- generated v3 schema binding;
- JSON Schema v3 PASS;
- installed common dispatch validation PASS;
- installed normalization produces CODEX / BRIDGE_DIRECT_CODEX_CLI / FULL_ACCESS and exact branch/worktree/base;
- all protected authority flags remain false.

Do not execute/claim the v3 fixture.

### v2

Derive one in-memory compatibility payload from the exact v3 fixture using only the supported normalizer transformation:
- set `schema_version="2.0"`;
- remove v3-only `dictionary`;
- change identity only as required for uniqueness.

Validate/normalize with installed runtime only. Do not publish or execute.

### v0.6

Validate the exact immutable Worker canary artifact through installed common validation before claim.

Record fresh:
- PROJECT_DICTIONARY_BINDING;
- DISPATCH_V3_SCHEMA_BINDING;
- DISPATCH_V3_STRUCTURAL_CONFORMANCE;
- DISPATCH_V3_RUNTIME_COMPATIBILITY;
- V2_COMPATIBILITY;
- V06_COMPATIBILITY.

Any failure: STOP before canary claim.

## Phase 3 — real installed Tray/Worker

While intake stays PAUSED:

1. start via owned startup task/stable launcher;
2. prove exactly one Tray + one Worker healthy;
3. heartbeat advances;
4. duplicate Tray/Worker attempts rejected by singleton locks;
5. prove no canary claim while PAUSED;
6. graceful exit;
7. prove process exit + lock release;
8. restart once;
9. prove heartbeat resumes;
10. prove 001–009 remain non-replayable.

No arbitrary process kill.

## Phase 4 — exactly one real Worker canary

Only after Phases 0–3 PASS:

1. prove canary 009 is the only new eligible auto-execute identity;
2. record remote canary branch head = `501822a...`;
3. resume Bridge intake;
4. trigger normal Worker polling/check-now;
5. installed Worker discovers and claims canary exactly once;
6. do NOT invoke `e2e-once` manually;
7. do NOT invoke Codex directly for the canary;
8. wait for terminal state.

Success requires:
`PUSHED_UNREVIEWED`

Then PAUSE intake immediately.

Agent/application evidence:
- CODEX;
- PINNED;
- gpt-6.1-sol;
- Medium;
- FULL_ACCESS;
- danger-full-access / approval never actually applied;
- no substitution;
- max_runs=1.

Result evidence:
- canary remote head advances exactly once;
- changed paths only under `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/**`;
- remote `agent_result.json` exists;
- marker exact;
- Bridge result record contains pushed head;
- exact Git remote readback equals pushed head.

Usage:
- persist structured usage/capacity if exposed;
- otherwise record exactly `NOT_EXPOSED_WITH_EXECUTION_PROOF` supported by successful execution evidence;
- never fabricate numbers.

Claimed canary is consumed on any terminal failure; no replay or silent substitute.

## Phase 5 — post-canary restart / no replay

After canary success:

1. graceful exit Tray/Worker;
2. restart through owned startup path;
3. keep intake PAUSED;
4. prove canary cannot claim/execute again;
5. prove canary remote branch does not advance twice;
6. prove 001–009 remain blocked from replay;
7. export final sanitized real diagnostics/support evidence.

## Phase 6 — final010 evidence and publication

Write only under:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/**`

At minimum:
- `controller_claim.json`;
- `lineage.json`;
- `startup_task.json`;
- `installed_compatibility.json`;
- `tray_worker.json`;
- `canary_execution.json`;
- `canary_remote_readback.json`;
- `usage.json`;
- `restart_no_replay.json`;
- `final_diagnostics.json`;
- `acceptance_gates.json`;
- `final_certification.json`;
- `publication_checks.json`.

Carry forward prior PASS evidence only by exact evidence identities. Do not rerun 373 tests merely for ceremony because no product source changed.

Fresh final gates must come from real installed runtime / canary execution.

Before publication:
- task-branch changes only under final010;
- secret scan PASS;
- `git diff --check` PASS;
- commit/push exact Bridge task branch;
- exact remote readback PASS.

Technical-success marker:

`FOX2_BRIDGE_FINAL_CERTIFICATION_010_PUSHED_UNREVIEWED`

This is NOT CHAT acceptance.

Only CHAT may accept:
`INTERNAL_FOX2_BRIDGE_READY`

On any material failure: publish truthful bounded evidence and STOP.
