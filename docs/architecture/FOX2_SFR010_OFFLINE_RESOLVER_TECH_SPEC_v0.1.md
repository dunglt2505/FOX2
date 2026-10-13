# FOX2 — SFR-010 Offline Source Release Resolver — Technical Specification v0.1

**Document ID:** `FOX2-SFR010-OFFLINE-TECH-001`  
**Project / WP:** FOX2 / SFR-010  
**Issue:** https://github.com/dunglt2505/FOX2/issues/11  
**Date:** 2026-10-13 (Asia/Ho_Chi_Minh)  
**Status:** `RELEASED_EFFECTIVE_FOR_SFR010_OFFLINE_DESIGN` after Library exact-byte publication, official manifest and Git mirror readback.  
**Owner decision:** “Chốt, triển khai đi” following explicit approval of two concurrent, independently owned implementation lanes. This source releases the **SFR-010 offline contract only**, not the wider SFR release hook, a DEV or Git-code-push grant, or a LIVE/Bridge launch.  
**Supersedes:** No earlier *released SFR-010 standalone* spec. Derived and scoped from `FOX2_SOURCE_FRESHNESS_REGISTRY_RESOLVER_SPEC_v0.1_CANDIDATE.md` (historical candidate, NOT promoted); excludes its SFR-020/030/040/050 runtime scope.  
**Normative current source:** FOX2 Policy V1.8.3 `RELEASED_EFFECTIVE` (Library raw SHA-256 `892a44f414c8deb3754782b0d1c9998a88fa1116da33e76048ac8756005dee82`); FOX2 Agent Prompt Routing Index V1.2.3 `EFFECTIVE_DERIVATIVE` (Library raw SHA-256 `f8d7ba05b5d35c269f939f6aa580517072d3e8734eee1e23f59cfb769aba2bbd`); Bridge Technical Spec v0.4 `RELEASED_EFFECTIVE` (only for future integration; no code in this WP). Latest applicable release head must be checked at *new handoff*, not hardcoded from this historical checkpoint.

## 1. Outcome, scope and hard boundaries

Build a **deterministic, offline, dependency-minimal** Python package that validates *provided* release evidence/manifest snapshots and computes a candidate SourceLock or a typed BLOCKED outcome. It does **not** autonomously read ChatGPT Library, publish a release, mutate a registry, invoke GitHub, create a dispatch or start an Agent. CHAT remains the live authoritative Library/Git resolver until SFR-020/030 integration is separately implemented and accepted.

The module must never treat a Git issue, moving branch, static bootstrap registry or highest filename as release authority. A `RELEASED_EFFECTIVE` string alone is not evidence: acceptance requires explicitly verified, attributable Library release + manifest evidence, complete relevant family enumeration, one unambiguous active head and a matching *immutable* Git mirror. Without these evidence fields, return BLOCKED/UNKNOWN, never fabricate `CURRENT_RELEASE_VERIFIED`.

No provider/DNSE/broker/network requests, background watcher, user-account credentials, SQLite DB, filesystem migrations or Bridge runtime edits. Gate A remains `BLOCKED_CAPABILITY_UNAVAILABLE` independent of SFR-010 test results.

## 2. Ownership and parallel boundary

**CODEX candidate:** independent `source_freshness/**` package subtree at FOX2 repo root, *including tests and JSON fixtures under that subtree*. Do not change `agent_bridge/**`, `backend/**`, root `tests/**`, root packaging files, `docs/**`, `.github/**`, governance or immutable received source mirrors. Prefer standard-library typed dataclasses and pure functions; if dependency changes are needed, STOP and return the requested path and reason to CHAT. All code paths here are proposals until the task-scoped Owner grant, exact worktree, model/quota and one-writer verification.

**COPILOT parallel lane:** only existing `agent_bridge/**` BRG-003 sanitized source import on its separately reserved branch/worktree after its own authorization and runtime gates. No cross-lane edits and no sharing a mutable worktree, test DB or local writer. CHAT later performs Git readback/acceptance and owns integration decisions. Two coding writers are a maximum design intent, not a claim two Agents have already started.

## 3. Typed input and boundary contracts

