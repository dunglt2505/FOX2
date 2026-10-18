# FOX2 — Independent Review Admission Contract v1 (CANDIDATE)

**Project:** FOX2 only
**Status:** `CANDIDATE_NOT_EFFECTIVE`
**Purpose:** A verifiable, feasible method to demonstrate independent reviewer eligibility before a mandatory independent release-readiness audit.
**Scope:** Proposed project-wide standard for future WORK/independent review contracts. For Bridge RC1 it is a proposed acceptance clarification only, **not an amendment of the frozen task or a waiver**.
**Owner/CHAT authority basis:** `docs/governance/releases/FOX2_OWNER_CHAT_FULL_DELEGATION_20261018.json` (prospective non-main governance documents, no repeat Owner approval for drafting/publication; EFFECTIVE and material release-gate changes still independently gated).
**Source:** Frozen Bridge RC1 Whole-WP `docs/agent_handoff/FOX2-BRIDGE-DESKTOP-BATCH-B/task.md`; Bridge source `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`; RC1 WP-only Registry `b27f1085ee13d8dce56fd2735e100ea1616e6e23`.
**No new privileges:** NO DEV/main/merge/LIVE/provider/broker write; NO Canary 009, APP-B resume, source rebind, or consumed Dispatch replay.

## 1. Why a contract is needed

The frozen Bridge task requires `PRECANARY_INDEPENDENT_AUDIT=PASS` and names **WORK** as the required independent reviewer. It does **not** exclusively require a host-issued cryptographic admission certificate or numerical model/quota telemetry.

Later handoff notes required proof of reviewer identity and genuine independence, correctly rejecting a same-session `CODEX_WORK_MODE_LINUX` reviewer. They also introduced a more specific “host-issued admission/provenance” proof method that the available host cannot provide. The substantive requirement (independent WORK review) must not be conflated with one particular proof mechanism, nor may CHAT declare the previous reviewer independent without evidence.

This contract proposes proof alternatives that protect the substantive requirement. It does **not** retroactively change any accepted or blocked result.

## 2. What “independent” means (all mandatory)

For a scoped Whole-WP, an independent reviewer:
1. Has verifiable authority to audit **that** Whole-WP and is the required WORK reviewer or another role only after a separately approved task-level role amendment.
2. Is not the implementation Agent, the same execution session as the implementer, or a reviewer who only reuses their own earlier non-admitted audit as independent certification.
3. Has no material conflict from writing, directing, or self-approving the product/evidence being certified; any contribution must be disclosed and evaluated before admission.
4. Can access immutable source/evidence and perform an actual review with review-specific observations, adverse-case checks, acceptance matrix, limitations, and a source-bound result.
5. Has reviewer identity/execution provenance **corroborated outside the reviewer's own prompt or self-authored report**. A Git principal of the Owner, a declared role, model name, new conversation, or source SHA alone does not prove reviewer independence.
6. Has read-only audit scope by default; any evidence publication requires separately verified non-main destination, file ownership, Git readback and source lock.
7. Retains ability to return `FAIL` or `BLOCKED` without pressure to force release.

A reviewer can be independent without needing a specific model tier; model, thinking and numeric quota are recorded only when visible and are not substitute identity credentials.

## 3. Candidate admission proof modes

### Mode A — Native host provenance (preferred if supported)
A trusted host/provider record (job/session/run/role or equivalent), bound to the actual reviewing execution, can support the reviewer identity, authorized role, execution separation and linkage to the audit result. CHAT checks that record against implementation/admission history and confirms no same-actor/same-session or material conflict. Host-origin alone is not enough if it does not prove the required role or independence.

### Mode B — Corroborated reviewer-of-record (proposed fallback; NOT YET APPROVED)
Where host-issued admission certificates are unavailable, an **externally verifiable**, separately identified reviewer-of-record may be admitted if and only if:
- The accountable Governance authority **prospectively approves this method** for the required role/task before its use; it does not retroactively convert the earlier Codex session into WORK.
- Evidence from a source independent of the reviewer's self-report establishes the reviewer's distinct authenticated identity or execution principal (for example separately verifiable reviewer account plus independent assignment record and audit/log trail). Owner assignment by itself, Owner's shared Git principal, and a fresh chat title are insufficient.
- Independent assignment source and review results link the same reviewer/principal to the exact task/source, with timestamps, allowed scope and reviewer conflicts disclosed.
- CHAT (as intake authority, not self-certifying auditor) independently verifies the evidence, confirms no overlap with the CODEX implementer and previous non-admitted reviewer, and records its grounds.
- The reviewer performs substantive read-only acceptance on the already frozen evidence; an external signer with no genuine review cannot turn an existing non-independent report into PASS.

