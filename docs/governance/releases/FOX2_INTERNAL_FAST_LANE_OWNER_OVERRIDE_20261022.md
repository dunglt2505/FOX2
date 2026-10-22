# FOX2 — Internal Fast Lane — Owner Standing Override — 2026-10-22

**Project:** FOX2 only  
**Authority:** Direct Owner instruction on 2026-10-22 to simplify FOX2 because it is an internal project and the existing process is slowing delivery.  
**Status:** `OWNER_APPROVED_STANDING_INTERNAL_OVERRIDE`  
**Applies to:** new/re-scoped FOX2 INTERNAL_ONLY / NON_LIVE work after publication of this record.  
**Does not silently rebind:** any already-issued immutable Dispatch, including the current R5 Dispatch.

## 1. Objective

Reduce FOX2 administrative latency while preserving correctness, source integrity, no-replay and honest acceptance.

The operating unit is the **Whole-WP / feature outcome**, not a chain of Owner-facing micro-gates.

CHAT MUST prefer the smallest amount of governance evidence that still proves the material facts.

## 2. Scope

Fast Lane applies when ALL are true:

- FOX2 internal development, internal test, localhost/Owner-host validation, or internal readiness;
- bounded non-main branch/worktree;
- no Production provider side effect;
- no broker/order write;
- no real-money action;
- no LIVE enablement;
- no main/merge/deploy authority is implied;
- no external legal/contract/entitlement requirement is being waived.

If any excluded action becomes material, leave Fast Lane for that action only.

## 3. Non-waivable invariants

Fast Lane retains these material controls:

1. **Source/scope lock:** know the exact source/result base, branch and allowed product paths before mutation.
2. **One writer:** no competing material writer for the same task/worktree at mutation time.
3. **No replay:** a consumed Dispatch/attempt identity is never replayed.
4. **Bounded permissions:** no path/permission expansion by implication.
5. **Real evidence:** FAIL/BLOCKED/NOT_RUN remain factual; no synthetic PASS.
6. **CHAT acceptance:** Agent push/self-report is never final acceptance.
7. **External boundary:** main/merge/deploy/provider/broker/LIVE remain separate explicit decisions.

Everything else is risk-proportionate and may be combined or reused.

## 4. Simplified internal execution contract

### 4.1 CHAT read-only / planning / document work

CHAT acts directly.

No Agent PreExec, Dispatch, PASS_TO_ASSIGN artifact or WORK review is required merely for read-only analysis, roadmap, source comparison, status update or permitted candidate documentation.

### 4.2 First executable attempt for a Whole-WP task

For a genuinely new executable task:

- resolve current Owner-approved source and immutable task scope;
- use `fox2-agent-prompt-builder`;
- publish/read back task + prompt;
- select Actor/Model/Thinking once;
- verify only material route capability, worktree, writer and permission;
- issue one fresh Dispatch.

R0-R7 remains CHAT's reasoning method but is recorded as **one compact assignment decision**, not a set of separate Owner-facing artifacts.

### 4.3 Bounded correction after CHAT REWORK

If ALL remain unchanged:

- same Whole-WP objective;
- same Actor/Model/Thinking;
- same permission profile;
- same branch family;
- same allowed code/test paths;
- same external-rights boundary;

then a bounded correction is **not a new Owner-facing task**.

CHAT MAY:

- reuse the existing task/prompt/source authority;
- bind the prior result SHA as unaccepted salvage when appropriate;
- issue a **fresh Dispatch identity with a concise correction delta**;
- reuse previous valid route/host/source PASS;
- run only a lightweight pre-consume check for changed/time-dependent facts.

CHAT MUST NOT:

- replay the consumed Dispatch;
- silently broaden paths/rights;
- relabel historical failures PASS.

A new full task/prompt/PreExec cycle is required only if a material execution-envelope input changes.

## 5. PreExec simplification

For INTERNAL_ONLY work, a full durable PreExec receipt is required only when one of these changes materially:

- Actor/Model/Thinking;
- permission profile;
- host/toolchain capability;
- worktree/branch/source binding;
- writer state;
- external side-effect class;
- task scope/allowed paths.

For bounded retry/correction under an unchanged execution envelope:

