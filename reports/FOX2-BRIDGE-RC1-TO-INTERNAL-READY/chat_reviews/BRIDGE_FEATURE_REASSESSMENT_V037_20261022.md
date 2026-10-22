# FOX2 — Bridge Feature Reassessment — Skills v0.3.7

Date: 2026-10-22
Feature: `FOX2-BRIDGE-RC1`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Target: `INTERNAL_FOX2_BRIDGE_READY`

## Skills actually applied

- `fox2-source-resolver`
- `fox2-status-roadmap`
- `fox2-feature-certification`
- `fox2-project-health`
- `fox2-strategic-agent-triage`
- `fox2-agent-route-runtime`
- `fox2-governance-preflight`

The installed Skill content contains the v0.3.7 project-wide rules:
- focused correction + PASS preservation;
- per-gate `PASSED_REUSABLE / FAILED / NOT_RUN / BLOCKED`;
- residual-task `TASK_ROUTE_ASSESSMENT` before Actor/Model/Thinking selection;
- PreExec verifies the selected route and MUST NOT classify complexity or default to High.

## Live source/governance snapshot

Governance branch:
`work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019`

Observed current governance head:
`d34da1e3b4918a902646621b487ca8ad3e05b0e0`

Verified current blobs:
- Registry: `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`
- Current Source Resolution: `186fdbc72dc1b22e97330895142d68600591ac21`

Current accepted Bridge BUILD source:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

CHAT BUILD acceptance:
`cdf9f9c919102a2337ef357f4b658dc9993f48e5`

Master Plan reuse-first directive:
- commit `ad7d6f0b9889fe4247c29ac3d77f0b90b5f40e56`
- blob `6068b0e664d43afc87468e52785806dafc70b59f`

## Current SDLC classification

**Whole feature stage: TEST / IN_PROGRESS.**

Do not downgrade the whole Bridge to BUILD because one test/certifier defect needs a bounded BUILD correction.

The product BUILD source is already CHAT-accepted. The current R2 correction is a child BUILD activity inside the TEST stage.

## A04 bounded outcome

A04 result:
`92394d0ae68911c98bcdaa40aaa76ed56de66881`

CHAT A04 review:
`a3e49a62dbd340eacd8dc8369aa303ed0e93b6f3`

A04 acceptance matrix:
- PASS: 52
- FAIL: 3
- NOT_RUN: 21
- NOT_APPLICABLE: 1
- evidence items: 34

A04 is:
`CLOSED_CHAT_REWORK / CONSUMED / NO_REPLAY`

It is not a broad Bridge failure.

### PASSED_REUSABLE

The following A04 evidence remains reusable because the runtime subject is unchanged:

