# FOX2 — Canary009 PreExec Compatibility: Source-Ready Engineering Task

**Project:** FOX2 only  
**Task/WP id:** `FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018` (bounded supporting work under `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`)  
**Status:** `OWNER_APPROVED_SCOPED_CODE / SOURCE_READY / EXECUTABLE_ASSIGNMENT_HOLD_FRESH_V1_PREEXEC`  
**Task branch:** `work/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018`  
**Frozen inspected implementation base:** `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`  
**PreExec current task SOURCE_HEAD:** immutable Git commit containing *this* `task.md`; CHAT must read branch HEAD at intake. Never use the base commit or `main` as a substitute.  
**Expected Windows worktree:** `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018` (NOT CREATED/NOT VERIFIED as of this task publication).

## 1. Actual Owner authority — limited to the new coding task

Owner approved this semantic compatibility change and its minimal file-scoped implementation in CHAT on 2026-10-18. Bound authenticated Git approval:

`bdaa6fd2be14b03e607fa52f91aa237596481780:docs/governance/releases/FOX2_CANARY009_PREEXEC_COMPAT_OWNER_SEMANTIC_CODE_AUTHORIZATION_20261018.json`.

This grants **bounded source scope** and permission to PREPARE source-ready task material. It does **not** admit an executable coding Agent, waive the task's own PreExec, authorize changing current EFFECTIVE schema bytes or grant Canary launch, merge/LIVE or other protected rights.

```text
SEMANTIC_COMPATIBILITY_SCOPE_OWNER_APPROVED=YES
CODE_ALLOWED_FOR_BOUNDED_SCOPE_ONCE_PREFLIGHT_AND_CHAT_INTAKE_PASS=YES
CODE_ALLOWED_FOR_EXECUTION_NOW=HOLD_FRESH_PREEXEC
TASK_EXECUTABLE_DISPATCH_ALREADY_PUBLISHED=NO
TASK_IMPL_AGENT_STARTED=NO_AS_OF_CHAT_PUBLICATION_NOT_HOST_PROOF
CANARY009_EXECUTABLE_DISPATCH_ALREADY_PUBLISHED=YES (SEPARATE IMMUTABLE TASK)
CANARY009_CURRENT_CONSUMPTION=UNKNOWN_NOT_REOBSERVED
```

A fresh PreExec v1 receipt for this NEW coding task legitimately records `executable_dispatch_published=false`, `dispatch_consumed=false`, `agent_execution_started=false` when independently observed true for this coding task; do not falsely apply those values to Canary009.

## 2. Controlling source authority

- WP Registry `b27f1085ee13d8dce56fd2735e100ea1616e6e23` (WP_ONLY_TRUST_BINDING).
- Frozen governance source `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`: Dictionary v1.2, Policy v1.8.9, Routing v1.3, Git-first Protocol v12, PreExec v1.1, Receipt Schema v1, CHAT intake v1.1.
- Source-bound Owner location exception (NOT to be reapproved): `84ac87fbccc947c16490fb9365dc5a3d8e49661c`, four published `FOX2_CANARY009_*` files unchanged.
- Candidate contract/matrix/scope/package on evidence branch: `1e01fa9936a7f4b7c1ad097e55801c27c5319bf0` and their exact path + digest in package manifest.
- Protected immutable Canary task branch `work/FOX2-BRIDGE-FINAL-CANARY-009` @ `501822a33ef08c7365154913bbc677544856eee5`, existing dispatch `FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`, control source `dc79f8143eec471508bf37565bff38442ce0548a` and prompt source `530cc64feedbab463cefb0f5baed4e9919f25f15`.

No automatic `main` or newer-policy rebind. On drift/source conflict STOP and return to CHAT.

## 3. Mandatory PreExec for THIS NEW coding task (before implementation or executable Dispatch)

```text
TASK_BRANCH=work/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018
TASK_PATH=docs/agent_handoff/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018/task.md
RECEIPT_PATH=reports/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018/preexec/preflight_receipt.json
PREEXEC_CONTRACT=FROZEN_SCHEMA_V1_PRE_DISPATCH
```

