# Trading — New Project Source Authority & Agent Handoff Starter Kit v1.0

**ID:** TSG-NEW-PROJECT-SOURCE-KIT-001 · **Date:** 2026-10-13 · **Status:** REUSABLE_REFERENCE / OPT_IN_ONLY / NOT_A_RELEASED_POLICY / NOT_AN_IMPLEMENTED_SERVICE.

**Purpose:** For a future new project, bootstrap versioned Policy/BRD/Technical publication, Active Source Registry, Release Resolver, SOURCE_LOCK and Agent Handoff Gate **without repeating stale-policy/stale-spec mistakes**. This kit does **not** apply itself to FOX, FOX2, Silkworm, Mantis or any other project; Owner/project admission and verified release are mandatory. Existing project-specific or actually effective law/provider restrictions take precedence. It is a reference template, not an unrestricted cross-project governance or Git sync request.

**Related files:** `00_EXISTING_CONTROLS_AND_GAPS.md`, `02_PROJECT_SOURCE_PROFILE_TEMPLATE.yaml`, `03_ACTIVE_SOURCE_REGISTRY_SCHEMA_v1.0.json`, `04_AGENT_SOURCE_LOCK_HANDOFF_TEMPLATE.yaml`, `05_SOURCE_FRESHNESS_ACCEPTANCE_MATRIX_v1.0.md`.

## I. Rules to carry into a project

1. **Project isolation:** Every new project declares PROJECT_ID, owner, canonical Library root, optional authorized Git repository, source families, data/secret exclusions and effective local policy. Other projects' docs are **READ_ONLY REFERENCE** unless explicitly adopted by a new Owner-approved release. Never inherit CODE_ALLOWED, trading authority, releases, broker/LIVE access or Git writer rights.
2. **Latest applicable released source:** Determine family `active` using actual Library publication, status (`RELEASED_EFFECTIVE` or explicitly project-defined approved status), Owner-scope/supersession, exact raw-byte SHA-256 and authoritative release manifest. **Not** highest version string, latest timestamp, Git commit or existing prompt.
3. **Registry is an index, not authority:** It caches checked release identity. Must record independent Library and Git evidence, resolver generation and freshness timestamp. An index never publishes a Candidate and never grants authority. Treat cached head as stale until checked against upstream on **each new handoff**.
4. **Release and mirror are distinct:** A Library release requires its own byte readback and publication receipt. Git is an optional execution mirror when the task needs Git. If no exact eligible mirror, use `SOURCE_PENDING` for Git-first executable tasks; unrelated planning can continue.
5. **Handoff gate:** A prompt for a new task contains an immutable `SOURCE_LOCK` for Policy + task-applicable BRD/Contracts + Technical + grants, linked to manifest, raw hashes and Git commit:path/blob (where applicable). A checksum-valid *old* release is `BLOCKED_SOURCE_VERSION`, not PASS.
6. **Execution gate:** Agent verifies actual checkout/HEAD/worktree, appropriate pinned source and task authority; Broker/Production/LIVE, code push, report push, PR, merge are independent grants. SOURCE_FRESHNESS_PASS alone never implies DEV.
7. **Fail closed:** Any incomplete paginated inventory, release-identity ambiguity, mismatched blob, untrusted publication, missing required manifest, stale lock, conflicting project identity, missing capability or unrelated WIP returns a typed blocker; no silent downgrade or self-selection of an older SHA.
8. **Auditable reuse:** Preserve prior released bytes, receipts, branch history, previous task source locks and acceptance. New releases affect new or materially impacted pending tasks, **not automatically accepted history**.

## II. Bootstrap procedure for a brand-new project