- exact package-source provenance;
- exact package build;
- package SHA `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`;
- package source `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- package/source/payload hash verification;
- per-user install/update;
- exact installed pointer/receipt;
- safe STOPPED/paused/setup/current_dispatch=null state;
- Worker/legacy absence;
- exact WPF singleton reached;
- durable state and SQLite integrity at failure checkpoint.

### FAILED / NOT_RUN and still material

- presentation-lock certification failed on real `PermissionError(errno=13)`;
- UI/exit/lock-release after that gate are not yet accepted;
- stable uninstall is NOT_RUN;
- preservation across uninstall is NOT_RUN;
- same-package reinstall is NOT_RUN;
- final installed safe state is NOT_RUN;
- G3 is NOT_RUN;
- G4 is NOT_RUN;
- current pre-Canary independent audit is NOT_RUN;
- current fresh Canary/restart/final intake are NOT_RUN.

## R2 route reassessment under v0.3.7

Current unrun R2 artifacts:
- task commit `9e1551d4e8e10aff3d302034c3f0c06588eac9ca`
- prompt commit `f6da01e9729b441ca80aece34ac282dd8195b12a`
- PreExec publication `da869f7171eb3e970e766ed3f8ff9100cfa316b0`
- receipt: ABSENT
- Dispatch: ABSENT
- Agent started: FALSE

These artifacts pin:
`CODEX / gpt-6.1-sol / high`

but were published before an explicit v0.3.7 `TASK_ROUTE_ASSESSMENT`.

Therefore:

**R2 current binding = SUPERSEDE_BEFORE_RUN.**

Do not run PreExec `da869f7171eb3e970e766ed3f8ff9100cfa316b0`.

### Correct R2 TASK_ROUTE_ASSESSMENT

Residual task:
external certifier correction only; 2 allowed files; known root cause; deterministic acceptance; no package build/install/host mutation.

- `COMPLEXITY=MEDIUM`
- ambiguity: LOW–MEDIUM
- `EXECUTION_RISK=MEDIUM`
- `SAFETY_OVERRIDE=NO`
- dependency impact: MEDIUM-HIGH because certifier controls later lifecycle acceptance
- evidence quality: HIGH (real A04 failure + accepted source + focused tests)
- route rationale: bounded edge-case implementation with clear negative fixtures; no architecture redesign or irreversible operation

Selected route candidate:
- Actor: CODEX
- Model: `gpt-6.1-sol`
- Thinking: `medium`
- Scope: exact two files + result/evidence
- STOP: any WPF product change, third product/test path, host mutation, G3/G4/Canary

This selected Medium route is not considered host-verified until a fresh route-specific PreExec proves actual model/effort/auth/capacity.

## Remaining task-level routing

### A05 continuation-only

- `COMPLEXITY=HARD`
- `EXECUTION_RISK=HIGH`
- `SAFETY_OVERRIDE=YES`
- reason: real host state, graceful exit, lock release, stable uninstall exactly once, durable preservation, same-package reinstall, no-replay
- candidate thinking: HIGH
- package rebuild/preinstall: forbidden if A04 archive remains hash-valid

### G3/G4 physical/adoption

- complexity: HARD
- execution risk: HIGH
- safety override: YES
- thinking: HIGH candidate
- route selected only after composite Host Lifecycle acceptance

### Independent pre-Canary audit

Independent reviewer is required by the Master Plan.
Actor/model/effort must be selected at task time after actual capability check; do not pre-pin from historical availability.

### Canary / restart / final intake

Canary is one-shot and no-replay-sensitive.
Treat as high-risk execution; select a high-safety route at task time and verify it with fresh PreExec.

## Feature progress assessment

Outcome-based estimate:

- product architecture/core implementation: substantially complete;
- BUILD acceptance: complete for current accepted product source;
- installed package/provenance/install prerequisites: materially proven and reusable;
- real lifecycle certification: partially proven, bounded failure at presentation-lock certifier;
- physical adoption / G3-G4: not run;
- independent current pre-Canary audit: not run;
- fresh Canary/restart/final intake: not run.

Estimated overall progress remains approximately **70–72%**, but this percentage should not be interpreted as 28–30% more coding. Most remaining work is runtime/release certification.

## Critical path

```text
TEST feature remains active
  -> supersede unrun R2 High binding
  -> fresh R2 with TASK_ROUTE_ASSESSMENT = MEDIUM
  -> PreExec verifies selected Medium route
  -> one bounded certifier correction
  -> CHAT_ACCEPT R2
  -> A05 continuation-only using reusable A04 PASS
  -> composite Host Lifecycle ACCEPT
  -> G3
  -> G4
  -> independent current pre-Canary audit
  -> fresh Canary
  -> restart/no-replay
  -> final CHAT intake
  -> INTERNAL_FOX2_BRIDGE_READY
```

## Verdict

`FEATURE_STATUS=TEST / IN_PROGRESS`

`BUILD_PRODUCT=CHAT_ACCEPTED`

`A04=BOUNDED_FAIL_WITH_REUSABLE_PASS`

`R2_CURRENT_HIGH_BINDING=SUPERSEDE_BEFORE_RUN`

`NEXT_SAFE_ACTION=REISSUE_R2_WITH_EXPLICIT_TASK_ROUTE_ASSESSMENT_AND_MEDIUM_THINKING_CANDIDATE`

`G3_G4_CANARY=HOLD`

No historical PASS is reset. No historical FAIL/NOT_RUN is promoted.
