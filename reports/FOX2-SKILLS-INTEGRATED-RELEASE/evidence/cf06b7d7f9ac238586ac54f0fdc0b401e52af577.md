# CHAT — FOX2 Project Dictionary Rollup Plan for BRIDGE-DESKTOP-BATCH-A

**Status:** SAME-WP MATERIAL REWORK / SUPERSEDES prior v2-only correction plans  
**Governance source:** Project Dictionary v1 -> Policy V1.8.7 -> Routing V1.2.8  
**Current Dispatch:** Schema v3 / Protocol v10  
**Canonical Dictionary source commit:** `28866ee6a61bde3fc3837ebd999c7b470afc7486`  
**Canonical Dictionary path:** `docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`

## 1. Objective

Fix the root cause once: Bridge code must not independently hard-code FOX2 current schema/control/path/version identifiers.

Implement a generated runtime binding derived only from the canonical Project Dictionary, then make config/poller/validator/normalizer consume that binding.

Do not create a second source of truth.

## 2. Generated binding

Add:

`agent_bridge/src/fox2_agent_bridge/project_dictionary.py`

This file is generated from the canonical JSON Dictionary and must include:
- source dictionary id/version/path;
- source dictionary SHA-256;
- project/repository/workspace ids;
- current/supported dispatch schemas;
- current/supported control branches;
- current/legacy dispatch path patterns;
- Agent/model-policy/permission/execution/delivery identifiers required by Bridge;
- protected authority defaults required by Bridge.

Add generator:

`agent_bridge/scripts/generate_project_dictionary.py`

Generator input is canonical Dictionary JSON. For this branch, it may read exact bytes via:

`git show 28866ee6a61bde3fc3837ebd999c7b470afc7486:docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`

or an explicit file argument containing those exact bytes.

Generated output must be deterministic UTF-8/LF.

No manual edits to generated constants.

## 3. Drift gate

Add a test that regenerates the binding from the pinned Dictionary and compares bytes/semantic content.

Required gate:

`PROJECT_DICTIONARY_BINDING=PASS`

A mismatch fails tests before runtime publication.

## 4. Config

Replace hand-coded current control branch with generated binding.

Default:
`work/FOX2-DISPATCH-chat`

Supported explicit legacy:
`work/FOX2-LOCAL-DISPATCH-chat`

Reject arbitrary branches.

One profile = one selected control branch. No multi-branch polling.

## 5. Poller

Discovery patterns come from generated binding.

Current canonical path:
`docs/agent_handoff/DISPATCH/<dispatch_id>.json`

Supported legacy:
- `docs/agent_handoff/DISPATCH_V2/<dispatch_id>.json`
- `docs/agent_handoff/<wp_segment>/dispatch/<dispatch_id>.json`

Filename identity remains exactly:
`<dispatch_id>.json`

Do not encode new schema versions into new folder names.

## 6. Dispatch schemas

Supported external:
- current `3.0`;
- legacy `2.0`;
- legacy `0.6`.

Implement:

```text
external dispatch
 -> schema-specific shape normalizer
 -> ONE normalized internal payload
 -> ONE common validator
 -> ONE existing execution engine
```

No duplicated execution pipeline.

### v3

Validate Dictionary block and cross-check:
- dictionary version/path/hash/commit;
- Policy version/path against Dictionary current Policy;
- project/repository/workspace;
- target Agent/routing identifiers;
- execution path;
- delivery owner;
- protected authority flags;
- runtime paths;
- required capabilities/tests;
- max_runs=1.

Bridge executes only `execution_path=BRIDGE`.

`MANUAL_LOCAL` / `VSCODE_ONE_CLICK` v3 dispatches are valid records but must be rejected for Bridge auto-execution before Agent spawn.

### v2

Preserve compatibility according to Dictionary. Normalize v2 shape into the same internal payload.

Do not assume v2 Policy version is current; validate as a legacy immutable dispatch against its own bound identity/safety fields.

### v0.6

Preserve current passing legacy behavior. Missing delivery_owner may retain historical default only for v0.6 if existing semantics require it.

## 7. Semantic boundary

Dictionary provides machine identity only.

Do not move Policy/BRD business or safety semantics into generated constants.

Protected authority false flags may be enforced both by dispatch shape and common validator as defense in depth.

## 8. Tests

Add focused tests proving:

- deterministic generator + drift PASS;
- current default control branch from generated binding;
- explicit legacy branch allowed;
- arbitrary branch rejected;
- canonical v3 path discovered;
- legacy v2/v0.6 paths discovered;
- unrelated JSON ignored;
- v3 CODEX tuple normalized exactly;
- v3 COPILOT Native Auto tuple normalized exactly;
- v3 AGENT/BRIDGE delivery owner preserved;
- v3 non-BRIDGE execution path not launched by Bridge;
- v3 dictionary hash/version/path mismatch fails closed;
- v3 Policy mismatch against Dictionary fails closed;
- v3 protected authority expansion fails closed;
- v2 compatibility PASS;
- v0.6 compatibility PASS;
- all schemas reuse same publication/replay/reconciliation execution path;
- full Bridge suite PASS;
- canonical artifact hygiene PASS;
- git diff check PASS.

## 9. Evidence

Update the existing:

`reports/BRIDGE-DESKTOP-BATCH-A/**`

Add acceptance:

```text
PROJECT_DICTIONARY_BINDING=PASS
PROJECT_DICTIONARY_DRIFT_CHECK=PASS
DISPATCH_V3_RUNTIME_COMPATIBILITY=PASS
V2_COMPATIBILITY=PASS
V06_COMPATIBILITY=PASS
STABLE_DISPATCH_PATH=PASS
CONTROL_BRANCH_REGISTRY=PASS
SINGLE_NORMALIZED_EXECUTION_PATH=PASS
```

Preserve all already-valid Batch A gates.

## 10. Scope

Writable:
- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-BATCH-A/**`

Read-only source:
- exact Project Dictionary commit/path above;
- Policy/BRD/Technical sources.

No backend/frontend/business semantic changes.

## 11. Delivery

Same WP, same branch, Agent-owned Git publication.

No PR/main/merge/deploy/provider/broker/LIVE.

Finish after remote push/readback with:

`FOX2_BRIDGE_DESKTOP_BATCH_A_DICTIONARY_ROLLUP_PUSHED_UNREVIEWED`
