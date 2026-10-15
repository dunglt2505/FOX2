# FOX2 Bridge Batch B — Final Installed-Runtime Certification 013

Status: FINAL BOUNDED RECONCILIATION OF EXISTING WHOLE-WP.

Controller 012 is CONSUMED. Never replay 001–012.

Certified production source:
501822a33ef08c7365154913bbc677544856eee5

Controller source/task head:
167482376e1d725e3723ccc249284a76edcf5e4e

Installed certified package:
6d6b66b6fa8d1b986835e3bf4368a9f7a8749a37f687c79d2ed4d95d88f3d5a6

Observer 013:
- commit: 60a566ba06d83b303cc7a92b832d89b24562c851
- blob: 0f256505f49d8a545f0c8e82973e24de8c29ddb8
- sha256: 3585a8f7211466c40b270ef2fd7f242913a5dcd04b7ba952fac60d57df46e96e
- raw bytes: 3017
- schema: FOX2_CERT_PROCESS_OBSERVER_2

Production mutation is NOT authorized.
Do not modify agent_bridge/**.

## Proven reason for 013

Controller 012 stopped Phase 3 because observer reported Tray=1 / Worker=0.

Subsequent bounded diagnosis proved a real Worker with:
- exact certified runtime/Scripts/python.exe;
- argv `-m fox2_agent_bridge worker`;
- ParentProcessId equal to the observed Tray PID;
- live PAUSED ledger and advancing heartbeat.

Observer 013 fixes only certification observation:
- exact Worker executable;
- corrected argv matcher:
  `(?i)(^|\s)-m(?:\s+|=)fox2_agent_bridge\s+worker(?:\s|$)`
- Worker parent PID must belong to the observed Tray PID set.

## Carry forward exact existing PASS evidence

Use exact final012/core008 identities.

Do NOT rerun 373 tests merely for ceremony because production source is unchanged.

Carry:
- package/install/update/uninstall/reinstall;
- environment isolation;
- 29 focused tests;
- 373 full tests;
- startup ownership;
- sanitized diagnostics;
- Dictionary binding;
- v3 schema/structural/runtime compatibility;
- v2 compatibility;
- v0.6 compatibility;
- changed-path/security evidence where applicable.

## Fresh Phase 3

Use ONLY the already-materialized Observer 013 path supplied by launcher.

While intake PAUSED:

1. require pre-start observer = Tray 0 / Worker 0;
2. start owned SID-qualified startup task;
3. bounded-wait for exactly Tray 1 / Worker 1;
4. require worker executable_exact=true;
5. require argv_exact=true;
6. require parent_is_tray=true;
7. prove heartbeat advances and ledger is PAUSED;
8. duplicate startup must not create duplicates;
9. Canary 009 remains unclaimed;
10. graceful request-exit only;
11. require observer 0/0 and lock released;
12. restart owned path;
13. again require exact 1/1 + heartbeat;
14. prove Dispatches 001–012 remain non-replayable.

No arbitrary process kill.

## Phase 4 — exact existing Canary 009 once

Only after Phase 3 PASS.

Dispatch:
FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001

Branch:
work/FOX2-BRIDGE-FINAL-CANARY-009

Base:
501822a33ef08c7365154913bbc677544856eee5

Do not create another canary.

Use normal installed Worker polling/check-now.
Do NOT manually call e2e-once.
Do NOT directly invoke Codex for Canary.

Required immutable Canary Agent configuration:
CODEX / PINNED / gpt-6.1-sol / Medium / FULL_ACCESS.

Success:
PUSHED_UNREVIEWED.

Immediately PAUSE intake after success.

Require:
- one claim/execution only;
- no Agent substitution;
- max_runs=1;
- FULL_ACCESS applied;
- canary branch advances exactly once;
- changed paths only final009/canary/**;
- agent_result.json exists;
- marker FOX2_BRIDGE_FINAL_CANARY_009_AGENT_OK;
- exact remote readback.

Usage may be NOT_EXPOSED_WITH_EXECUTION_PROOF.
Never invent numeric usage.

## Phase 5 — post-canary restart/no-replay

- graceful exit;
- observer 0/0;
- restart owned path;
- observer exact 1/1;
- intake PAUSED;
- Canary cannot execute again;
- Canary branch does not advance twice;
- 001–012 remain blocked;
- fresh sanitized diagnostics.

## Publication

Controller writable repository scope ONLY:

reports/BRIDGE-DESKTOP-BATCH-B/evidence/final013/**

Canary Agent keeps its already-authorized immutable final009/canary/** scope.

Before task-branch push:
- product source unchanged;
- final013 changed-path allowlist PASS;
- secret scan PASS;
- git diff --check PASS.

Publish/read back exact task branch.

Technical success marker:

FOX2_BRIDGE_FINAL_CERTIFICATION_013_PUSHED_UNREVIEWED

This is NOT CHAT acceptance.

Only CHAT grants:

INTERNAL_FOX2_BRIDGE_READY

Any material failure:
publish truthful bounded final013 stop evidence and STOP.
