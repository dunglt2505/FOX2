# FOX2 — BRD Standard Template v1.0

**Document type:** Business Requirements Document (BRD) template for FOX2  
**Owner direction:** approved for project-wide future BRD authoring on 2026-10-23  
**Git adoption:** PR #31 / CANDIDATE on non-main branch; not yet integrated into main  
**Application:** every new BRD; material revisions to existing DRAFT/CANDIDATE BRDs; released BRDs only on a separately scoped substantive change  
**Usage guide:** [FOX2 BRD authoring & source index](../brd_mirror/README.md)  
**Principle:** BRD defines WHAT, WHY and acceptance; Technical Spec defines HOW.

> **Usage:** Copy from the FOX2-BRD-XX heading below to a real BRD. Replace bracketed fields and remove example rows before release. Use N/A with a reason if a section is inapplicable. Do not rewrite an already RELEASED_EFFECTIVE BRD just to change its structure, or renumber released requirement/test IDs. The template does not itself grant DEV, merge or LIVE authority.

---

# FOX2-BRD-XX — [Business capability / subsystem]

| Field | Value |
|---|---|
| Document ID | FOX2-BRD-XX |
| Version | [vX.Y / REVn] |
| Status | [DRAFT / CANDIDATE / RELEASED_EFFECTIVE / SUPERSEDED — grounded in authority] |
| Business Owner | [Role or Owner] |
| Last updated | [YYYY-MM-DD] |
| Milestone / scope | [M1-A / M1-B / Bridge / other] |
| Previous version | [Git path + immutable SHA / N/A] |
| Authority | [Governance Registry and Owner decision; UNKNOWN if unverified] |
| Technical counterpart | [Tech Spec + version/ref / TBD] |
| Data/API contracts | [Contracts + versions / N/A] |
| Acceptance source | [Matrix/test source + ref / TBD] |
| Git source | [Branch + commit SHA when published] |

## 1. Business context and desired outcome

**1.1 Problem / opportunity:** [Who faces what problem, when, and what evidence supports it?]

**1.2 Objective / value:** [Required FOX2 capability or user-visible value; not implementation design.]

**1.3 Success measure:** [Observable outcome/KPI and agreed target, or TBD if not agreed.]

**1.4 Requirement ownership:** [What this BRD owns, what another BRD/Tech Spec/Contract owns.]

## 2. Actors and user journeys

| Actor / consumer | Business goal and authorized scope | Main usage scenario |
|---|---|---|
| [Actor] | [Need and permission boundary] | [Event → expected result] |

**Journey:** [Start condition → business action → user/consumer-visible result.]

## 3. Scope and dependencies

**IN SCOPE**
- [Capability/behavior that must be delivered for this milestone.]

**OUT OF SCOPE**
- [Explicitly unsupported/deferred capabilities, forbidden actions.]

**Dependencies:** [Relevant BRDs, rights, sources, contracts, decisions; only actual prerequisites.]

**Assumptions and constraints:** [Platform, availability, rights, evidence level; distinguish assumptions from facts.]

## 4. Functional and business requirements

One stable ID per testable normative requirement; state actor/condition, required behavior and observable outcome. A new BRD can use FOX2-XX-R01, R02...; an existing BRD MUST keep its previously released IDs. P0/P1/P2 is priority, never acceptance status.

| Requirement ID | Priority | Actor / condition | Normative behavior (WHAT) | Observable outcome / rejection | Acceptance ID |
|---|---|---|---|---|---|
| FOX2-XX-R01 | P0 | [Actor / Given] | [When ..., system MUST ...] | [Then: unambiguous result] | FOX2-XX-T01 |
| FOX2-XX-R02 | P1 | [Actor / Given] | [Under ..., system MUST NOT ...] | [Explicit error/rejection state] | FOX2-XX-T02 |

Avoid vague statements such as fast, stable or secure without measurable criteria. Frameworks, source files, DB schema, API routes, command syntax and implementation algorithms belong to Technical Spec, not BRD.

## 5. Business flows and negative cases

**5.1 Main flow**
1. **Given:** [User, permission, prerequisites, valid input.]
2. **When:** [Business action or event.]
3. **Then:** [Expected output/state the user or consumer can observe.]

**5.2 Exception/recovery flow**
1. **Given:** [Unavailable, stale, conflict, timeout, offline, crash, quota, rejected rights — where relevant.]
2. **When:** [Attempt/interrupting event.]
3. **Then:** [Explicit, safe outcome; no invented success or fabricated data.]

**5.3 Edge cases:** [Limits, duplicates, concurrency, idempotency/no-replay where business-relevant; otherwise N/A.]

## 6. Business rules and data semantics

