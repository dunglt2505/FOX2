# FOX2 Bridge Batch B — Final Installed-Runtime Certification 012

## Role

Replacement final-certification controller for the EXISTING `FOX2-BRIDGE-DESKTOP-BATCH-B` whole-WP after consumed Controller 011 stopped fail-closed on certification-helper raw-byte materialization.

This is **certification-only**. Production code mutation is NOT authorized.

## Immutable lineage

Bridge task branch:
`work/FOX2-BRIDGE-DESKTOP-BATCH-B`

Current controller source head:
`4a00621b6a736d612cdf99506da01d0e4b3c6417`

Certified product source:
`501822a33ef08c7365154913bbc677544856eee5`

Installed certified package SHA-256:
`6d6b66b6fa8d1b986835e3bf4368a9f7a8749a37f687c79d2ed4d95d88f3d5a6`

The only branch changes after the certified product source are bounded certification evidence under:
- `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/**`
- `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/**`
- `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final011/**`

No production source changed in those deltas.

Dispatches 001–011 are CONSUMED and MUST NOT be replayed.

## Controller 011 stop — accepted root cause

Controller 011 stopped in Phase 0 on:

`OBSERVER_HELPER_RAW_SHA256_MISMATCH`

Immutable Git observer helper was correct:

- commit `928e8279ac6ca45d9421d5fa3773dd44943008ef`
- path `docs/agent_handoff/RECOVERY/FOX2-BRIDGE-CERT-PROCESS-OBSERVER-011.ps1`
- blob SHA-1 `000dc032777cec198f59ddb7d6af049a9d23f1fc`
- raw bytes `2768`
- raw SHA-256 `75325a05b79cc97e20811d724bde9f0642376b2b359de68d5d6439b5f97d5792`
- CRLF count in Git blob `0`

The Controller-011 materialized helper was incorrect only because a PowerShell text pipeline converted LF to CRLF:

- materialized bytes `2859`
- CRLF count `91`
- SHA-256 `55905659a6ba5a11af52b5a7cc6afd04575d3dbf7cc0502725479782dca731be`
- equality after CRLF normalization `true`

Classification:

`CERTIFICATION_HARNESS_MATERIALIZATION_FAILURE`

Not proven:

`PRODUCT_RUNTIME_FAILURE`

011 safety facts:
- runtime_mutated=false;
- product_source_mutated=false;
- canary 009 UNCLAIMED / UNEXECUTED;
- canary branch unchanged at `501822a...`;
- no canary result exists.

## Mandatory binary-safe observer materialization

Controller 012 MUST use the SAME immutable observer helper listed above.

The launcher materializes it outside the repository using exact raw Git blob bytes:

`git cat-file blob <commit:path>`

captured by Python `subprocess.check_output` and written by `Path.write_bytes`.

The launcher MUST verify after materialization:
- byte length = `2768`;
- SHA-256 = `75325a05b79cc97e20811d724bde9f0642376b2b359de68d5d6439b5f97d5792`;
- CRLF count = `0`.

The launcher then runs the observer smoke test before claim and requires:
- `tray_count=0`;
- `worker_count=0`;
- no match PID equals observer PID.

The controller MUST reuse the exact launcher-materialized observer path.

The controller MUST NOT:
- materialize the observer again;
- pipe observer source through `Out-String`, `Get-Content`, `Set-Content` or `WriteAllText`;
- normalize newline bytes;
- reconstruct an inline observer;
- replace the pinned helper.

Before Phase 1, controller must independently verify the already-materialized file via binary read and SHA-256. If it does not match the exact Git helper, STOP.

## Carry-forward accepted product/runtime facts

From 007/008:
- installer environment isolation PASS;
- Windows self-uninstall PASS;
- 29 focused tests PASS;
- 373 full Bridge tests PASS;
- deterministic package PASS;
- complete disposable install/update/uninstall/reinstall/restart/no-replay PASS;
- real owned damaged versions safely reconciled;
- durable config/data/logs/reports and ledger preserved;
- exact certified package installed;
- setup complete;
- intake PAUSED;
- SID-qualified startup task registered/enabled.

009/010/011 made no product/runtime mutation.

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

