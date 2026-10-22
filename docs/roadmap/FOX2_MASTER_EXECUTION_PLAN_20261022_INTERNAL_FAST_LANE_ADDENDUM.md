# FOX2 — Master Execution Plan Addendum — Internal Fast Lane — 2026-10-22

**Status:** OWNER-DIRECTED / INTERNAL_ONLY FAST LANE  
**Authority:** FOX2 Policy v2.0.0 + `FOX2_INTERNAL_FAST_LANE_OWNER_OVERRIDE_20261022.md`  
**Scope:** FOX2 internal development, local validation and internal readiness only.  
**External rights:** main/merge/deploy/provider/broker/LIVE remain separate and are not granted.

## 1. Planning model

Owner-facing work is managed in **three outcome bands**:

1. **BUILD / CORRECT**
   - implement or repair the product;
   - focused/affected regression evidence;
   - CHAT result review;
   - exit: `CHAT_ACCEPT`.

2. **INTERNAL VALIDATE**
   - integrated internal functional/runtime validation;
   - combine compatible host/runtime checks into one run;
   - stop on first material failure and preserve reusable PASS;
   - exit: `INTERNAL_VALIDATION_PASS`.

3. **READY**
   - one final CHAT intake of accepted code + integrated validation;
   - exit: the named internal milestone, e.g. `INTERNAL_FOX2_BRIDGE_READY`.

Individual checks such as PreExec, A05, G3, G4, local runtime trial, restart/no-replay and evidence reconciliation are **internal checks**, not separate Owner-facing milestones unless a real blocker or authority boundary appears.

## 2. Assignment simplification

For a new executable Whole-WP task:
- one source/task/prompt binding;
- one selected route;
- one full material PreExec;
- one fresh Dispatch.

For a bounded correction after `CHAT_REWORK`, when execution envelope and code-path scope are unchanged:
- keep the same Whole-WP;
- reuse task/prompt/source authority;
- issue a fresh no-replay Dispatch containing the correction delta;
- recheck only changed/time-dependent facts;
- do not create a new Owner-facing WP or repeat full governance publication.

## 3. Evidence simplification

Use the minimum reproducible evidence set:
- remote result SHA;
- code/test diff;
- focused tests;
- affected regression;
- diff check/path allowlist;
- concise report + manifest.

Do not generate duplicate source-binding, code-diff, static-check and summary artifacts when the same fact is directly reproducible from Git and already represented in the report/manifest.

Full suite is risk-triggered, not ritual:
- shared/common code;
- broad dependency impact;
- explicit acceptance mandate;
- CHAT identifies material regression risk.

## 4. Review simplification

CHAT is the default internal reviewer.

WORK independent review is exceptional and triggered by:
- real financial safety;
- provider/broker/LIVE boundary;
- materially irreversible/high-risk recovery or concurrency;
- contested source authority;
- explicit Owner request.

No routine independent pre-Canary audit for an INTERNAL_ONLY path.

## 5. Bridge current critical path

Current R5 remains pinned to its already-published immutable task/prompt/PreExec/Dispatch/launcher.

After R5:

```
R5 CODEX result
  -> CHAT result review
  -> if ACCEPT:
       BRIDGE_INTERNAL_VALIDATION
         = A05 continuation
         + remaining G3/G4 internal assertions
         + local/internal runtime trial
         + graceful stop/restart
         + singleton/no-replay
         + final safe state
       -> one CHAT review
       -> FINAL_CHAT_ACCEPTANCE
       -> INTERNAL_FOX2_BRIDGE_READY
```

No separate Owner-facing:
- A05 milestone;
- G3 milestone;
- G4 milestone;
- independent pre-Canary audit milestone;
- Canary milestone;
- restart milestone.

They are internal checks inside `BRIDGE_INTERNAL_VALIDATION`.

If one internal check fails:
- keep prior PASS reusable;
- correct the earliest causal defect;
- resume only affected checks;
- do not rerun the entire chain.

## 6. Release boundary

Internal-ready does not authorize:
- main;
- merge;
- deployment to production;
- real provider access;
- broker write;
- LIVE.

Those require a separate explicit consequential-action decision.

## 7. Operating summary

`FOX2_FAST_LANE_ROADMAP = BUILD/CORRECT -> INTERNAL_VALIDATE -> READY`

`CURRENT_BRIDGE = R5 -> BRIDGE_INTERNAL_VALIDATION -> FINAL_CHAT_ACCEPTANCE -> INTERNAL_FOX2_BRIDGE_READY`
