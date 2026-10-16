# FOX2 Bridge RC1 — Routing, Intake and Release Decision

**State:** CHAT_LOCKED_PLANNING_BASELINE / NON_EXECUTABLE

## 1. Routing precondition

Before any RC1 product-code write or build/install certification:

```text
PROJECT_DICTIONARY_CHECK
-> POLICY_CHECK
-> TASK_STATE_CHECK
-> LIVE_GIT_CHECK
-> SOURCE_BINDING_CHECK
-> ROUTING_R0_R7
-> PREEXEC_REQUIREMENTS_BIND
-> FRESH PREEXEC
-> CHAT PREFLIGHT INTAKE
-> ASSIGNMENT_CHECK
-> EXECUTE
```

The historical Bridge receipt is not valid for RC1 because it binds `ac41a7e...`, while the current Bridge planning source is based on `d129f919...` and RC1 will materially add Desktop App/Artifact Vault integration.

## 2. Candidate comparison

CHAT MUST compare all currently eligible routes from fresh evidence.

Default comparison:
- CHAT: architecture, source binding, release decisions, intake, acceptance;
- COPILOT: clear WPF/XAML/boilerplate candidate when current auth/capacity PASS;
- CODEX: integration/recovery/installer/concurrency candidate when current auth/capacity PASS;
- WORK: independent release-readiness audit; not the default implementation route.

No candidate is selected from historical quota/auth facts. Fresh PreExec decides current eligibility.

## 3. Source/worktree ownership

Until a fresh executable handoff supersedes this planning baseline:
- current Bridge task branch remains `work/FOX2-BRIDGE-DESKTOP-BATCH-B`;
- current writable scope remains `agent_bridge/**` and `reports/BRIDGE-DESKTOP-BATCH-B/**`;
- all other paths remain read-only;
- no overlapping writer may own `agent_bridge/**`.

Desktop App integration SHOULD live under `agent_bridge/desktop_app/**` so it stays inside the existing writable boundary.

## 4. Execution scope for RC1 integration

One bounded implementation execution should absorb:
- WPF Desktop App source;
- two-process launcher topology;
- Desktop single-instance;
- Worker/UI lifecycle separation;
- package inclusion;
- update/uninstall integration;
- startup integration;
- local Artifact Vault;
- tests and evidence.

Do not fragment these into micro-WPs unless a material authority/source change requires re-scope.

## 5. STOP conditions

STOP for:
- exact source/head mismatch;
- stale or missing fresh PreExec receipt;
- wrong worktree/branch;
- overlapping `agent_bridge/**` writer;
- no eligible implementation route;
- Desktop App requires direct Git/ledger/Agent execution;
- Worker/UI separation cannot be proven;
- installer/update/uninstall failure;
- secret/private exposure;
- changed path outside allowlist;
- test/security failure;
- publication/readback failure.

## 6. Pre-Canary intake

CHAT may set `FOX2_BRIDGE_RC1_PRECANARY_READY` only after immutable evidence proves all non-Canary acceptance gates PASS.

WORK independent audit is required at this point because RC1 materially changes startup/launcher/process/package/recovery surfaces.

The audit must review at minimum:
- Worker/UI process isolation;
- startup and single-instance behavior;
- installer/update/uninstall safety;
- replay/reconciliation semantics;
- artifact persistence isolation;
- secret/log hygiene;
- evidence integrity.

WORK does not grant release authority; CHAT performs final intake.

## 7. Canary decision

Canary 009 is immutable:
`FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`

Rules:
- do not create a replacement Canary;
- do not edit the Canary branch/prompt/result contract;
- do not claim it before `FOX2_BRIDGE_RC1_PRECANARY_READY`;
- execute exactly once;
- exact Agent tuple/permission must match its immutable dispatch;
- remote result readback is mandatory;
- restart after completion must prove no replay.

Any uncertainty after Agent start is `NEEDS_RECONCILIATION`; never blind-replay.

## 8. Final CHAT intake

CHAT grants `INTERNAL_FOX2_BRIDGE_READY` only if:
1. RC1 exact source/package identities are known;
2. every required acceptance gate is PASS;
3. Canary 009 produced a valid remote result;
4. restart/no-replay is PASS;
5. no unauthorized source/path changed;
6. no secret exposure;
7. no open material blocker remains;
8. historical invalid closure is not used as supporting PASS evidence.

## 9. After Bridge acceptance

Only after `INTERNAL_FOX2_BRIDGE_READY`:
- resume `work/FOX2-M1-A-APP-BATCH-B`;
- preserve the already-approved UI direction;
- finish build/typecheck/API integration/tests/offline acceptance;
- then perform the genuine M1-A release integration boundary.

No Bridge result grants main/merge/deploy/provider/broker/LIVE authority.