Use plain dataclasses/TypedDict/enums (or equivalent typed Python structures):

- `ResolverRequest`: `project_id` exactly FOX2, `task_id`, `applicable_family_ids`, requested phase, optional previous immutable lock, trusted evaluation timestamp. Reject absent/unsupported project, family, or ambiguous scope.
- `ReleaseEvidence`: `family_id`, `scope`, `release_id`, version text (display only), exact `status`, `supersedes` ID(s), `owner_decision_ref`, `library_file_id/path`, `library_raw_sha256`, `library_size_bytes`, `manifest_path/sha256`, `publication_receipt_ref`, `library_enumeration_exhaustive`, validated-receipt status and provenance.
- `GitMirrorEvidence`: repository `dunglt2505/FOX2` (as fixture input), 40-char immutable commit, path, Git blob ID, raw-file sha256, size, verification status from an independent readback. An unresolved Git mirror is `GIT_SOURCE_PENDING`, not PASS.
- `FamilyEvidenceSet`: all relevant releases supplied by authorized CHAT source resolver; enumerable completeness flag, query scope, observation identity/time and per-record receipt-verification. A static JSON fixture is always SIMULATED/TEST_ONLY unless a separately trusted adapter proves source provenance.
- `ResolverOutcome`: `SOURCE_FRESHNESS_PASS` only for sufficiently verified externally supplied evidence; otherwise one of `BLOCKED_SOURCE_VERSION`, `SOURCE_PENDING`, `SOURCE_AUTHORITY_UNKNOWN`, `AMBIGUOUS_ACTIVE_HEAD`, `SOURCE_HASH_MISMATCH`, `STALE_FOR_NEW_EXECUTION` with precise sanitized reason codes. **Never** place DEV/CODE_ALLOWED/merge/live permissions in ResolverOutcome.
- `SourceLock`: serializable immutable selection list for each applicable family (Library release/ref/raw SHA, manifest ref/SHA, Git immutable commit:path/blob/raw SHA, scope/relevance, resolved_at, verifying receipt ID) and source-set fingerprint; decision authority remains CHAT, not this Python module.

Methods: `validate_release_evidence`, `resolve_family_head`, `resolve_source_lock`, `compare_source_lock`, `canonical_source_lock_digest`. All deterministic, no hidden I/O. Use exact byte SHA-256 and canonical JSON serialization (`sort_keys`, stable separators, UTF-8) for testable digests; if supplied Library/Git contents exist in a test fixture, check raw bytes rather than transformed Markdown, and independently test Git blob as `sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw)` for small offline fixtures. Do not hash ambiguous newline-normalized text and claim parity.

## 4. Resolution order and safety semantics

1. Validate trusted input/provenance, exact project and family/scope. A source snapshot not individually attested by CHAT or real authorized publisher is test input, not authoritative production evidence.
2. Require full pagination/exhaustive enumeration for each relevant family; `next_cursor` non-null or missing required family -> `SOURCE_AUTHORITY_UNKNOWN` / STOP. Do not infer from folder name, semver sorting, modification date or Git branch history.
3. Eligible release records must be `RELEASED_EFFECTIVE`, valid owner-scope + manifest + attributable publication proof. Ignore Candidate as a *head candidate* while retaining history. Reject unverifiable entries or contradictory release receipts.
4. Construct the explicit supersession graph using immutable release IDs. Select exactly one applicable unsuperseded released head. If zero, ambiguous competing heads, cycles, dangling relevant supersession or an unproven revocation -> safe typed BLOCKED outcome. A higher version label does not win automatically.
5. Verify head's exact Library raw byte hash and manifest evidence against trusted verification facts. Independently require verified Git immutable commit:path and raw SHA/size/blob parity. Missing mirror -> `SOURCE_PENDING`, mismatch -> `SOURCE_HASH_MISMATCH`; no executable PASS.
6. Resolve all families atomically as a *pure value*. A single blocked family blocks the complete executable SourceLock; partial diagnostics are allowed but cannot be presented as full PASS. Produce deterministic canonical lock and fingerprint only when all material inputs succeed.
7. `compare_source_lock` compares old lock to a *newly attested* family-head set. A changed material release on an unexecuted task yields `STALE_FOR_NEW_EXECUTION`; never silently mutate old task or reroute automatically. Previously accepted historical task receipts remain immutable.
8. No source-lock result is an authorization for material code, Git push, merge, Bridge dispatch, Broker or LIVE. Unit evidence proves only offline resolver behavior.

