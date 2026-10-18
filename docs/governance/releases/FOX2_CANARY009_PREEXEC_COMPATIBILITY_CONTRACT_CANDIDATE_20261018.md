# FOX2 — Canary009 Existing-Dispatch PreExec Compatibility Contract (CANDIDATE)

**Status:** `CANDIDATE_NOT_EFFECTIVE / NO_EXECUTION_AUTHORIZATION`
**Date:** 2026-10-18
**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
**Scope:** One *existing-published immutable dispatch* revalidation plus split receipt publication location. This is a proposed change to shared contract semantics, **not** an extension of the previously approved location-only exception into code or EFFECTIVE schema authority.

## 1. Exact frozen authority and identity

- WP-only Registry: `b27f1085ee13d8dce56fd2735e100ea1616e6e23:docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json`.
- Frozen source: `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`; Dictionary 1.2 / Policy 1.8.9 / Routing 1.3.0 / Protocol 12 / PreExec 1.1 / Receipt Schema v1 / Intake v1.1. The ten manifest/source SHA-256 families were rechecked from authenticated Git and matched their locked expected hashes, 10/10; this is **CHAT source-resolution equivalent**, not a claim of executing the installed Windows resolver.
- Frozen runtime code baseline: `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`.
- Prior blocker decision: `c73d1146463490e62bb698744e0f14ad9b189e0b:docs/roadmap/FOX2_BRIDGE_RC1_PREEXEC_BINDING_DECISION_20261018.json`.
- Already Owner-approved *location-only* exception: `84ac87fbccc947c16490fb9365dc5a3d8e49661c`, the four `docs/governance/releases/FOX2_CANARY009_*` approval/addendum/source-binding/impact files. **Do not modify or re-approve these files.**
- Executable dispatch: `FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`.
- Task branch and locked task head: `work/FOX2-BRIDGE-FINAL-CANARY-009` @ `501822a33ef08c7365154913bbc677544856eee5`. This HEAD must never advance for publication of the PreExec receipt.
- Immutable executable dispatch source: `dc79f8143eec471508bf37565bff38442ce0548a:docs/agent_handoff/FOX2-BRIDGE-FINAL-CANARY-009/dispatch/FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001.json`, SHA-256 `a8756aa6e66e98ba0a6fcc0995bf72fd175ef103a8bf9f27f79466535112576a`.
- Prompt source: `530cc64feedbab463cefb0f5baed4e9919f25f15:docs/agent_handoff/BRIDGE/FOX2_BRIDGE_FINAL_CANARY_009_PROMPT.md`, SHA-256 `dd9f45c5ac5f62bc8c65c53fe629a15d67381fe794e18956347fd1e9999ba3e0`.
- Agent tuple: `CODEX / gpt-6.1-sol / medium / FULL_ACCESS`, execution path `BRIDGE_DIRECT_CODEX_CLI`, delivery owner `BRIDGE`, `max_runs=1`. Preserve every component.
- Owner-approved *publication locator*: `work/FOX2-BRIDGE-RC1-PREEXEC-EVIDENCE-20261018:reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/preexec/preflight_receipt.json`. The path remains RESERVED, **NO RECEIPT CREATED**.

## 2. Proven incompatibilities — not a missing permission check

**Schema conflict:** EFFECTIVE `docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json` has `dispatch_state.executable_dispatch_published.const=false`; `dispatch_consumed.const=false`; `agent_execution_started.const=false`; root `additionalProperties=false`. EFFECTIVE `FOX2_CHAT_PREFLIGHT_INTAKE_CHECKLIST_v1.1.md` item 7 likewise demands `executable_dispatch_published=false` and assumes a new Dispatch has not yet been published. The existing Canary Dispatch is published=true. A truthful receipt for it is impossible in schema v1. No rewriting of truth or reinterpretation of false is permitted.