- reuse valid prior PASS evidence;
- recheck only time-dependent facts immediately before consume;
- record the result in the Dispatch/launcher/result receipt;
- **no standalone PASS_TO_ASSIGN document is required**.

A failure stops only the affected action.

## 6. Result evidence simplification

For INTERNAL_ONLY DEV/TEST results, the minimum result contract is:

- observed remote result SHA;
- actual code/test diff;
- focused tests for changed behavior;
- affected regression suite;
- `git diff --check`;
- changed-path allowlist;
- concise report;
- evidence manifest sufficient for CHAT readback.

Do NOT create redundant evidence files for facts directly reproducible from Git or already present in the report.

Full-suite rerun is required only when:

- shared/common behavior changed;
- regression blast radius is broad;
- acceptance/spec explicitly mandates it;
- CHAT identifies a material dependency edge.

K1 remains a method for unexplained changes, not a reason to generate artifact volume.

## 7. Independent audit simplification

For INTERNAL_ONLY work, WORK independent audit is **not a default gate**.

Use independent audit only when at least one is material:

- irreversible or difficult-to-recover state transition;
- real financial/real-money safety;
- external provider/broker/LIVE boundary;
- materially contested source authority;
- high-risk concurrency/recovery where CHAT review alone is insufficient;
- Owner explicitly requests independent review.

Otherwise CHAT result review is the acceptance authority for internal readiness.

## 8. Bridge fast path

For the current Bridge Whole-WP, after the current R5 immutable Dispatch completes and R5 receives `CHAT_ACCEPT`:

replace the previous sequence

`A05 -> G3 -> G4 -> independent pre-Canary audit -> Canary -> restart/no-replay -> final intake`

with:

`R5 CHAT_ACCEPT -> BRIDGE_INTERNAL_VALIDATION -> FINAL_CHAT_ACCEPTANCE -> INTERNAL_FOX2_BRIDGE_READY`

### BRIDGE_INTERNAL_VALIDATION

One integrated Owner-host run SHOULD combine, where technically safe:

- A05 continuation lifecycle from existing reusable A04 evidence;
- remaining G3/G4 internal integration assertions;
- local/internal runtime trial;
- graceful stop/restart;
- singleton/no-replay verification;
- final safe-state check.

Rules:

- stop at first material failure;
- preserve earlier reusable PASS;
- do not rerun unaffected stages;
- one result/evidence package;
- one CHAT review.

Independent WORK pre-Canary audit is waived for this INTERNAL_ONLY path unless a trigger in section 7 appears.

This Fast Lane does **not** authorize real provider/broker/LIVE activity.

## 9. Project roadmap presentation

Owner-facing roadmap uses three outcome bands only:

1. **BUILD / CORRECT** — code or bounded correction reaches CHAT_ACCEPT.
2. **INTERNAL VALIDATE** — integrated internal functional/runtime validation.
3. **READY** — final CHAT acceptance for the internal milestone.

Detailed checks remain internal evidence, not separate roadmap milestones unless they reveal a real blocker or new authority boundary.

## 10. Current R5 handling

The already-published R5 task/prompt/PreExec/Dispatch/launcher remain immutable and are not rebound by this standing override.

Fast Lane applies to:

- CHAT review of the R5 result using minimal sufficient evidence;
- any subsequent bounded correction only under section 4.3;
- the post-R5 Bridge path under section 8.

## 11. Status semantics

Use:

- `PASSED_REUSABLE`
- `FAILED`
- `NOT_RUN`
- `BLOCKED`
- `OWNER_WAIVED`

Do not invent PASS for waived/unrun checks.

## 12. Effective interpretation

This record is an Owner-approved **human operating standing override** under FOX2 Policy v2.0.0.

It supersedes conflicting older internal sequencing/process requirements only within the scope above.

It does not claim installed runtime enforcement and does not alter external permissions.

`FOX2_INTERNAL_FAST_LANE=OWNER_APPROVED / INTERNAL_ONLY=YES / NON_LIVE=YES / WHOLE_WP_FIRST=YES / REUSE_PASS=YES / MICRO_GATE_ARTIFACTS=MINIMIZED / NO_REPLAY=RETAINED / CHAT_ACCEPTANCE=RETAINED / EXTERNAL_RIGHTS=UNCHANGED`
