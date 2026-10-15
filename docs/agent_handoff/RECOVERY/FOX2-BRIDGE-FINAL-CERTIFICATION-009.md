# FOX2 Bridge Batch B — Final Installed-Runtime Certification 009

## Role

Certification controller for the EXISTING `FOX2-BRIDGE-DESKTOP-BATCH-B` whole-WP.

This is **certification-only**. Production code mutation is not authorized by this dispatch.

## Immutable source/runtime state

Bridge task branch:
`work/FOX2-BRIDGE-DESKTOP-BATCH-B`

Bound source head:
`501822a33ef08c7365154913bbc677544856eee5`

Installed certified package SHA-256:
`6d6b66b6fa8d1b986835e3bf4368a9f7a8749a37f687c79d2ed4d95d88f3d5a6`

Dispatches 001–008 are CONSUMED and MUST NOT be replayed.

008 accepted facts:
- 29 focused tests PASS;
- 373 full Bridge tests PASS;
- installer environment isolation PASS;
- Windows external self-uninstall PASS;
- complete disposable lifecycle including uninstall/reinstall/restart/no-replay PASS;
- real owned damaged versions safely reconciled;
- durable config/data/logs/reports and original ledger values preserved;
- exact certified package installed in the real per-user root;
- repeated setup PASS and intake is PAUSED;
- exact SID-qualified startup task registered/enabled;
- worker final state before 009 is STOPPED / PAUSED.

008 stopped only because its certification harness compared `pwsh.EXE` vs `pwsh.exe` case-sensitively. Read-only evidence proved both resolve to the same Windows executable and all other startup ownership fields match.

## Normative schema/canary semantics locked by CHAT

Do NOT merge the following two roles:

### Current Dispatch v3 compatibility

Dispatch v3 is the current Project-Dictionary-bound external schema and MUST be validated by the installed runtime through its current schema + normalizer + common runtime validation path.

Pinned non-auto-executable v3 fixture:

`cd2a1bd0d2a4e851a79c17f538f70734277d5ad5:docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-FINAL-CERT-V3-009.json`

It has `execution_path=BRIDGE` and intentionally has no `runtime_contract.auto_execute`, because Dispatch Schema v3 does not permit that field.

Do NOT execute/claim this v3 fixture. It exists only for installed-runtime schema/structural/normalization compatibility proof.

### Real Worker auto-execution canary

The current Worker auto-discovery contract explicitly requires:
- `runtime_contract.auto_execute=true`;
- top-level legacy `agent.product`.

Therefore the real installed Worker canary is the supported legacy v0.6 artifact:

`cd2a1bd0d2a4e851a79c17f538f70734277d5ad5:docs/agent_handoff/FOX2-BRIDGE-FINAL-CANARY-009/dispatch/FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001.json`

Canary branch:
`work/FOX2-BRIDGE-FINAL-CANARY-009`

Canary base:
`501822a33ef08c7365154913bbc677544856eee5`