| Step | Owner/CHAT activity | Artifact & mandatory evidence | May proceed when |
|---|---|---|---|
| B0 | Start source inventory, choose Owner/project and applicable external obligations; record PROJECT_ID | A project identity decision; source/policy applicability register | No unknown project collision |
| B1 | Fill `02_PROJECT_SOURCE_PROFILE_TEMPLATE.yaml` (no live credentials) | Project profile incl Library folders and Git namespace; explicit statuses | Owner approves initial governance scope |
| B2 | Release inaugural Policy/BRD/Technical (separate families) in **project-owned** Library paths | Raw bytes + SHA256 + Owner decision + release manifest + readback | Effectivity independently evidenced; Template by itself is not release |
| B3 | Mirror only required/authorized release bytes to project's exact approved Git destination | Git commit:path SHA, blob and raw byte digest, source-sync receipt | Source bytes match, proper writer; Git data-rights checked |
| B4 | Initialize materialized Active Source Registry from verified release receipts, not from directory names | Schema v1 validated registry snapshot + generation/head + parent receipts | All advertised CURRENT heads have upstream proof |
| B5 | Provision supported Library reader or authorized Publisher event integration; add reconciliation | Durable idempotent event receipts/CAS/retry; compare to live upstream | Realtime automation claimed only if installed/tested |
| B6 | Wire Handoff Resolver to the CHAT router before new prompt and before executable dispatch | Typed SOURCE_LOCK + latest-effective freshness decision + task permission receipt | No stale/conflict, no WIP and task gate satisfied |
| B7 | Verify actual Agent checkout, scoped Git permissions and independent negative tests | Source lock, checkout proof, positive/negative test results, review decision | All gates measured; not based on model claims |
| B8 | Freeze a project-specific `PROJECT_SOURCE_GOVERNANCE_RELEASE_RECEIPT` | Owner-approved release, version, adoption scope and implementation evidence | Only this step makes the *project-specific* adoption effective |

A first-run chicken-and-egg case uses **PREPARE_CHECKOUT / READ_ONLY** with exact Owner permission and no material DEV. Do not manufacture `PUBLISHED_FOR_AGENT` or `CODE_ALLOWED=YES` just to bootstrap source.

## III. Target architecture

```text
Authorized Owner / Library Publisher
  -> Library release -> raw byte readback -> immutable release manifest/receipt
  -> Git exact mirror (if authorized; asynchronous SOURCE_PENDING is possible)
  -> Release Event Queue (auth + idempotency, only when available)
  -> Registry Builder CAS generation; keep all immutable history
  -> Active Source Registry [NON-AUTHORITATIVE MATERIALIZED VIEW]
  -> On every new task: CHAT Release Resolver re-queries authoritative family heads
  -> SOURCE_LOCK + immutable task authorization receipt + handoff prompt
  -> On dispatch: CHAT revalidates current source; Bridge attests exact runtime receipt
  -> Agent actual checkout source/hash/HEAD preflight
  -> result/push evidence -> independent CHAT acceptance (never automatic merge)
```

**Fallback:** If supported Library event delivery/read access is absent, CHAT performs the latest-effective Library resolve at each new handoff and records `MANUAL_SOURCE_FRESHNESS_VERIFIED`. Never call this `AUTO_POLICY_VERSION_ENFORCEMENT=PASS`. A Git-only webhook cannot certify unseen Library changes.

## IV. Minimal project contract (instantiated from templates)

- Registry `project_id`, `schema_version`, `generation`, `verified_at`, `authority_class=NON_AUTHORITATIVE_INDEX`, `heads[]`. For each head, `family_id`, `scope`, `version`, `release_id`, `state`, `library` (stable identity, raw SHA256, size, verified receipt), `manifest` (raw SHA256), `git` (immutable commit:path/blob/raw SHA256 or SOURCE_PENDING) and `supersedes`.
- Resolver input: `PROJECT_ID`, `TASK_ID`, relevant family IDs + BRD applicability, requested execution phase, source-lock generation and Owner approval/grant reference. Resolver must verify exhaustive Library pagination/authorized publisher and explicit supersession order. Two unreconciled active heads block.
- Resolver output: `VERIFIED_CURRENT`, `SOURCE_PENDING`, `BLOCKED_SOURCE_VERSION`, `DIVERGED`, `AMBIGUOUS_ACTIVE_HEAD`, `SOURCE_ACCESS_UNKNOWN` with evidence; failure **not** coerced to default version. Include `resolved_at` and the *actual method* used.
- Handoff input: **immutable resolved source lock**, plus separate task-specific approval, code path allowlist, actor/host/writer/quota, test plan and STOP conditions. Do not allow task packet to self-issue permissions by an asserted boolean.
- Release trigger: authenticated append-only receipt with generation CAS, dedup `release_id`, no reordering; reconciler compares event state with Library, protects against crash between Library release and Git mirror. If platform provides no event feed, alternative pull/schedule is best effort **not** atomic release capture.

