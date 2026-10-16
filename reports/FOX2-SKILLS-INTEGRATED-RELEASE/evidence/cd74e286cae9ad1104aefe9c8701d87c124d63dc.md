# FOX2 — Active Source Registry, Release Trigger & Handoff Resolver — v0.1 Candidate

**Document ID:** `FOX2-SOURCE-FRESHNESS-TECH-001`  
**Change ID:** `FOX2-SFR-P0-20261013`  
**Scope:** FOX2 only · P0 documentation/technical design · `DESIGN_ONLY / NOT_RELEASED / NO_DEV_GRANT`  
**Owner direction:** Implement dependable, automatically refreshed use of the latest *actually released* FOX2 Policy, BRD and Technical Specifications on each new Agent handoff. Do not rely on static version text in the Agent Prompt Routing Index.  
**Authority:** Owner decision → FOX2 Policy V1.8.2 (RELEASED_EFFECTIVE) → relevant released BRD/Data Contract/Acceptance → Bridge Technical Spec v0.4 (RELEASED_EFFECTIVE) → Agent Prompt Routing Index V1.2.2 (effective derivative). This Candidate does **not** amend any of those source authorities.

## 1. Current evidence, no duplicate work

- Active Policy: V1.8.2, Library raw SHA-256 `552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc`; mirrored Git object at `c9dc41b97ca8bc58f06cc2f3701832ba083422e3:docs/governance/FOX2_POLICY_V1.8.2.md` (blob `0783c024d19f96a0b87ab770dad80bab449fa21f`).
- Bridge Technical Spec: v0.4 RELEASED_EFFECTIVE, Library SHA-256 `8a7d5e55239c07fb32834f856fbe59b33cbc90d92768a7804c9a70236907cd9e`; Git `36e4249d10d82e258626e3e49d796d8a8f498b8d:docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4.md` (blob `e74402d294c713a07a08b2c4e68b6caafbe2ad48`).
- Agent Prompt Routing Index: V1.2.2 EFFECTIVE DERIVATIVE; already requires `SOURCE_FRESHNESS_PRECHECK`, `SOURCE_LOCK`, and `BLOCKED_SOURCE_VERSION` for new WPs, but it is an instruction, not an installed resolver. Do **not** version-bump Policy just to repeat the same rule.
- GitHub Issue #10 tracks Bridge work. Existing BRG-001/002 evidence and BRG-003 source-import readiness are retained. Existing local Bridge runtime source remains not Git-versioned/independently tested; no installed release-trigger/Library-reader is proven.
- `AUTOMATED_GATE_A=BLOCKED_CAPABILITY_UNAVAILABLE`; publisher identity/branch enforcement unavailable/unverified. Source freshness **does not unlock Agent dispatch**.

## 2. Required architecture and trust boundaries

```text
Owner/CHAT publishes RELEASED_EFFECTIVE document
   │ must have Library exact-byte readback + release manifest
   ▼
Release Receipt / Publication Hook (authorized source)
   │ idempotent, append-only, no unconditional Git-authority promotion
   ▼
Source Registry Builder (candidate record, optimistic CAS)
   │ verifies effectivity/supersession & matching Git immutable mirror
   ▼
Active Source Registry (materialized index; NOT a new authority)
   │ periodically and on request reconcile against live authoritative Library
   ├─────────► CHAT Handoff Resolver [MANDATORY SOURCE_FRESHNESS_PRECHECK]
   │                  │ latest Library release + hashes + Git + grants
   │                  ▼
   │              Immutable SOURCE_LOCK in task/prompt
   │                  │ compare again before *actual executable* dispatch
   ▼                  ▼
Read-only status      Bridge RuntimeAttestor: exact lock/receipt only
                                │
                                ▼
                Agent launch remains BLOCKED until Gate A/DEV gates pass
```

**Authority rule:** Library published release + manifest + attributable Owner decision are authority. Registry JSON, Git issue comments, branch names, timestamps and version strings are only indexes/evidence. **A registry entry never promotes a Candidate and never grants Git code write, merge, production, broker or LIVE.**

## 3. Data contract (`registry.schema_version=1`)

For each document family and applicable scope, store:

- `family_id`, `project_id=FOX2`, `applies_to`/requirement scope, `release_id`, exact `version`, `status=RELEASED_EFFECTIVE` and `supersedes` pointer;
- `owner_decision_ref`, immutable `library_file_id` (when available), `library_path`, `library_raw_sha256`, `release_manifest_path`, `release_manifest_sha256`, verified `publication_receipt_ref`;
- independent `git_repo`, `git_full_commit_sha`, `git_path`, `git_blob_sha`, `git_raw_sha256` or `GIT_SOURCE_PENDING`; immutable source mirror and receipt must agree at byte level;
- `verified_at`, `verified_by`, `verification_method`, `library_listing_exhaustive`, and evidence IDs;
- `state`: `CANDIDATE_INDEX` | `VERIFIED_CURRENT` | `SOURCE_PENDING` | `DIVERGED` | `REVOKED` | `SUPERSEDED` | `UNKNOWN`.

