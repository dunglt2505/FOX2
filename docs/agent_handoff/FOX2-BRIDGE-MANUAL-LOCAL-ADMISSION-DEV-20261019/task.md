# FOX2 — Manual Local Admission Infrastructure: Source-Ready Task Candidate

**Project:** FOX2 only
**WP ID:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`
**Status:** `SOURCE_READY_DOCUMENT_CANDIDATE / OWNER_CODE_SCOPE_MISSING / PREEXEC_NOT_RUN / ASSIGNMENT_HOLD / NO_EXECUTABLE_DISPATCH`
**Control:** CHAT / code implementation only after a separately approved scoped grant, own PreExec receipt and own executable Dispatch.
**Source-ready branch:** `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`
**Frozen inspected implementation base:** `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`
**Authoritative source for this candidate:** immutable Git commit containing this exact `task.md` after publication; NEVER mistake base SHA for task SOURCE_HEAD.
**Proposed Windows task worktree:** `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019` (not created or verified by CHAT).
**Current date:** 2026-10-19.

## 1. Purpose and scope

Resolve a material infrastructure gap: FOX2 Dictionary v1.2 declares `MANUAL_LOCAL`, but the inspected Bridge `dispatch_normalizer.py` explicitly rejects non-`BRIDGE` execution paths, `__main__.py` has no dedicated manual admission CLI, and `manual_consumption.json` imports identity as `NEEDS_RECONCILIATION` rather than admitting a run. Build one governed, reusable operator-triggered manual admission path with durable exactly-once claim and fail-closed recovery, without replacing the existing Bridge engine or weakening auto-execution checks.

This is a **new bounded infrastructure dependency**, distinct from the already authorized PreExec compatibility task. It must NOT be implemented under that task's Dispatch or Owner grant.

## 2. Immutable source/authority binding

- WP Registry: `b27f1085ee13d8dce56fd2735e100ea1616e6e23:docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json`, scoped WP-only.
- Frozen governance: `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`, Dictionary v1.2 / Policy v1.8.9 / Routing v1.3 / Git-first Protocol v12 / shared PreExec v1.1 and Receipt Schema v1.
- Engineering contract candidate: `1177388dd8e75697778f25cd166cced672653b5d:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_SOURCE_IMPACT_BOOTSTRAP_CANDIDATE_20261019.md`.
  - Git blob SHA-1: `f7496977ddc5993c847bb84a0b41106cf4566dda`.
  - SHA-256: `5a9a9913389051af65ab70b707c3f25bd10fd0d60be982aed3230c191e46eebc`.
- Historical bounded Owner approval `bdaa6fd2be14b03e607fa52f91aa237596481780` authorizes ONLY PreExec compatibility scope and its four code paths; **not** the six infrastructure code paths below. A fresh explicit infrastructure code grant is REQUIRED.
- Old compatibility Dispatch `FOX2-DISPATCH-PREEXEC-COMPAT-CODEX-001` publication `3f885b2d24cb131b5e96dfdb67a44677599197e2`; `MANUAL_LOCAL / AGENT / CODEX gpt-6.1-sol medium FULL_ACCESS / max_runs=1`; PUBLISHED but HOST_ADMISSION=HOLD.
- Canary009 protected `work/FOX2-BRIDGE-FINAL-CANARY-009` @ `501822a33ef08c7365154913bbc677544856eee5`; remains HOLD.
- No assumption that highest version/main/source candidate grants EFFECTIVE authority. A private Git document is not an independent signature.

## 3. Permission and readiness gates

`POLICY_CHECK -> TASK_STATE_CHECK -> SOURCE_BINDING_CHECK -> ROUTING_R0_R7 -> PREEXEC_REQUIREMENTS_BIND -> MATERIAL_PREFLIGHT_RUN -> CHAT_INTAKE -> ASSIGNMENT_CHECK -> EXECUTABLE_DISPATCH -> HOST_ADMISSION`

**Present reality:** Only this candidate engineering/task publication is permitted by the current request. No proof of a new code grant, fresh Windows host worker exclusion, new task PreExec, CHAT PASS_TO_ASSIGN or new infrastructure Dispatch exists.

Before any infrastructure implementation:
1. Record an explicit Owner-authorized, path-scoped grant for this new WP. The prior authorization MUST NOT be inherited or expanded.
2. Verify exact task Git SOURCE_HEAD (the immutable publication commit), new branch/worktree, exclusive writer, absence of unrelated WIP and current/legacy ledger/marker state for the new identity.
3. Run actual shared PreExec v1 with correct `Requirements` bound to this new WP; never use a Batch-B or prior compatibility task profile. Provisional receipt path `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_receipt.json`. Publish only under an approved branch/path and remote byte-readback.
4. CHAT independently reviews receipt and R0-R7, routes Agent/Model/Thinking and grants PASS_TO_ASSIGN only if justified.
5. Publish one new separate immutable executable Dispatch via Dictionary-derived Schema v3 and canonical control path, only after all preceding gates PASS.
6. Confirm installed Bridge implementation, `e2e-once` compatibility, operator control state, singleton lock, no-replay and paused/stop behavior. Never bypass PAUSED, silently resume workers, or activate via an unrecorded direct CLI.

Proposed implementation route (NOT YET ASSIGNED): `CODEX / PINNED gpt-6.1-sol / medium / FULL_ACCESS / execution_path=BRIDGE / delivery_owner=BRIDGE`. CHAT must verify current capability and final tuple; if concurrency/safety risk requires High, seek a separately governed routing decision rather than silently changing pinned dispatch. Proposed bootstrap is existing explicit `fox2-bridge e2e-once --dispatch-path <NEW_INFRASTRUCTURE_DISPATCH_PATH>`, contingent on all host checks and safe worker controls. This is NOT an activation command issued by this candidate.

## 4. Proposed path-scoped implementation allowlist (Owner approval pending)

Six primary exact code/test files:

1. `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py` — mode-aware validation, explicit manual path; keep normal `BRIDGE` auto-execution guard.
2. `agent_bridge/src/fox2_agent_bridge/e2e_runner.py` — reuse validation/claim/adapter/checkpoint pipeline; distinguish manual operator admission without cloned engine.
3. `agent_bridge/src/fox2_agent_bridge/app.py` — controlled manual entrypoint using shared singleton lifecycle.
4. `agent_bridge/src/fox2_agent_bridge/__main__.py` — one explicit `manual-once` command, name candidate only until adopted.
5. `agent_bridge/tests/test_project_dictionary.py` — preserve BRIDGE auto rejection, validate manual route only through explicit entrypoint.
6. `agent_bridge/tests/test_e2e_runner.py` — synthetic integration/no-replay/race/crash tests.

**Conditional, excluded until separately justified and authorized:** `agent_bridge/src/fox2_agent_bridge/ledger.py`, `desktop.py`, `process_lock.py`, `codex_adapter.py`, `agent_policy.py`, `config.py`, `ops_runner.py`, `dispatch_poller.py`, `project_dictionary.py`, `agent_bridge/scripts/generate_project_dictionary.py`, their tests, schema/Policy/Registry and all other paths. Runtime ledger extensions may prove necessary; require exact source-impact/consumer evidence before scope expansion. No `agent_bridge/**` blanket grant.

All code hunks need K1 trace: `REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED`. No unrelated edits.

## 5. Acceptance requirements (fixtures and disposable remotes; NO real Dispatch/Canary run)

- Exact mutable ref + immutable commit/blob/SHA-256 source checks; reject source or prompt drift and conflicted/unknown authority.
- Dictionary/Policy/Owner/source/CHAT admission check with correct project/task, branch/worktree/base, permissions and pinned route; no alternate-model fallback.
- Single OS-backed writer/runtime lock; atomic durable claim + execution row BEFORE spawn. At most one attempt, no time-of-check/time-of-use gap.
- Current and legacy ledger, manual marker, worker PAUSED/stop, competing processes and previously started/consumed/unknown state fail closed. A marker alone is never a launch permit.
- Crash/timeout before/after claim/spawn/checkpoint, nonzero exit and partial publication -> `NEEDS_RECONCILIATION` when uncertain, preserve no-replay.
- Manual explicit path never auto-selected by `run-next`; existing `BRIDGE` paths retain behavior.
- Changed-path allowlist, K1 diff trace, secret scan, expected-head Git push and exact remote readback; no fabricated PUSHED/ACCEPTED/EFFECTIVE.
- Verify legacy PreExec v1 and known consumer compatibility. Tests must prove real Canary009 and old Dispatch001 are not claimed, rewritten or launched.

Deliver source-bound Result v2, test summary/JUnit, K1 trace, actual diff and immutable branch commit. CHAT decides ACCEPT/REWORK/HOLD. Installed runtime adoption is a SEPARATE gated operation with worker quiescence, rollback and safe restart.

## 6. Strict boundaries / next step

No code, PreExec receipt, runtime publication, executable Dispatch, worker start/resume/stop, manual marker, ledger write/claim, CODEX launch, PR, main/merge, install, provider/broker/LIVE or Canary execution is authorized by this task candidate. Preserve Dispatch001 and Canary009 unchanged.

**NEXT_OWNER:** CHAT for scoped Owner authorization and independent source/readiness check. HOST OPERATOR for Windows-only PreExec after that grant. CODEX only after successful separate BRIDGE bootstrap admission.

```text
INFRA_TASK_DOCUMENT=SOURCE_READY_CANDIDATE_ONLY
OWNER_INFRA_CODE_SCOPE=MISSING
INFRA_PREEXEC=NOT_RUN
CHAT_ASSIGNMENT=HOLD
INFRA_DISPATCH=NOT_PUBLISHED
BRIDGE_BOOTSTRAP_ADMISSION=NOT_RUN
IMPLEMENTATION=NOT_STARTED
DISPATCH001=PUBLISHED_HOLD
CANARY009=HOLD
```
