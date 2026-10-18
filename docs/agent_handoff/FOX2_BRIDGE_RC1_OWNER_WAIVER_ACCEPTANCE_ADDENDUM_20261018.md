# FOX2 — Bridge RC1 Owner-Approved Acceptance Addendum (Independent Audit Waiver)

**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
**Status:** `OWNER_APPROVED_RC1_ONLY / SOURCE_BOUND_ADDENDUM / NO_CANARY_PERMISSION`
**Owner directive:** Explicitly approved 2026-10-18 in current CHAT conversation.
**Owner approval receipt:** `docs/governance/releases/FOX2_OWNER_BRIDGE_RC1_PRECANARY_AUDIT_WAIVER_APPROVAL_20261018.json` (first immutable publication commit `451aaaf617cc2c9b7e4a9f8f6503e75bbc8e95a1`, Git blob `a39c92cb385f36c9eaa12d34e4299c885ae649e4`).
**Scope:** RC1 pre-Canary acceptance only. This document is a prospective Owner-directed *material change to acceptance semantics*, **not** a rewrite of the already consumed implementation Dispatch or historical frozen task.

## 1. Precedence, authority and frozen source

The Owner authorizes the following one-time exception to the RC1 task section 7 requirement `PRECANARY_INDEPENDENT_AUDIT=PASS` and to the related mandatory WORK step in task section 11, **for this Whole-WP only**. Owner approval is an acceptance-waiver decision, **not** a claim that an independent review occurred or passed.

Frozen implementation task: `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9:docs/agent_handoff/FOX2-BRIDGE-DESKTOP-BATCH-B/task.md`.
Frozen acceptance matrix: `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9:reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_final_closure_004/acceptance_gates.json`.
WP-only trusted Registry: `b27f1085ee13d8dce56fd2735e100ea1616e6e23:docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json`.
Immutable technical source-set: `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`.
Bound runtime sources remain Dictionary v1.2, Policy v1.8.9, Routing v1.3.0, Git-first Protocol v12.

The frozen task, historic acceptance JSON, installed product bytes and immutable evidence remain byte-for-byte unchanged. This Owner approval is a *scoped acceptance overlay* for the next RC1 pre-Canary decision; it does not rebind historical Dispatches or promote projectwide Governance candidates.

## 2. Single acceptance exception

| Gate | Original task condition | Owner-approved prospective disposition |
| --- | --- | --- |
| `PRECANARY_INDEPENDENT_AUDIT` | `PASS` required | `WAIVED_BY_OWNER` — accepted internal review assurance risk; **NOT PASS** |

The earlier reviewer result `PRECANARY_INDEPENDENT_AUDIT=BLOCKED` remains factually correct about the attempted review. The implementation-era JSON still says `PENDING`; neither is overwritten.

For a **future** RC1 pre-Canary acceptance decision, apply the following gate *expression*, and no broader one:

```text
RC1_PRECANARY_ELIGIBLE =
  (EVERY_APPLICABLE_ORIGINAL_TECHNICAL_GATE == PASS)
  AND (SOURCE_LOCK_AND_REQUIRED_EVIDENCE == VERIFIED)
  AND (PRECANARY_INDEPENDENT_AUDIT == WAIVED_BY_OWNER
       AND OWNER_WAIVER_SCOPE == FOX2-BRIDGE-RC1-TO-INTERNAL-READY
       AND OWNER_DIRECTIVE_RECORD_AND_GIT_READBACK == VERIFIED)
  AND (CURRENT_HOST_AND_CANARY_PREFLIGHT_REQUIRED_FOR_CLAIM == PASS)
  AND (NO_MATERIAL_UNRESOLVED_PRODUCT_FAILURE)
  AND (CHAT_PRECANARY_READINESS_DECISION == APPROVED)
```

The non-gating `ICON_DISPOSITION=ICON_NON_GATING_NO_AUTHORIZED_ASSET` remains non-gating. **Do not** feed `WAIVED_BY_OWNER` into a validator that only accepts `PASS` without an approved explicit exception-aware acceptance route; report that evaluator mismatch and STOP the affected transition rather than falsify the historical matrix. A focused compatibility check is needed before an automated gate consumer uses this new disposition.

## 3. Technical and Canary safety requirements still mandatory

- Preserve and independently validate source hashes, changed-path allowlist, diff/secret scan, package/installed evidence and relevant technical PASS claims. Reuse 34/34 earlier bounded checks, B2 10/10 resolver, 252/252 payload hashes, 399 JUnit and 30 Desktop historical PASS, subject to source-materiality review.
- Before authorizing Canary, collect **fresh read-only** Windows installed-package/source-pointer verification and **current control-store execution ledger**; Git branch stability is not a claim that Canary 009 has never run.
- Validate exact intended Canary ID `FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`, preserved head `501822a33ef08c7365154913bbc677544856eee5`, `max_runs=1`, unconsumed status, current PreExec/Agent/permissions/worktree and no-replay admission. Do not issue a new Canary or change its immutable prompt/tuple.
- Future Canary execution remains **HOLD until a separate evidence-backed CHAT readiness marker is issued**, then only via the governing execution host, exactly once.
- Only after successful Canary, restart/no-replay validation and CHAT intake may `INTERNAL_FOX2_BRIDGE_READY` be considered. APP-B waits for that milestone.

No DEV/source rewrite, main/merge/deploy, provider/broker writes or LIVE authority is granted.

## 4. Owner risk acceptance and evidence distinction

Owner accepts the *incremental assurance risk from absence of a separate independent WORK audit*, not unknown or adverse product correctness evidence. Prior `CODEX_WORK_MODE_LINUX` results remain bounded/non-independent and cannot be labeled WORK PASS. An actual material finding remains material regardless of this waiver.

The Owner's appointment authority and choice of waiver require **no further reviewer admission bureaucracy**. No new review host, host-issued certificate or separate WORK report is needed for this waived **RC1 checkpoint**. No other WP is covered.

This approval does **not** waive release-chain authority for a future projectwide Policy, nor make any candidate Policy EFFECTIVE. The separate future Policy mechanism is drafted as `docs/governance/FOX2_POLICY_OWNER_ACCEPTANCE_WAIVER_v1_CANDIDATE.md`.

## 5. Source-bound publication and required CHAT next step

The Owner instruction and JSON approval must be published under the authorized non-main Governance branch and remote byte-read back. This document is the prospective approved owner exception scoped above. A separate release publication record must connect this document's **immutable Git commit/blob** to the frozen WP and verify bytes before an acceptance evaluator may consume the overlay.

**Current publication does not equal `FOX2_BRIDGE_RC1_PRECANARY_READY`.** CHAT next reconciles technical PASS, evaluator compatibility, current Windows ledger and fresh Canary PreExec in a bounded read-only gate check; it does **not** launch Canary as part of publication.

**Owner-directed STOP:** No admission investigation or repeated WORK/CODEX prompt; no gate PASS fabrication; no historical source overwrite; no automatic policy promotion; no Canary/APP-B/merge/LIVE.