Never put credentials, raw client data, personally identifying paths, secrets or private feeds in registry. Keep prior releases for provenance; never overwrite released historical receipts.

**Bootstrap artifact:** `docs/agent_handoff/SOURCE_FRESHNESS/FOX2_ACTIVE_SOURCE_REGISTRY_BOOTSTRAP_20261013.json` is a **non-authoritative source snapshot**; it is **NOT** a live mutable Registry, NOT an automated release receipt and NOT a substitute for querying the Library at handoff. Do not claim `AUTO_POLICY_VERSION_ENFORCEMENT=PASS` from this document.

## 4. Resolution algorithm

1. Input: exact project FOX2, new task/WP ID, BRD applicability, Agent role, intended phase/permissions, current timestamp, optional immutable frozen scope receipt.
2. Enumerate **all relevant Library release records with complete pagination** for Policy family and each applicable BRD/Contract/Technical family. Reject incomplete result sets. Only explicit `RELEASED_EFFECTIVE` with valid Owner-scope and byte-verified Library artifact+manifest may compete for `active`.
3. Determine family head by explicit publication/supersession evidence (not lexical version or latest file modification time). If multiple competing effective heads, return `BLOCKED_SOURCE_VERSION / AMBIGUOUS_ACTIVE_HEAD`; do not pick arbitrarily. A newer Candidate is irrelevant to active selection.
4. Independently fetch exact Git `full_commit:path` for the chosen release and verify blob AND raw-byte digest against Library. If Git mirror is pending, set `GIT_SOURCE_PENDING`; block executable Git-first dispatch while allowing planning-only CHAT work as permitted by Policy.
5. Check materiality of any source update for a previously created but not yet executed WP. Mark its prepared prompt `STALE_FOR_NEW_EXECUTION` pending CHAT re-route; preserve accepted historical tasks with their original source locks. Do not auto-rewrite old dispatches.
6. Emit signed/attributable *decision provenance* from CHAT only, with immutable `SOURCE_LOCK` including all chosen families, validated receipts, scope, generation/revision, update sequence, and `resolved_at`. Enforce current routing policy R0–R7; never self-issue DEV.
7. At handoff, compare freshly queried authoritative head(s) to source lock and stop on mismatch; do not trust a cached `active` pointer alone. Before an **executable** local dispatch, CHAT revalidates changed head(s) and Gate A; Bridge validates exact locked source/runtime but **must not repeat or override CHAT's governance decisions**.
8. Report `SOURCE_FRESHNESS=PASS|BLOCKED_SOURCE_VERSION|SOURCE_PENDING|UNKNOWN` separately from `CODE_ALLOWED`, `HOST_GIT_PERMISSION`, `MODEL_QUOTA`, `AUTOMATED_GATE_A`, `RESULT_PUSH_VERIFIED`, `MERGE` and `LIVE`.

## 5. Publication update / release trigger

- **Preferred:** authorized Library Publisher invokes `publish → readback → manifest → Git exact mirror/readback → CAS registry update → release receipt`. This is a controlled publication **pipeline** once platform permissions and trigger integration are verified.
- **Fallback until automation is actually installed:** CHAT triggers the same resolver manually at every new handoff, querying authoritative Library records each time; a scheduled digest or GitHub-only webhook is **not sufficient** to claim atomic latest-policy enforcement.
- A GitHub webhook alone cannot see protected Library publication, therefore cannot certify newest Policy without a Library-connected reader and authenticated release receipt.
- Concurrency: compare-and-swap registry `generation`/previous head, use immutable receipt ID for deduplication; reject stale writer or out-of-order events. Crash between Library and Git mirror yields `SOURCE_PENDING`, not a valid new executable source lock.
- Rollback/revocation: require attributable explicit Owner release/supersession action; append receipt (do not delete history), re-resolve impacted *pending* WPs; accepted old WP evidence stays immutable.
- Future registry service credential must have minimum necessary read scope. No token/path ACL assumed: current private personal repo's branch restrictions remain unproven.

## 6. Local runtime and security requirements