**Producer conflict:** `agent_bridge/src/fox2_agent_bridge/preexec/engine.py` (blob `9740fd959277e189e47f6d6a2e75dcf0e13dadfd`) hardcodes published=false in `failure_receipt` at line 190 and `build` at lines 281–282. `Requirements` uses one `branch`, `worktree`, and `source_head` as both execution-task identity and publication checkout. `hygiene` lines 227–249 demands that task branch/HEAD own that worktree; `publish` lines 327–363 pushes the same branch after a single-file commit. Existing shared `preexec.py --profile bridge` binds Batch-B identity and does not identify immutable Canary009. Location-only waiver cannot change these code semantics.

## 3. Two strictly separate lifecycle cohorts

| Cohort | Truth of executable dispatch | Applicable contract | Expected effect |
|---|---|---|---|
| `PRE_DISPATCH` (existing ordinary FOX2 workflows) | `executable_dispatch_published=false`, `dispatch_consumed=false`, `agent_execution_started=false` | Frozen Schema v1 + intake v1.1, **unchanged** | Current producer/consumer and all earlier v1 receipts remain accepted exactly as before |
| `EXISTING_IMMUTABLE_DISPATCH_REVALIDATION` (Canary009 only) | `executable_dispatch_published=true` verified from immutable control Git | A **separately governed compatible schema/contract candidate**; never shoehorn into v1 | No pre-Dispatch publication action. Preflight verifies the existing dispatch's immutable identity, *fresh* unconsumed/unstarted ledger and material host conditions. Only CHAT may later decide readiness |

**Not yet selected:** Future schema `$id`, schema_version, Dictionary registration, consumer routing and promotion version. Options: a new versioned receipt profile plus a separate exception-aware CHAT intake (preferred for preserving v1 semantics), or a formally controlled extension with explicitly proven old-consumer compatibility. Do not label either EFFECTIVE or mint a canonical version number in this candidate. No extra field may be silently inserted into a v1 `additionalProperties=false` receipt.

## 4. Truthful dispatch and observation semantics

The existing-published cohort MUST bind `dispatch_id`, `control_commit`, dispatch full SHA-256, prompt commit/hash, immutable Canary branch/head, Registry+frozen source-set and the Owner's location exception. It MUST record `executable_dispatch_published=true`.

A distinct fresh host observation must establish each of:
- `dispatch_consumed=false` with evidence of the exact `dispatch_id` in *all applicable durable per-user/legacy/manual-consumption stores*;
- `agent_execution_started=false` through the same provenance;
- no `RUNNING`, `CLAIMED`, `NEEDS_RECONCILIATION`, duplicate attempt, uncertain checkpoint, or conflicting record;
- observation timestamp, host identity, ledger source method, consistency/freshness evidence and time-bound status.

If consumed=true, started=true, source ambiguous, one store unreadable, or any required field **UNKNOWN**: **HOLD/STOP / NEEDS_RECONCILIATION**. A historical 21:46:06+07 snapshot on 2026-10-18 cannot serve as a current pre-claim attestation. A missing Git execution-result marker or a stable Git HEAD proves neither unconsumed nor unstarted. Do not trigger claim, poll, worker, status with side effects, Agent execution or Canary probe during this check.

A compatibility receipt may record truthful rejected/unknown states in the future extension's evidence model, but may yield **PASS/readiness eligibility only if both current consumed and started are conclusively false**. It must not fabricate a v1 `PASS` or falsely state executable dispatch unpublished. An existing executable Dispatch is neither republished nor replaced.

## 5. Separate identities: execution source vs publication source

**Task identity (immutable):** `task_branch=work/FOX2-BRIDGE-FINAL-CANARY-009`, `source_head=501822a33ef08c7365154913bbc677544856eee5`, exact dispatch and prompt identities above. Validate the frozen task/source bytes from that commit. These fields NEVER point at evidence-only branch.

**Publication locator (variable evidence branch):** `publication_branch=work/FOX2-BRIDGE-RC1-PREEXEC-EVIDENCE-20261018`, approved exact `receipt_path`, and `expected_publication_head` obtained by a new live authenticated read immediately before writing. Publication head may advance **once** for the single receipt commit, while the Canary execution HEAD remains identical. Bind the previously published location exception's immutable bytes as a sidecar. Avoid changing the legacy receipt's meaning of `source_head`.

