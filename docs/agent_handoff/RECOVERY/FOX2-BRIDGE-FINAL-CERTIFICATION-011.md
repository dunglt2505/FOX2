# FOX2 Bridge Batch B — Final Installed-Runtime Certification 011

## Role

Replacement final-certification controller for the EXISTING `FOX2-BRIDGE-DESKTOP-BATCH-B` whole-WP after consumed Controller 010 stopped fail-closed on a certification-process observer self-match.

This is **certification-only**. Production code mutation is NOT authorized.

## Immutable lineage

Bridge task branch:
`work/FOX2-BRIDGE-DESKTOP-BATCH-B`

Current controller source head:
`92bd9c82385f05893d9379c00f964760e9fe06dc`

Certified product source:
`501822a33ef08c7365154913bbc677544856eee5`

Installed certified package SHA-256:
`6d6b66b6fa8d1b986835e3bf4368a9f7a8749a37f687c79d2ed4d95d88f3d5a6`

The only branch changes after the certified product source are bounded certification evidence under:
- `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/**`
- `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/**`

No production source changed in those deltas.

Dispatches 001–010 are CONSUMED and MUST NOT be replayed.

Controller 010 stopped in Phase 0 on:
`CERTIFICATION_HARNESS_PROCESS_OBSERVER_SELF_MATCH`.

010 read-only diagnosis proved:
- observer PID 24408;
- executable `C:\Program Files\PowerShell\7\pwsh.EXE`;
- the observer query's own command line contained the Tray target literal;
- it self-matched as TRAY;
- `real_matches=[]`;
- actual Tray count = 0;
- actual Worker count = 0;
- runtime_mutated=false;
- product_source_mutated=false;
- canary 009 remained UNCLAIMED / UNEXECUTED.

## Mandatory certification process observer

Controller 011 MUST use the exact pinned observer helper:

Commit:
`928e8279ac6ca45d9421d5fa3773dd44943008ef`

Path:
`docs/agent_handoff/RECOVERY/FOX2-BRIDGE-CERT-PROCESS-OBSERVER-011.ps1`

Blob SHA-1:
`000dc032777cec198f59ddb7d6af049a9d23f1fc`

Raw UTF-8 SHA-256:
`75325a05b79cc97e20811d724bde9f0642376b2b359de68d5d6439b5f97d5792`

The helper:
- reads target Tray / Worker paths from environment variables, not its own command line;
- excludes its own PID;
- recognizes Tray only when executable is the expected pwsh binary AND command line references the exact installed `desktop_tray.ps1`;
- recognizes Worker only when executable is the exact installed Python AND argv contains `-m fox2_agent_bridge worker`;
- emits structured JSON only; it does not mutate runtime state.

Do NOT replace this with an inline `pwsh -Command` process query.
Do NOT search arbitrary process command lines using a target literal embedded in the observer command itself.

Materialize this exact helper to a temp/runner-cache path outside the repository and verify its blob/hash before use.

## Carry-forward accepted facts

From 007/008:
- installer environment isolation PASS;
- Windows self-uninstall PASS;
- 29 focused tests PASS;
- 373 full Bridge tests PASS;
- deterministic package PASS;
- complete disposable install/update/uninstall/reinstall/restart/no-replay PASS;
- real owned damaged versions safely reconciled;
- durable config/data/logs/reports and ledger values preserved;
- exact certified package installed;
- setup complete;
- intake PAUSED;
- SID-qualified startup task registered/enabled.

010 immutable bindings also PASSed. No product/runtime failure was proven.

## Existing schema fixtures and real canary

### Dispatch v3 fixture — compatibility only

Exact artifact:

`cd2a1bd0d2a4e851a79c17f538f70734277d5ad5:docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-FINAL-CERT-V3-009.json`

Do NOT claim or execute it.

Use it only for installed:
- Project Dictionary binding;
- Dispatch-v3 schema binding;
- structural conformance;
- runtime/normalizer compatibility.

### Real Worker canary — reuse unchanged identity

Dispatch:
`FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`

Exact artifact:

`cd2a1bd0d2a4e851a79c17f538f70734277d5ad5:docs/agent_handoff/FOX2-BRIDGE-FINAL-CANARY-009/dispatch/FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001.json`

Canary branch:
`work/FOX2-BRIDGE-FINAL-CANARY-009`

Canary base:
`501822a33ef08c7365154913bbc677544856eee5`

