# FOX2 Bridge RC1 — Independent Reviewer Admission Handoff Addendum (CANDIDATE)

**Status:** `CANDIDATE_NOT_EFFECTIVE / BRIDGE_AUDIT_BLOCKED`
**Owner-facing WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
**Date:** 2026-10-18
**Applies to:** Prospective clarification of the reviewer-admission evidence method only, conditional on Governance approval.
**Historical handoff:** `docs/roadmap/FOX2_BRIDGE_RC1_PRECANARY_WORK_AUDIT_HANDOFF_20261018.md` at CHAT commit `38a6e2d265cfca1f14305c11b535800a5494f873`.
**Frozen Bridge task and source:** `docs/agent_handoff/FOX2-BRIDGE-DESKTOP-BATCH-B/task.md` at `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`.
**Candidate contract:** `docs/governance/FOX2_INDEPENDENT_REVIEW_ADMISSION_CONTRACT_v1_CANDIDATE.md`.
**Candidate receipt schema:** `docs/governance/FOX2_INDEPENDENT_AUDIT_RECEIPT_SCHEMA_v1_CANDIDATE.json`.

## 1. CHAT finding — separate the requirement from the proof mechanism

**Binding requirement is unchanged:** The frozen task section 11 names WORK as required independent pre-Canary auditor; section 7 requires `PRECANARY_INDEPENDENT_AUDIT=PASS` before any `FOX2_BRIDGE_RC1_PRECANARY_READY` marker and before Canary 009 claim.

The frozen task does NOT exclusively require a host-issued reviewer certificate, a cryptographic signature or exposed numeric model/quota metrics. A later CHAT handoff requested real independent identity/admission provenance and used host-issued proof as an approach. That request is not a standalone new source of authority to alter the frozen gate.

Actual reviewer evidence currently comes from a `CODEX_WORK_MODE_LINUX` session continuing the initial bounded audit, source resolver recovery and later assessment. Those same-session self-reviewed receipts cannot prove independent WORK admission. Not having a host-issued certificate is a **proof-mechanism limitation**, but it is not permission to waive actual independence.

## 2. Current immutable evidence to reuse — no retesting by default

| Record | Immutable Git evidence | Fact |
|---|---|---|
| Bridge implementation | `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9` | 38 technical gates PASS; 1 non-gating icon disposition; independent audit gate remains pending |
| Initial bounded audit | `d48aea2e22449ee4435cd81cb89101b653e7dbc8` | 34/34 checks, 26/26 Dispatch 004 digests, 67/67 historical digests, 252/252 ZIP hashes, source-binding evidence PASS |
| Resolver recovery | `980335cae53904f4cc0b06ae5b3a6ba59516ae90` | B2 CLOSED_PASS: authentic FOX2 Skills resolver, 10/10 effective WP source families, 24 Git reads, exit 0 |
| Final admission determination | `541bf35e3bdb95b701bd1cdc22b0bdbe87333110` | B1 BLOCKED: same unadmitted reviewer execution, no independent WORK admission; no product FAIL |
| CHAT intake | `38a6e2d265cfca1f14305c11b535800a5494f873` | Result reviewed; B1 BLOCKED; Canary 009 and APP-B HOLD |

Reused technical tests: Python JUnit 399 PASS, Desktop 30 PASS historical; no fresh installed Windows runtime/ledger observation is claimed by the audit session. This addendum requires no rerun.

## 3. Candidate clarification for the next truly independent reviewer

Until the proposed admission contract is authorized: `WORK_REVIEWER_ADMISSION=BLOCKED`.

Following valid prospective Governance approval only:
- Prefer **Mode A**, platform-native externally corroborated WORK execution/role provenance.
- Consider **Mode B** only when authorized for this exact task: separately authenticated, independently assigned reviewer-of-record with objective non-self-authored proof of reviewer identity and execution separation. It must still be an eligible WORK auditor under the frozen task, unless a separate authorized task role amendment is published.
- In neither mode may a new chat title, role string, Owner's shared Git identity, Codex output or an unverified signature stand in for substantive independence.
- CHAT verifies admission sources but does **not** self-perform/sign the required independent audit; qualified reviewer actually reviews the frozen technical evidence and issues a fresh source-bound conclusion.
- The reviewer evaluates whether an extra minimal *read-only* Windows host/ledger attestation is genuinely material for audit sufficiency. The future Canary claim independently requires fresh host ledger and PreExec before execution.

**Admission is separate from certification:** `ADMITTED != INDEPENDENT_AUDIT_PASS != PRECANARY_READY`.

## 4. Governance and release STOP

This addendum and the companion contract/schema are published as *candidate documentation*, not a new effective Policy, not a replacement Registry and not a frozen Whole-WP task edit. It grants no new host authority, model, runtime, code, release, merge or LIVE rights.

Do NOT:
- rewrite frozen Bridge task or source lock;
- turn the existing audit's BLOCKED into PASS;
- rerun or replace Dispatch 001–004;
- execute Canary 009 or create Canary 010;
- resume APP-B or promote the Governance v1.3/v1.9.0 candidate;
- change Owner-level acceptance semantics without authorized source-bound approval.

Required next decision: the Governance-owning authority confirms whether the candidate evidence contract is an acceptable method consistent with the task's mandatory WORK role. If not, record exactly why and retain B1=BLOCKED. If the host cannot supply a genuine eligible independent reviewer under an approved method, the Owner must make a separately governed task-level decision; this candidate does not waive the audit requirement.

## 5. Routing / assignment

- **R0:** Audit evidence already completed, no code replay.
- **R1:** Reviewer eligibility / admission contract; no new implementation task.
- **R2:** Authority = prospective CHAT documentation only; EFFECTIVE/readiness not proven.
- **R3:** Current WORK host independent identity/quota and Windows host access remain UNKNOWN.
- **R4:** CHAT authors candidate directly; COPILOT/CODEX are not substitute independent auditors; WORK is *not admitted* yet.
- **R5:** Only CHAT-owned non-main Governance docs; no Bridge/Canary/APP worktree modification.
- **R6:** Candidate files need Git remote exact-byte readback and future source-bound approval; preserve legacy receipts.
- **R7:** STOP before assigned WORK audit execution, PRECANARY_READY, Canary, APP-B or EFFECTIVE.

**Final recorded status:** `B2=CLOSED_PASS / B1=BLOCKED / PRECANARY_INDEPENDENT_AUDIT=BLOCKED / CANDIDATE_ADMISSION_METHOD_NOT_ACTIVE`.