- Use Bridge's existing `C:\Projects\FOX2-AgentBridge` and `C:\Projects\FOX2-worktrees` constraints; avoid duplicate poller/ledger implementation. Before implementation inspect actual code baseline, worktree/writer and host quotas.
- Registry Builder/Resolver must not parse, modify or checkpoint `bridge.db` as part of a *read-only* host inspection: SQLite read-only mode previously created WAL/SHM sidecars. Avoid side-effectful probes.
- No automatic Agent start, failover, model substitution, code checkpoint, PR, merge, release or LIVE. The standing Bridge output grant on `work/FOX2-REVIEW-EVENTS-bridge` authorizes **review-event metadata** only, not Registry/Policy publication or source-code push. CHAT-owned control and review branches remain CHAT-owned.
- Unknown Library service API auth/event subscription, Bridge host identity/credential, Git writer, Copilot/Codex quota or GitHub path enforcement must stay `UNKNOWN`, not guessed or bypassed.

## 7. Work packages and gates

| WP | Deliverable | Execution readiness / gate |
|---|---|---|
| `SFR-001` | Host/source/Library-capability inspection, code ownership and design freeze | READ_ONLY manual preflight; Copilot eligible if real host access; never re-run BRG-001/002 |
| `SFR-010` | Typed resolver + manifest verification + local fixtures | Separate scoped DEV/Git code grant, pinned source, one isolated writer |
| `SFR-020` | Authorized Publisher release hook + idempotent Registry CAS and audit receipt | Evidence of Library connector/trigger & service credentials; no self-promotion |
| `SFR-030` | Handoff resolver / `SOURCE_LOCK` binding and stale-prompt blocker | Source parity; CHAT authority and manual fallback preserved |
| `SFR-040` | Bridge attestation integration (lock verification only) | BRG baseline + Gate A before automated dispatch; no duplicate governance decision |
| `SFR-050` | Independent E2E negative, race/crash/release-order tests and acceptance | All required gates independently observed; no blanket PASS from unit tests |

Execution order: `SFR-001 → SFR-010 → SFR-020/030 → SFR-040 → SFR-050`, with Gate A handling a separate blocker; no automatic source-code permission follows from creating this specification.

## 8. Acceptance matrix (design-only, not executed)

| ID | Scenario | Expected result |
|---|---|---|
| SFR-T01 | Policy V1.8.3 valid Library release & Git readback | New WP binds V1.8.3 without editing V1.2.2 text |
| SFR-T02 | V1.8.4 Candidate only | V1.8.3 stays active |
| SFR-T03 | Current old SHA validates but newer release exists | `BLOCKED_SOURCE_VERSION`, never silent old-source use |
| SFR-T04 | Library release exists; Git mirror not synced | `SOURCE_PENDING`; no executable dispatch |
| SFR-T05 | Manifest digest mismatches Library bytes | `BLOCKED_SOURCE_VERSION` |
| SFR-T06 | Two concurrent releases/CAS race | Exactly one active ordered head; loser retries reconciliation safely |
| SFR-T07 | Duplicate webhook/publication event | Idempotent; no double receipt or task |
| SFR-T08 | Library API down/no read access | No false `LATEST_VERIFIED`; pause new executable handoff |
| SFR-T09 | Listing paginated, next_cursor non-null | Exhaust pages or fail closed |
| SFR-T10 | Candidate greater version than Released | Candidate never promoted |
| SFR-T11 | Source changes between prompt and dispatch | CHAT source revalidation/STOP; no Agent silent rebind |
| SFR-T12 | Old completed WP source-pinned | Retain acceptance/history without rework |
| SFR-T13 | Multiple conflicting active family heads | `AMBIGUOUS_ACTIVE_HEAD` fail closed |
| SFR-T14 | Owner revoke/release rollback | Append explicit event, preserve history and revalidate pending WPs |
| SFR-T15 | Bridge trust Gate A still blocked | Source resolver passing cannot launch automatic Agent |
| SFR-T16 | Event branch standing grant used to publish Policy Registry | Deny: unauthorized authority/path expansion |
| SFR-T17 | Release trigger only gets GitHub event but no Library proof | `SOURCE_AUTHORITY_UNKNOWN`; no automatic head promotion |
| SFR-T18 | Report-only Copilot standing grant exists | Does not authorize `CODE_ALLOWED`/`GIT_CODE_PUSH` |

All `SFR-T01..18 = NOT_RUN`. Unit fixtures can demonstrate algorithm behavior only; full LIVE ENFORCEMENT requires real Library-event/publisher and handoff/Bridge acceptance. `AUTO_POLICY_VERSION_ENFORCEMENT` remains `NOT_IMPLEMENTED/NOT_VERIFIED` until E2E.

## 9. Required release/readiness evidence

Before marking any implementation phase DONE: exact pinned source set, task/grant, independent Git source blob readback, host/Agent/Writer lease, quota/mode observation (or UNKNOWN & blocked executable), tests+negative evidence, event/receipt idempotency, actual Library release resolution, proof of stale-prompt block, Review receipt; no path to main/merge/LIVE. WORK may audit high-risk concurrency/trust delta independently when suitably routed. `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `MERGE=NO`, `LIVE=NO` for this document production only.