Canary worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-FINAL-CANARY-009`

Route:
`CODEX / PINNED / gpt-6.1-sol / Medium / FULL_ACCESS`

Delivery owner:
`BRIDGE`

Canary Agent writable scope only:
`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/**`

Expected result:
`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/agent_result.json`

Expected marker:
`FOX2_BRIDGE_FINAL_CANARY_009_AGENT_OK`

Do NOT create another canary identity.

## Controller writable scope

Controller 011 may write only:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final011/**`

Do NOT modify:
- `agent_bridge/**`;
- frontend/backend/provider/broker code;
- governance/policy/spec source;
- `final009/**`;
- `final010/**`;
- `core001/**` through `core008/**`.

Temporary observer/controller helpers may exist outside the repository only.

## Phase 0 — immutable binding, lineage and observer safety

Before any runtime mutation:

1. prove task branch HEAD exactly `92bd9c...`;
2. prove `501822a..92bd9c` changes only final009/final010 report evidence;
3. prove no production-source diff from the certified `501822a...`;
4. independently validate Controller 011 Dispatch and prompt raw bytes/hash;
5. independently validate pinned observer helper blob and SHA-256;
6. independently validate canary prompt hash and exact canary/v3 fixture blobs;
7. prove Dispatches 001–010 consumed/non-replayable;
8. prove canary 009 remains unclaimed/unexecuted;
9. prove canary branch still equals `501822a...`;
10. prove no remote canary result exists;
11. derive the installed version from real `current.json`;
12. derive exact installed Tray script, installed Worker Python and pwsh executable;
13. run the pinned observer helper while runtime is expected STOPPED/PAUSED;
14. require `tray_count=0`, `worker_count=0`, and no match PID equals the observer PID.

Record this as `observer_validation.json`.

If the observer validation fails, STOP before any runtime mutation and publish bounded final011 evidence when safe.

## Phase 1 — startup ownership

Read the real SID-qualified Task Scheduler entry.

Compare executable using Windows path-equivalence semantics:
- canonical/full path;
- case-insensitive;
- same resolved executable.

Record raw and normalized values.

Require:
- exact SID;
- exact task name;
- exact arguments;
- Limited run level;
- Interactive logon;
- IgnoreNew multiple-instance policy;
- same resolved pwsh executable.

Do not rewrite the task merely for filename case.

## Phase 2 — installed v3 / v2 / v0.6 compatibility

Use installed certified Bridge modules only.

### v3

Read exact v3 fixture from bundle `cd2a1bd...`.

Prove:
- Dictionary v1.2 identity/hash;
- generated v3 schema binding;
- JSON Schema v3 PASS;
- common installed validation PASS;
- normalization yields CODEX / BRIDGE_DIRECT_CODEX_CLI / FULL_ACCESS and exact canary branch/worktree/base;
- protected authority flags remain false.

Do not execute or claim the v3 fixture.

### v2

Derive one in-memory compatibility payload from the exact v3 fixture:
- `schema_version="2.0"`;
- remove v3-only `dictionary`;
- change only identity if necessary for uniqueness.

Validate/normalize with installed runtime only. Do not publish or execute.

### v0.6

Validate the exact immutable Worker canary through installed common validation before claim.

Freshly record:
- PROJECT_DICTIONARY_BINDING;
- DISPATCH_V3_SCHEMA_BINDING;
- DISPATCH_V3_STRUCTURAL_CONFORMANCE;
- DISPATCH_V3_RUNTIME_COMPATIBILITY;
- V2_COMPATIBILITY;
- V06_COMPATIBILITY.

Any compatibility failure: STOP before canary claim.

## Phase 3 — real Tray/Worker certification

While intake remains PAUSED:

1. observe zero Tray/Worker with the pinned helper;
2. start through the owned startup task/stable launcher;
3. use the pinned helper to prove exactly one Tray and one Worker;
4. prove heartbeat advances;
5. attempt duplicate Tray/Worker launches through supported paths and prove singleton rejection without creating a second real match;
6. prove canary remains unclaimed while PAUSED;
7. request graceful exit through Bridge control;
8. use pinned helper until both counts return to zero;
9. prove locks release;
10. restart once through owned startup path;
11. prove exactly one Tray and Worker again and heartbeat resumes;
12. prove 001–010 remain non-replayable.

No arbitrary process kill.

## Phase 4 — execute exactly one real Worker canary

Only after Phases 0–3 PASS:

1. prove canary 009 is the only new eligible auto-execute identity;
2. record canary remote head = `501822a...`;
3. resume intake;
4. trigger normal Worker polling/check-now;
5. installed Worker discovers and claims canary exactly once;
6. do NOT invoke `e2e-once` manually;
7. do NOT invoke Codex directly for the canary;
8. wait for terminal state.

Success requires:
`PUSHED_UNREVIEWED`.

Immediately PAUSE intake after terminal success.

Required Agent evidence:
- CODEX;
- PINNED;
- gpt-6.1-sol;
- Medium;
- FULL_ACCESS;
- danger-full-access / approval never applied;
- no substitution;
- max_runs=1.

Required result evidence:
- canary remote branch advances exactly once;
- changed paths only under final009/canary scope;
- remote `agent_result.json` exists;
- marker exact;
- Bridge runtime result records pushed head;
- exact remote readback equals pushed head.

Usage:
- persist structured values if exposed;
- otherwise record exactly `NOT_EXPOSED_WITH_EXECUTION_PROOF`;
- never fabricate numeric quota/usage.

A claimed canary is consumed on failure; no replay or silent substitution.

## Phase 5 — post-canary restart/no-replay

After canary success:

1. graceful exit;
2. pinned observer proves Tray/Worker zero;
3. restart via owned startup path;
4. pinned observer proves exactly one Tray/Worker;
5. keep intake PAUSED;
6. prove canary cannot claim/execute again;
7. prove canary branch does not advance twice;
8. prove 001–010 remain blocked from replay;
9. export final sanitized diagnostics/support evidence.

## Phase 6 — final011 evidence and publication

Write only under:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final011/**`

At minimum:
- `controller_claim.json`;
- `lineage.json`;
- `observer_validation.json`;
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

Carry forward previous PASS evidence only by exact evidence identity. Do not rerun 373 tests merely for ceremony because product source is unchanged.

Before publication:
- task-branch changes only under final011;
- secret scan PASS;
- `git diff --check` PASS;
- commit/push exact task branch;
- exact remote readback PASS.

Technical-success marker:

`FOX2_BRIDGE_FINAL_CERTIFICATION_011_PUSHED_UNREVIEWED`

This is NOT CHAT acceptance.

Only CHAT may accept:
`INTERNAL_FOX2_BRIDGE_READY`.

On any material failure, publish truthful bounded final011 evidence and STOP.