| Rule / data | Business meaning | Authoritative source | Missing/invalid/stale behavior | Requirement / AC |
|---|---|---|---|---|
| [Rule/state] | [Units, meaning, time basis] | [BRD, Dictionary or Data Contract] | [UNKNOWN/STALE/UNAVAILABLE/rejection] | [Rxx/Txx] |

**For market-data features:** identify provenance, data rights, units, calendar, event/as-of/first availability, freshness and source state; UNKNOWN is not zero; no fake investor data.

**For Agent/permission-sensitive features:** define owner permissions, allowed operations, one-writer/no-replay outcomes, uncertainty and secret protection; a BRD must not imply authorization to run DEV, merge, broker/provider writes or LIVE.

## 7. Non-functional requirements and constraints

Targets must be measurable, or explicitly marked TBD/N/A with a reason. Where needed, trace them to the same stable requirement IDs (no parallel mandatory numbering system).

| Category | Required measurable target or boundary | Verification method | Requirement / AC |
|---|---|---|---|
| Performance | [Target, workload/environment / TBD reason] | [Test/benchmark] | [Rxx/Txx] |
| Availability and recovery | [Offline/restart/stale expected result] | [Failure test] | [Rxx/Txx] |
| Security and privacy | [Authorization, redaction, secrets boundary] | [Negative/security test] | [Rxx/Txx] |
| UX/accessibility | [Supported viewport/navigation/status labeling] | [Review/test] | [Rxx/Txx] |
| Financial/operational safety | [Read-only/no order write/no LIVE when relevant] | [Rejected action test] | [Rxx/Txx] |

## 8. Acceptance criteria and traceability

Keep acceptance scenarios in this BRD OR point precisely to an existing authoritative Acceptance Matrix. Do not maintain two contradictory copies. Preserve released IDs and verified historical evidence.

| Acceptance ID | Requirement | Given / When | Then — exact expected outcome | Tech Spec / test | Status / evidence |
|---|---|---|---|---|---|
| FOX2-XX-T01 | FOX2-XX-R01 | [Setup and action] | [Observable, measurable PASS condition] | [Spec section / test ID] | NOT_RUN |
| FOX2-XX-T02 | FOX2-XX-R02 | [Negative case] | [Correctly rejected/error state] | [Spec section / test ID] | NOT_RUN |

**Traceability:** Requirement → Acceptance → Technical Spec/Contract → Test → Git commit/evidence. Mark absent mapping TBD/UNKNOWN. PASS/FAIL/BLOCKED/NOT_RUN require observed evidence; prompt publication, Agent statement, or PUSHED_UNREVIEWED is not CHAT acceptance.

## 9. Risks, dependencies and open decisions

| ID | Open question / impact | Responsible actor | Evidence needed to resolve | Status |
|---|---|---|---|---|
| O01 | [Unknown source/rights/contract/outcome] | [Role] | [Specific fact or decision] | OPEN |

Mark BLOCKED only for a real prerequisite preventing the next selected action. Deferred scope belongs in BACKLOG/OUT OF SCOPE, not an administrative micro-task.

## 10. Change history and release status

| Version / REV | Change type | Business behavior / acceptance change | Affected consumers | Publication/evidence |
|---|---|---|---|---|
| [vX.Y] | [EDITORIAL / STRUCTURAL / SEMANTIC] | [WHAT/AC delta or none] | [Relevant Tech Spec, Contract, tests, or N/A] | [Git SHA / Candidate] |

**Authority rule:** DRAFT/CANDIDATE is not RELEASED_EFFECTIVE. Effective source is resolved by authorized Owner decision and Registry/release evidence, NOT highest version number or Git publication alone. Do not rewrite frozen history, silently merge main, falsely attest machine adoption, or replay consumed Dispatch. On genuine business-semantic change, adjust only impacted Tech Spec/Contract/test consumers; editorial changes do not require version cascades.

---

### Quality checklist (not an additional approval gate)

- [ ] Problem, actors, desired outcome and IN/OUT scope are unambiguous.
- [ ] Every P0 requirement has a stable ID, testable behavior and acceptance mapping.
- [ ] Happy path and material failure/negative cases have observable outcomes.
- [ ] Data authority, UNKNOWN/STALE, rights and no-replay semantics are specified when applicable.
- [ ] NFR targets are measurable or transparently TBD/N/A with a reason.
- [ ] Traceability connects BRD/AC/Tech Spec/Test/evidence, or names the missing dependency.
- [ ] Revision preserves released IDs and unaffected evidence, with authority/status verified.

**Method note:** Adapted from clear, unambiguous, verifiable and traceable requirements principles used in ISO/IEC/IEEE 29148 and Given–When–Then scenarios; this FOX2 document does NOT claim formal ISO certification or complete standards conformance.