1. On `FOXLE-PC`, read actual current remote task branch HEAD, source/Registry/Owner approval; verify the intended path does not contain unrelated WIP; verify local Git worktree ownership, exclusive writer, clean tree, permission and installed tooling.
2. Observe current Codex and Copilot authenticated capability/quota. Compare CHAT, COPILOT, CODEX, WORK; do not silently pin the implementation Agent to the separate Canary's CODEX tuple. Use non-implementation marker-only capability probes when scoped permissions permit and costs are justified; never the Canary marker or Dispatch.
3. Run the **shared** PreExec v1.1 engine with explicit `Requirements` bound to the task identity above, the exact new task head, and its actual worktree. The generic shared engine supports `Requirements` provided by a bounded host invocation without editing product code. `scripts/preexec.py --profile bridge` is the WRONG task identity because it binds historical Batch-B, not this new coding task. Do not fork the lifecycle or create a task-local validator.
4. Material checks include correct Python/Git/Pwsh and required test/build tooling, schema, source hash, writer/worktree safety, full current route capabilities, and actual permission/quota evidence; stop on UNKNOWN.
5. Only after all checks and safe single-writer admission, commit/push a Schema-v1 canonical receipt on **this exact task branch** under the `RECEIPT_PATH` above; preserve source task commit as `source_head`. Do not mark `RECEIPT_PUSHED` until exact remote commit/bytes readback.
6. CHAT reads receipt, validates all material R3/R5 gates, compares eligible Agents, then alone makes `PASS_TO_ASSIGN` and authorizes future executable coding Dispatch. No code edit or implementation Agent starts before then.

If current CLI lacks a correct task selector, use the **existing generic shared `PreExec(Requirements(...))` interface via a bounded, read-only preflight launcher outside the repo**; no product-code workaround, fake receipt or old Batch-B profile substitution. Any material unsafe host operation requires explicit task rights and STOP otherwise. Local probe/receipt writing is allowed only for the authorized preflight phase, NOT product code.

## 4. Implementation scope — after PASS_TO_ASSIGN only

Primary allowlist (exact):
- `agent_bridge/src/fox2_agent_bridge/preexec/engine.py`
- `agent_bridge/src/fox2_agent_bridge/preexec/profiles.py`
- `agent_bridge/scripts/preexec.py`
- `agent_bridge/tests/test_preexec.py`

New candidate contract artifacts permitted **only** if truly needed for approved semantic compatibility (no change to EFFECTIVE v1):
- `docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_EXISTING_DISPATCH_EXTENSION_CANDIDATE_20261018.json`
- `docs/agent_handoff/FOX2_CHAT_PREFLIGHT_EXISTING_DISPATCH_INTAKE_CANDIDATE_20261018.md`
- `docs/agent_handoff/FOX2_PREEXEC_EXISTING_DISPATCH_CONTRACT_ADDENDUM_CANDIDATE_20261018.md`

Only exact code change to introduce a **separate authenticated existing-published-dispatch revalidation profile** while leaving normal pre-Dispatch v1 behavior byte/semantically unchanged; distinguish `task_branch/source_head` from evidence publication branch/head and enforce immutable Git identities, real ledger, writer/WIP, atomic expected-head and remote byte readback.

No blanket `agent_bridge/**` allowance. `probes.py`, generated Dictionary and generator/test, poller, runner, main, any other source file require source-impact proof plus CHAT-approved allowlist extension **before** modification. No speculative refactor.

## 5. Acceptance checks and delivery

Required tests on fixtures and disposable Git remotes, never the real Canary:
- Old Schema v1 and existing PreExec PASS/BLOCKED/INFRA_FAILED contract behavior and relevant regression tests unchanged.
- Honest already-published Canary-like Dispatch `published=true`, never impersonated as false.
- Exact dispatch ID/source/head, SHA-256 `a8756aa6e66e98ba0a6fcc0995bf72fd175ef103a8bf9f27f79466535112576a`, prompt `dd9f45c5ac5f62bc8c65c53fe629a15d67381fe794e18956347fd1e9999ba3e0`, WP Registry and Owner exception validated or rejection before any probe/publication.
- `consumed=true`, `started=true`, missing/UNKNOWN or old/conflicting ledger → HOLD/STOP with no PASS/readiness.
- Distinct task/source and receipt publication branch, expected-head guarded, allowlisted one-file diff and exact-byte remote readback, no update of locked Canary branch.
- Conflict/WIP/competing writer/secret/remote drift/failed push or readback → fail closed and no false `RECEIPT_PUSHED`.
- Caller/consumer and generated binding tests only if actually affected.
- No `poll-once`, worker launch, `run-next`, `e2e-once`, claim, replay or Canary execution during compatibility tests.

After authorized implementation, Agent provides scoped diff, test evidence, Git result and source-bound report to CHAT. CHAT audits and decides whether contract release is permitted. **Installation/runtime adoption and a later real Canary host PreExec are separate.**

## 6. STOP

Unverified source authority; task branch/worktree/writer/permission drift; no valid preflight receipt; claimed/consumed Canary; material defects; unknown host ledger; generated binding incompatibility; out-of-scope paths; unrelated WIP; secret/readback mismatch; dispatch changes or alternative Agent substitution; protected branch head drift.

**Not authorized:** any other product work, main/merge, deploy/provider/broker/LIVE, Canary claim/replay/run or APP-B resume.
