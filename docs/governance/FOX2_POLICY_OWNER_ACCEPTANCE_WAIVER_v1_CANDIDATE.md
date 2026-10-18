# FOX2 — Policy Addendum v1: Owner Acceptance Waiver (PROSPECTIVE CANDIDATE)

**Project:** FOX2 only
**Status:** `OWNER_APPROVED_FOR_GOVERNED_POLICY_CHANGE / CANDIDATE_NOT_GLOBAL_EFFECTIVE`
**Date:** 2026-10-18
**Authority:** Explicit Owner direction in current CHAT conversation authorizing a future-policy Owner Acceptance Waiver mechanism.
**Owning source:** `docs/governance/FOX2_POLICY_V1.8.9.md` (EFFECTIVE under RC1 WP-only binding, SHA in its immutable source manifest).
**Related candidate:** `docs/governance/FOX2_POLICY_V1.9.0_CANDIDATE.md` (existing prospectively published draft; NOT_EFFECTIVE).
**This document:** A separate **proposed policy semantic addendum**; it does not rewrite released Policy v1.8.9, mutate the existing 1.9.0 Git/Library release receipt, create a competing effective Dictionary, or automatically change any in-flight WP.
**Only already approved WP exception:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` with its own source-bound Owner approval and acceptance addendum. No automatic waiver for other WPs.

## 1. Intent, authority and precedence

Owner is the ultimate project decision maker for internal acceptance checkpoints and may explicitly **waive an Owner-controlled internal review/test checkpoint** when the residual risk is bounded and accepted. The action is an **acceptance-contract change**, not a retroactive technical PASS, and must be documented against the exact work package and current governing requirements.

CHAT directly executes authorized documentation and verification; release authority, protected operations, source lock and real technical safety gates remain independently applicable. This Policy proposal must be promoted using the established trust/authority/compatibility lifecycle before use as a **projectwide EFFECTIVE** rule.

## 2. Standard waiver taxonomy

A release gate's prospective disposition can be:

- `PASS`: Required operation performed with verifiable acceptance evidence.
- `FAIL`: A proven material defect; not converted to PASS by waiver.
- `NOT_RUN` / `BLOCKED`: Factual historical result; never rewritten by an Owner waiver.
- `WAIVED_BY_OWNER`: Owner explicitly authorizes *not performing that checkpoint* for the named WP and names accepted assurance risk; only a separately source-bound accepted-exception overlay, not an executed test outcome.

The expression `GATE_SATISFIED_FOR_RELEASE` may include `WAIVED_BY_OWNER` **only** when a valid scope-bound Owner approval and release/publication provenance are present **and** the gate is permitted to be waived without removing material correctness/safety prerequisites. A status enum in isolation does not grant release.

## 3. Mandatory exception scope and receipt

Every future Owner Acceptance Waiver must record:

1. The exact Whole-WP, original immutable task/source/Registry/manifest references, affected acceptance gate IDs and original requirement.
2. Explicit Owner directive and what is waived; **no implied blanket authority or silent other-WP inheritance**.
3. Why the checkpoint is waived and the specific residual assurance risk Owner accepts, versus actual product faults Owner does not waive.
4. Required compensating controls, unchanged PASS conditions, prohibited actions and external/regulatory/third-party restrictions.
5. Effective scope/period and expiration/supersession condition, if relevant.
6. Candidate vs Owner-approved vs Git-published/readback vs acceptance-applied vs release status; **do not conflate these**.
7. Record owner, approval source, authorized path, immutable Git publication commit/blob/content digest and remote readback.
8. Impact/compatibility review of all known acceptance evaluators, scripts, dashboards, receipts, Routing/PreExec/consumer APIs that might assume `ALL_GATES_PASS` or reject `WAIVED_BY_OWNER`.

CHAT need not request repeated Owner approval for steps already covered by a specific bounded Owner directive. If a new WP, material scope expansion or an unapproved gate is implicated, obtain corresponding approval before applying any exception.

## 4. Waiverable vs non-waiverable conditions

The Owner may waive an **internal process or independent review step** when the acceptance risk is explicitly understood, evidence already shows no unresolved material correctness issue, and downstream controls remain intact.

Waiver **does not**:
- fabricate a test execution or transform historical `NOT_RUN/BLOCKED/FAIL` into `PASS`;
- authorize ignoring a **proven material product failure**, source integrity mismatch, secret/privacy incident, externally binding compliance/licensing restriction or unmitigated catastrophic/irreversible safety condition;
- replace exact source lock, accepted code-path compatibility, authenticated host capability, permissions, concurrency/writer separation, immutable dispatch/ledger state, single-use/no-replay, installed current state or required fresh PreExec;
- grant DEV, main/merge/deploy, production/LIVE, provider/broker write or funds-trading authority;
- retroactively change consumed Dispatch, past certification, or install a new code acceptance policy in a running worker.

Where the requested waiver would remove an operationally necessary guard or externally required constraint, classify `WAIVER_NOT_APPLICABLE` with a technical reason and escalate through the owning change-control process; do not silently call it an Owner-approved internal process waiver.

## 5. Work-package application procedure

```text
Owner explicit bounded waiver
 -> CHAT confirms exact WP, frozen authority and acceptance scope
 -> scope-specific versioned Owner approval and prospective WP addendum
 -> material impact and consumer compatibility assessment
 -> governed non-main publication + Git readback
 -> CHAT verifies applicable Owner exception at release-readiness intake
 -> separate fresh material host/ledger/PreExec and remaining safety checks
 -> explicit CHAT release-readiness decision (PASS / FAIL / HOLD)
```

Preserve original task and immutable evidence as historical records; publish a prospective addendum that supersedes *only the named condition*, never mass-edit historical files. Future WPs continue under their own original gates until their own explicit Owner approval.

A deterministic gate evaluator or JSON schema that accepts only `PASS` must be amended/tested by an **authorized separately routed engineering task** before consuming `WAIVED_BY_OWNER`; never fake `PASS` just to satisfy its existing enum. A human CHAT acceptance decision is valid only when it can trace the Owner approval, the source-bound exception and all applicable remaining gates, and when governing runtime/release policy permits that route.

## 6. Release and supersession of this global Policy proposal

This document is a **prospective semantic Policy candidate**. To make Owner Acceptance Waiver an EFFECTIVE projectwide mechanism, the release owner must incorporate it into the next governed Policy revision (taking account of existing Policy v1.9.0 candidate and its Dictionary v1.3, Routing v1.4, PreExec/Protocol source-compatibility chain), or publish an independently authorized effective Policy addendum through the same source-trust lifecycle.

Required before claiming global `EFFECTIVE`: exactly bound source family/manifest/Registry, owner authority, independent release-chain verification as required by the current Governance release contract, Git/Library parity where required, conflict-free supersession and consumer compatibility evidence. Existing prospective Governance v1.9.0 release has unclosed trusted release authority and installed Dictionary v1.3 runtime compatibility; this proposal does not bypass those gates.

**Current decision matrix:**
- `BRIDGE_RC1_OWNER_WAIVER=EXPLICITLY_APPROVED_IN_ITS_WP_ONLY_SCOPE`.
- `POLICY_OWNER_ACCEPTANCE_WAIVER_MECHANISM=OWNER_APPROVED_CANDIDATE`.
- `POLICY_GLOBAL_EFFECTIVE=NOT_CLAIMED`.
- `WAIVER_OTHER_WPS=NOT_AUTHORIZED`.
- `CANARY_009=HOLD_UNTIL_SEPARATE_VALID_READINESS_DECISION`.