## V. Security, tenancy and source ownership

- One Registry **namespace per project**. The same implementation can be cloned; its data and credentials cannot be shared implicitly.
- No private keys/tokens, account details, raw licensed vendor feeds or user machine paths in shared templates/registry. Secret scanning and rights checks before Git mirror and before any result push.
- Writer leases for exact worktree/path/branch. A branch named `work/...` does not itself prove server-side ACL; private/personal repos can lack effective ref rules. Allowlist of paths at application layer is defense-in-depth, not verified GitHub enforcement.
- Distinguish `REPORT_WRITE/PUSH` vs `CODE_ALLOWED/GIT_CODE_PUSH` vs `MERGE` vs `PRODUCTION/LIVE`. Standing report permissions cannot import code or review their own results.
- Registry/Resolver **never** changes project effective Policy or initiates checkout, merge, migration, refactor or order placement.
- Freeze past accepted WPs. A current-release change invalidates **new and materially impacted unexecuted** handoffs; notify CHAT to re-route changed scope, not trigger recursive automatic rework.

## VI. Adoption and release gates

- **Reference available** means only Library/Git bytes stored and independently read back.
- **Project adopted** only after project-specific Owner scope, issued effective policy/technical contract, exact release manifest, Git mirrored when applicable, and verified local permission. No opt-in inferred from copying these files.
- **Automation implemented** only after actual Library reader/Publisher integration, Registry Resolver and handoff/dispatch enforcement are deployed, with all required negative tests green and independent safety review when applicable.
- **Unattended dispatch** is a separate gated capability and may remain BLOCKED even if latest-source resolution works perfectly.

**Failure examples:** `BLOCKED_SOURCE_VERSION/NEWER_RELEASE`, `SOURCE_PENDING/GIT_MIRROR_MISSING`, `SOURCE_ACCESS_UNKNOWN/LIBRARY_UNAVAILABLE`, `DIVERGED/RAW_HASH_MISMATCH`, `AMBIGUOUS_ACTIVE_HEAD`, `WRITER_COLLISION`, `UNVERIFIED_OWNER_RECEIPT`. An error/UNKNOWN is never an implicit permission or a reason to downgrade.

## VII. Future project handoff checklist (copy into project kickoff)

- [ ] Project ID, Owner, authority tree and applicable external restrictions verified.
- [ ] All required Library families and previous releases enumerated to final cursor; no Candidate promoted.
- [ ] Inaugural issued policy + manifest + exact-byte readback established.
- [ ] Authorized Git mirror source/branch/worktree (if necessary) verified remotely.
- [ ] Registry schema and bootstrap records validated and marked non-authoritative.
- [ ] Library event/read capability known: IMPLEMENTED or MANUAL/UNKNOWN, never guessed.
- [ ] `SOURCE_LOCK` generated for actual task with fresh Library family-head verification.
- [ ] Separate Owner task approval and CODE_ALLOWED/report/push/merge gates recorded.
- [ ] Stale-valid-SHA and concurrent-release negative cases PASS before auto execution claim.
- [ ] Independent reviewer/release evidence exists where required by effective policy.
- [ ] History, archived candidates and previous accepted WPs preserved.
- [ ] Project-specific adoption receipt issued; no cross-project global enable switch.

**Route:** For any future project's actual deployment, redo R0–R7 against its real policy/host/quota/Git ownership. CHAT drafts and source-checks first; Copilot/CodeX/WORK eligibility is measured, not inherited from another project's tools or allocations.