**The frozen Bridge task pins WORK**. Mode B must still demonstrate an eligible WORK reviewer. Substitution by a human auditor, CHAT, COPILOT or CODEX requires an explicit, appropriately authorized task/acceptance change first, not this candidate contract.

If neither Mode A nor approved Mode B can substantiate independence, status is `BLOCKED`; do not manufacture signatures, session IDs, provider attestations or “equivalent” identity.

## 4. Minimum admission record and decision

Required fields: contract version/authority status, whole_wp, immutable Registry/manifest/source bindings, implementing actor/session evidence, reviewer role and observed principal/host/session (nullable if not exposed), independently sourced identity/authorization evidence references, proof mode, role separation and conflict analysis, live permissions/capacity observation, decision owner and decision evidence, read-only scope, creation UTC, and disposition.

Allowed dispositions:
- `ADMITTED`: required role/independence supported by externally corroborated evidence under an **effective approved** method.
- `BLOCKED`: missing platform evidence, no eligible reviewer, unapproved method, or lack of proof; no audit PASS.
- `REJECTED`: evidence proves self-review, forbidden conflict or other substantive ineligibility; no audit PASS.

`ADMITTED` does **not** imply `PRECANARY_INDEPENDENT_AUDIT=PASS`. The admitted reviewer must independently assess acceptance and deliver its own evidence-bound PASS/FAIL/BLOCKED report; CHAT performs separate intake.

The companion candidate JSON Schema is `docs/governance/FOX2_INDEPENDENT_AUDIT_RECEIPT_SCHEMA_v1_CANDIDATE.json`. Schema validation proves structure, **not** identity, authority, or an actual review.

## 5. Audit evidence reuse, freshness and source authority

- Use Registry -> Owner authorization -> release manifest -> immutable Git bytes/path/SHA-256. The existing RC1 WP-only binding remains Dictionary v1.2 / Policy v1.8.9 / Routing v1.3.0 / Protocol v12, and B2 resolver execution is `CLOSED_PASS`.
- Inherit accepted integrity checks and product regressions when still material and source unchanged; avoid repeated 34 checks, 399 JUnit tests, 30 Desktop tests and consumed Dispatches.
- Treat immutable Git evidence and `installed/current Windows host state` separately. Reviewer decides if one minimally scoped **read-only** host attestation is material; before any Canary claim CHAT must separately verify the actual current ledger/no-prior-claim and fresh PreExec. Git branch stability alone is not current ledger proof.
- Preserve the frozen 40-gate Bridge acceptance matrix; independent audit gate remains mandatory, Canary 009 remains HOLD pending audit PASS and CHAT release decision.
- Never reinterpret `CANDIDATE`, `GIT_PUBLISHED`, `CHAT_INTAKED` or `SOURCE_VERIFIED` as `EFFECTIVE`, `REVIEWER_ADMITTED` or `AUDIT_PASS`.

## 6. Required governance authorization before activation

This candidate is **only published for review**. Activation requires:
1. Governance-owning authority decides whether Mode A and/or Mode B is an allowed evidence mechanism, consistent with the frozen task's mandatory WORK role and non-negotiable independence.
2. A versioned, source-bound approval/manifest and explicit effective status through the actual trusted release chain (do not self-assert it).
3. Applicable impact assessment for the Bridge task/handoff and any changed acceptance wording, without altering immutable historical bytes.
4. A real eligible reviewer executes under the approved method and produces verifiable independent evidence.
5. CHAT independently intakes that result and separately decides `FOX2_BRIDGE_RC1_PRECANARY_READY` only if every applicable original gate is PASS.

Until these steps are proven: `ADMISSION_METHOD_B=NOT_APPROVED`, `WORK_REVIEWER_ADMISSION=BLOCKED`, `PRECANARY_INDEPENDENT_AUDIT=BLOCKED`, `CANARY_009=HOLD`.

## 7. Security and STOP

Never store credential secrets, bearer tokens, private session identifiers unnecessarily, or account passwords in receipts. Store provider-issued evidence references or redacted verification results, with immutable hashes where practical. Fail closed for absent independence proof, source conflict, unverifiable approval, or material test/host uncertainty. No prompt, Git commit or this draft may grant release or waive the mandatory audit gate.

**Suggested review owners:** CHAT drafts and checks source/contract consistency; Governance owning authority decides admissible evidence mechanism; independently eligible WORK executes actual audit only after admission; COPILOT/CODEX have no implementation work from this contract.