## 5. Offline acceptance tests and evidence

Target at least these isolated tests; annotate what is pure fixture simulation versus actual remote authority verification:

| Case | Fixture/action | Required behavior |
|---|---|---|
| `SFR010-01` | Explicit verified Policy V1.8.3 vs older V1.8.2 with confirmed supersession | Select current V1.8.3 in fixtures; **no live Library claim** |
| `SFR010-02` | Higher-version Candidate 1.8.4 exists | Ignore Candidate for active head |
| `SFR010-03` | Older lock / newer accepted head | `STALE_FOR_NEW_EXECUTION` |
| `SFR010-04` | Released head with missing Git mirror | `SOURCE_PENDING` |
| `SFR010-05` | byte/raw SHA or Git blob mismatch | Reject, report no secret bytes |
| `SFR010-06` | Incomplete pagination / missing family | `SOURCE_AUTHORITY_UNKNOWN` |
| `SFR010-07` | Competing released family heads or graph cycle | `AMBIGUOUS_ACTIVE_HEAD` / blocked |
| `SFR010-08` | Authorized revoke/rollback lacking active replacement | BLOCKED with historical receipt retained |
| `SFR010-09` | Identical reproducible input in arbitrary ordering | Same head/SourceLock digest |
| `SFR010-10` | Original accepted historical WP retained | Historical lock immutable; no forced rework |
| `SFR010-11` | Partial family PASS plus one blocked family | Whole executable SourceLock fails closed |
| `SFR010-12` | Token strings/raw private account fields in fixture | Never present in error/result/log; no provider access |
| `SFR010-13` | Fake direct GitHub-only receipt without Library authority | `SOURCE_AUTHORITY_UNKNOWN` |
| `SFR010-14` | Candidate registry JSON claims current Policy v1.8.2 while Library-attested v1.8.3 exists | Registry snapshot cannot override newly attested release |

Unit tests may reuse `SFR-T01/02/03/04/05/09/10/12/13/14` as simulated algorithmic sub-evidence. `SFR-T06/07` CAS/webhook idempotency, `SFR-T08/11/15/16/17/18` live Library, Bridge trust and event constraints remain NOT_RUN unless separately tested. A test name referring to live Library is not evidence of a live connector.

**Acceptance receipt required:** source-lock identifier, exact branch/HEAD, allowed diff and file list, actual Python/test toolchain/model if observable, test command, pass/fail/skip count, fixtures and hash results, network-free proof method, CODE_ALLOWED status, remote full commit SHA/tree/blob readback (done by CHAT), and remaining open integration gates. No passing test summary without logs/evidence on the task branch.

## 6. Release boundaries and future integration

- `SFR-020`: protected publisher hook and idempotent release-CAS registry receipt; requires actual ChatGPT Library API/connector event access. NOT an offline Resolver requirement.
- `SFR-030`: CHAT new-task resolver orchestration, source-lock/stale-gate integration; separate source authority and receipt controls.
- `SFR-040`: Bridge RuntimeAttestor adapter, can begin only after BRG-003 remote source baseline/ownership and relevant Gate A controls, no duplicate CHAT governance evaluations.
- `SFR-050`: full negative/cross-agent/concurrency/crash E2E tests; no automatic enforcement PASS from SFR-010 fixtures.
- `FOX2-M1-P2-01`: separate application source/writer, may prepare docs in parallel now; coding held until Owner's priority acceptance checkpoints and task-specific DEV gate.

**Hard STOP:** newer actual released Policy/Tech/Contract source, task scope drift, missing authorization, unverified actual coding host/quota/writer, dirty or conflicted worktree, hash/secret mismatch, path outside this module, tests failing with no in-scope repair, inability to safely push/report. Never modify or destroy accepted work to force completion.