Canary worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-FINAL-CANARY-009`

The canary is the ONLY new auto-executable identity authorized in 009.

Expected canary route:
`CODEX / PINNED / gpt-6.1-sol / Medium / FULL_ACCESS`

Delivery owner:
`BRIDGE`

The selected Agent may change only:
`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/**`

The Bridge, not the Agent, must commit/push the bounded result.

## Writable scope for the certification controller

On the Bridge task branch, this controller may write only:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/**`

Do NOT modify:
- `agent_bridge/**`;
- application/backend/frontend/provider/broker code;
- governance/policy/BRD/spec source;
- any prior `core001`–`core008` evidence.

Temporary local helper scripts may be created under `%TEMP%` or `%LOCALAPPDATA%\FOX2\runner-cache`; they are not repository artifacts.

## Phase 0 — launch/source/replay safety

Before any real runtime mutation:

1. prove exact task branch/source head `501822a...`;
2. prove controller worktree is clean and there is no competing material writer;
3. read the exact controller Dispatch and this prompt;
4. prove Dispatches 001–008 remain consumed/non-replayable;
5. prove final legacy canary identity has NOT already been claimed;
6. prove remote canary branch head still equals `501822a...`;
7. prove exact canary and v3 fixture blobs are readable at control bundle commit `cd2a1bd...`.

If any condition fails: STOP before new claim/runtime mutation.

## Phase 1 — startup ownership reconciliation, no rewrite

Read the real SID-qualified Task Scheduler entry.

Compare executable paths using Windows path-equivalence semantics:
- canonical/full path;
- case-insensitive comparison;
- same resolved executable.

Record BOTH raw forms.

Required fields:
- exact SID;
- exact task name;
- exact launcher arguments;
- run level Limited;
- logon type Interactive;
- multiple-instances IgnoreNew;
- executable resolves to the same pwsh binary.

Do NOT rewrite/re-register the task merely to normalize filename case.

## Phase 2 — installed v3 / v2 / v0.6 compatibility

Use the **installed certified Bridge runtime**, not source imports from the worktree.

### v3

Read the exact v3 fixture from control commit `cd2a1bd...`.

Through installed modules, prove:
- Project Dictionary v1.2 identity/hash binding;
- Dispatch Schema v3 generated binding;
- JSON Schema v3 PASS;
- `BridgeE2ERunner._validate_dispatch` / equivalent installed common validation PASS;
- normalization yields `CODEX`, `BRIDGE_DIRECT_CODEX_CLI`, `FULL_ACCESS`, exact canary branch/worktree/base;
- protected authorities remain false.

Do NOT claim or execute the v3 fixture.

### v2

Derive one in-memory v2 compatibility payload from that exact v3 fixture using only the supported legacy transformation:
- `schema_version = "2.0"`;
- remove the v3-only `dictionary` object;
- change only the dispatch identity/path as necessary to keep it unique.

Run it through the installed normalizer/common validation path. Do not publish or execute it.

### v0.6

Before execution, validate the exact immutable legacy canary blob through the installed common validation path.

Record:
`PROJECT_DICTIONARY_BINDING`,
`DISPATCH_V3_SCHEMA_BINDING`,
`DISPATCH_V3_STRUCTURAL_CONFORMANCE`,
`DISPATCH_V3_RUNTIME_COMPATIBILITY`,
`V2_COMPATIBILITY`,
`V06_COMPATIBILITY`.

Any compatibility failure: STOP before canary claim.

## Phase 3 — real installed Tray/Worker certification while intake remains PAUSED

Use the real installed runtime and registered startup path.

Required proof:
1. start the owned startup task / stable launcher;
2. exactly one Tray and one Worker become healthy;
3. heartbeat advances;
4. duplicate Tray/Worker attempts are rejected by singleton locks;
5. current state remains PAUSED and no canary is claimed yet;
6. request graceful exit;
7. prove processes exit and locks release;
8. restart once;
9. prove heartbeat resumes and 001–008 remain non-replayable.

No arbitrary process kill.

If graceful control cannot stop the owned processes, STOP rather than force kill.

## Phase 4 — execute exactly one real Worker canary

Only after Phases 0–3 PASS:

1. prove the final009 legacy canary is the only new eligible `auto_execute` identity;
2. record canary branch remote head = `501822a...`;
3. resume Bridge intake;
4. trigger normal Worker check-now / normal Worker polling;
5. allow installed Worker to discover and claim the canary exactly once;
6. do NOT run `e2e-once` manually for this canary;
7. do NOT call Codex directly for the canary;
8. wait for terminal canary state.

Required successful terminal state:
`PUSHED_UNREVIEWED`.

Immediately after terminal state, PAUSE intake again.

Required Agent/application evidence:
- product CODEX;
- model policy PINNED;
- requested model `gpt-6.1-sol`;
- requested reasoning `medium`;
- permission profile FULL_ACCESS;
- Codex sandbox/approval application corresponds to danger-full-access + never;
- no Agent substitution;
- max_runs=1.

Required result evidence:
- canary branch remote head advances exactly once from `501822a...`;
- changed paths are only under `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/**`;
- required `agent_result.json` exists remotely;
- marker is `FOX2_BRIDGE_FINAL_CANARY_009_AGENT_OK`;
- Bridge runtime report records the pushed result head;
- exact Git remote readback equals that head.

Usage:
- if structured Agent usage/capacity is exposed, persist it;
- if it is not exposed, record exactly `NOT_EXPOSED_WITH_EXECUTION_PROOF` with the successful real execution evidence.
Never fabricate numeric quota/usage.

If canary fails after claim, it is consumed. STOP and report NEEDS_RECONCILIATION; never replay it or silently substitute another Agent.

## Phase 5 — post-canary restart/no-replay

After canary success:

1. graceful exit real Tray/Worker;
2. restart through the owned startup path;
3. keep intake PAUSED after restart;
4. prove the final canary cannot be claimed/executed again;
5. prove canary branch head does not advance a second time;
6. prove all 001–008 remain blocked from replay;
7. export final sanitized real diagnostics/support evidence.

## Phase 6 — final evidence / publication

Write new evidence only under:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/**`

At minimum publish:
- `startup_task.json`;
- `installed_compatibility.json`;
- `tray_worker.json`;
- `canary_execution.json`;
- `canary_remote_readback.json`;
- `usage.json`;
- `restart_no_replay.json`;
- `final_diagnostics.json`;
- `acceptance_gates.json`;
- `final_certification.json`.

`acceptance_gates.json` must carry all Batch-B required gates and must not erase historical facts.

Previous PASS evidence from 007/008 may be carried forward only by exact referenced evidence identity; do not rerun code tests merely for ceremony.

New final gates must be fresh real-runtime evidence.

Before publication:
- only final009 report paths changed on the Bridge task branch;
- secret scan PASS;
- `git diff --check` PASS;
- commit/push exact task branch;
- remote readback exact.

Controller terminal marker on technical success:

`FOX2_BRIDGE_FINAL_CERTIFICATION_009_PUSHED_UNREVIEWED`

This is NOT CHAT acceptance.

Do NOT write `INTERNAL_FOX2_BRIDGE_READY` as an accepted project state. CHAT alone performs final intake and may accept that marker after remote evidence review.

On any material failure, publish truthful `STOPPED_NEEDS_RECONCILIATION` evidence when safe and STOP.