**Writer separation:** Verify task worktree at locked HEAD with exclusive no-writer admission and clean state; verify a distinct, separately-owned evidence publication checkout/destination. Neither checkout may have unrelated WIP. Do not use the task worktree to push a receipt onto Canary. Never use a receipt publication commit as an Agent execution source commit. Verify both remote heads before action, and ensure only exact receipt path changes on evidence branch.

**No race/side effects:** Protect publication against head drift with an atomic expected-head/non-fast-forward guard, allowlisted single-file diff, secret scan, schema/contract validation, canonical UTF-8/LF, successful push then authenticated remote commit-and-byte readback; make no success claim before readback. Reject or reconcile drift rather than reset/stash/rebase/force-push. Confirm unchanged Canary head, dispatch bytes and prompt after receipt publication.

## 6. Contract migration and source authority

Schema v1, generated v1 binding and historic receipts MUST remain byte-for-byte. Existing pre-Dispatch consumers keep selecting v1 based on their *actual* workflow. The new cohort must be selected by explicit, authenticated **existing-dispatch identity and separately authorized contract profile** (not filename heuristics or task-branch substitution). Schema validation must be performed against the actual authorized profile, not bypassed.

The candidate compatibility semantic change needs **separate scoped Owner/Policy-source authorization** for the shared receipt schema/PreExec Protocol/intake and an implementation authorization for producer/consumer code, including PreExec for **that coding work** and worktree/writer ownership evidence. The previously approved location-only exception does not grant this. After an authorized implementation, run contract/test/consumer validation then publish a distinct source-bound candidate release/acceptance decision; install/runtime adoption and Canary Host PreExec are later, separately gated stages. No silent Dictionary/Registry or global Policy EFFECTIVE promotion.

## 7. Acceptance contract — minimum adversarial cases

1. Frozen v1 `PRE_DISPATCH` PASS, BLOCKED, INFRA_FAILED semantics and exact receipt bytes remain compatible; no existing v1 tests silently reinterpreted.
2. `EXISTING` with `published=true`, fresh `consumed=false/started=false`, exact hashes and approved publication locator may become a **candidate eligible** record only after every material check passes; never claim performed in this document.
3. A `published=true` record cannot validate as v1 with `published=false`; a failed validation must fail closed.
4. Wrong dispatch ID / dispatch digest / prompt digest / Canary task HEAD / Registry/source-set / Owner location approval → REJECT.
5. `consumed=true`, `started=true`, unknown, missing, stale or inconsistent ledger → HOLD/STOP; no readiness, claim, replay or replacement.
6. Publication branch cannot become `task_branch`; task HEAD cannot advance because the receipt was committed elsewhere.
7. Unknown writer, unrelated WIP, staged out-of-scope paths, remote drift, non-fast-forward, secret mismatch or failed remote byte readback → FAIL CLOSED and preserve evidence; no success marker.
8. No test invokes the real Canary dispatch, `e2e-once`, `run-next`, worker resume, actual claim or broker/provider/LIVE effects.
9. Legacy dispatch is already published, so old pre-dispatch intake fields requiring `executable_dispatch_published=false` must not be used to misstate this revalidation route.
10. Provenance for a frozen task branch vs a changing evidence-branch publication is verified independently and both remote heads rechecked.

**Verification status:** Normative schema conflict and observed producer coupling were confirmed against Git. These cases are **test requirements**, not claimed executed tests. A later coding task must run them on isolated fixtures/safe test remotes, not on the immutable Canary.

## 8. STOP and delivery semantics

`CANDIDATE_NOT_EFFECTIVE`; `CODE_ALLOWED=NO_UNDER_THIS_DOC_ASSIGNMENT`; `IMPLEMENTATION_PREEXEC=NOT_RUN`; `HOST_CANARY_PREEXEC=NOT_RUN`; `CANARY_CURRENT_CONSUMED=UNKNOWN_NOT_REOBSERVED`; `CANARY009_READY=NOT_GRANTED`. No merge, main, provider/broker writes, deployment, LIVE or Canary execution.