Controller 012 may write only:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final012/**`

Do NOT modify:
- `agent_bridge/**`;
- frontend/backend/provider/broker code;
- governance/policy/spec source;
- `final009/**`;
- `final010/**`;
- `final011/**`;
- `core001/**` through `core008/**`.

Temporary observer/controller helpers may exist outside the repository only.

## Phase 0 — immutable binding, lineage and raw-byte observer safety

Before any runtime mutation:

1. prove task branch HEAD exactly `4a00621...`;
2. prove `501822a..4a00621` changes only final009/final010/final011 report evidence;
3. prove no production-source diff from certified `501822a...`;
4. independently validate Controller 012 Dispatch and prompt raw bytes/hash;
5. independently validate pinned observer Git blob and raw SHA-256;
6. independently binary-read the launcher-materialized observer file;
7. require materialized file:
   - bytes = 2768;
   - SHA-256 exact;
   - CRLF count = 0;
8. independently validate canary prompt hash and exact canary/v3 fixture blobs;
9. prove Dispatches 001–011 consumed/non-replayable;
10. prove canary 009 remains unclaimed/unexecuted;
11. prove canary branch still equals `501822a...`;
12. prove no remote canary result exists;
13. derive installed version from real `current.json`;
14. derive exact installed Tray script, Worker Python and pwsh executable;
15. execute ONLY the already-materialized pinned observer helper;
16. require `tray_count=0`, `worker_count=0`, and no self-match.

Record this as `observer_validation.json`.

Any failure: STOP before runtime mutation and publish bounded final012 evidence when safe.

## Phase 1 — startup ownership

Read the real SID-qualified Task Scheduler entry.

Compare executable using Windows path-equivalence semantics:
- canonical/full path;
- case-insensitive;
- same resolved executable.

Require:
- exact SID;
- exact task name;
- exact arguments;
- Limited run level;
- Interactive logon;
- IgnoreNew multiple-instance policy;
- same resolved pwsh executable.

Do not rewrite task merely for case normalization.

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
- protected authorities false.

Do not execute or claim v3 fixture.

### v2

Derive one in-memory compatibility payload from exact v3 fixture:
- `schema_version="2.0"`;
- remove v3-only `dictionary`;
- change only identity if necessary.

Validate/normalize through installed runtime only. Do not publish or execute.

### v0.6

Validate exact immutable Worker canary through installed common validation before claim.

Freshly record:
- PROJECT_DICTIONARY_BINDING;
- DISPATCH_V3_SCHEMA_BINDING;
- DISPATCH_V3_STRUCTURAL_CONFORMANCE;
- DISPATCH_V3_RUNTIME_COMPATIBILITY;
- V2_COMPATIBILITY;
- V06_COMPATIBILITY.

Any failure: STOP before canary claim.

## Phase 3 — real Tray/Worker certification

While intake PAUSED:

1. observer proves zero Tray/Worker;
2. start through owned startup task/stable launcher;
3. observer proves exactly one Tray + one Worker;
4. heartbeat advances;
5. duplicate launch attempts rejected by singleton locks;
6. canary remains unclaimed while PAUSED;
7. request graceful exit;
8. observer proves zero;
9. locks release;
10. restart through owned path;
11. observer proves exactly one each and heartbeat resumes;
12. prove 001–011 non-replayable.

No arbitrary process kill.

## Phase 4 — exactly one real Worker canary

Only after Phases 0–3 PASS:

1. prove canary 009 is the only new eligible auto-execute identity;
2. record remote canary branch head = `501822a...`;
3. resume intake;
4. trigger normal Worker polling/check-now;
5. installed Worker discovers/claims canary exactly once;
6. do NOT invoke `e2e-once` manually;
7. do NOT invoke Codex directly for canary;
8. wait for terminal state.

Success requires:
`PUSHED_UNREVIEWED`.

Immediately PAUSE intake after success.

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
- canary branch advances exactly once;
- changed paths only final009/canary scope;
- remote `agent_result.json` exists;
- exact marker;
- Bridge result record contains pushed head;
- exact remote readback equals pushed head.

Usage:
- persist structured usage/capacity if exposed;
- otherwise `NOT_EXPOSED_WITH_EXECUTION_PROOF`;
- never fabricate numeric usage.

Claimed canary is consumed on failure; no replay or silent substitute.

## Phase 5 — post-canary restart/no-replay

After canary success:

1. graceful exit;
2. observer proves zero;
3. restart through owned path;
4. observer proves exactly one Tray/Worker;
5. keep intake PAUSED;
6. prove canary cannot claim/execute again;
7. prove canary branch does not advance twice;
8. prove 001–011 remain blocked;
9. export final sanitized diagnostics.

## Phase 6 — final012 evidence and publication

Write only under:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final012/**`

At minimum:
- `controller_claim.json`;
- `lineage.json`;
- `observer_materialization.json`;
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

Carry forward prior PASS evidence only by exact evidence identity. Do not rerun 373 tests merely for ceremony because product source is unchanged.

Before publication:
- task-branch changes only final012;
- secret scan PASS;
- `git diff --check` PASS;
- commit/push exact task branch;
- exact remote readback PASS.

Technical-success marker:

`FOX2_BRIDGE_FINAL_CERTIFICATION_012_PUSHED_UNREVIEWED`

This is NOT CHAT acceptance.

Only CHAT may accept:
`INTERNAL_FOX2_BRIDGE_READY`.

On any material failure, publish truthful bounded final012 evidence and STOP.
