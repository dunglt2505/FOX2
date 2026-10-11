# FOX2 — POLICY V1.0 | CONSOLIDATED GOVERNANCE

**Document ID:** `FOX2-POLICY-V1`  
**Version:** `1.0.0`  
**Applicability:** `FOX2 ONLY`  
**Release date:** 2026-10-11 (Asia/Ho_Chi_Minh)  
**Document authority:** FOX2 Owner; CHAT acts as delegated Library document operator.  
**Status:** `RELEASED_EFFECTIVE` for FOX2 **internal document governance only**, conditional on the completed, read-back Library publication and linked release manifest.  
**Release verification:** See separate FOX2 V1.0 release manifest for the actual provider file ID, bytes, SHA-256, operation and receipt. The text alone is not evidence that a write occurred.  
**Exclusions:** This publication grants no DEV, Git push/merge, broker orders, provider credentials, deployment or LIVE status.

> **ONE FOX2 POLICY FAMILY.** Sections A (Governance), B (BRD), and C (Agent Routing) form one authoritative FOX2-only policy. Any separate drafts or preparatory documents are non-binding unless expressly adopted by a subsequently published FOX2 Owner decision.

> **SCOPE BOUNDARY.** FOX2 is an independent new project. Other-project documents, release rules and implementation approvals do **not** apply automatically, by similarity of names or folder location. Owner has the highest internal FOX2 decision authority including technical delegation, while applicable law, third-party rights and actual system access remain factual execution boundaries. Cross-project migration/synchronization is not authorized by this release.

## 0. Executive decisions captured from the 2026-10-11 FOX2 discussion

1. Establish this FOX2-specific Policy V1 with no inherited project governance or cross-project release dependencies.
2. Use separate, explicit names for **BRD governance** and **Agent prompt/routing governance**, with the Governance Core as the authority and safety layer.
3. **One canonical approved BRD revision** owns the business requirement. Break its authorized implementation into *Work Packages* (WPs) for Agents, **not** into rival master BRDs.
4. When Owner approves a named BRD, record its exact revision/BCC/scope. Owner may act as Publisher or delegate CHAT/another actor with **actual** Library write access; verify published bytes by readback. A private-Git mirror is a separate later step required for technical handoff only when that handoff uses Git; it does not veto document adoption.
5. If Owner approves BRD **and asks to implement**, do not request approval again for the same unchanged decision. Owner has ultimate internal authority to approve scoped technical work and delegate DEV/Git responsibility; an actual executable grant still requires specified scope, real target access, source state and exclusive writer verification. Publication alone does not mean code already ran.
6. Before material Agent prompts, CHAT performs `POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK`. Actual handoff cites immutable Library and Git source identities and requires receiver readback.
7. **Routing target:** COPILOT ~**70%**, CODEX ~**30%** of *accepted eligible material implementation WPs*. This supersedes the previously discussed 80/20 direction. Routing is based first on risk, capability, actual quota/access and total cost of safe acceptance; 70/30 is a flexible planning metric, **not a mandatory work split or a grant**.
8. Copilot is initially considered for Windows/IDE/Git source checks, frontend, dashboard, routine APIs/backend, offline fixtures and ordinary tests. Codex is initially considered for domain core, nontrivial backend/data invariants, quantitative/risk algorithms, concurrency and difficult integration. CHAT owns decomposition and routing; independent reviewer involvement is risk-based or expressly Owner-directed, and cannot create an unapproved blanket veto. Agent assignments are never automatic based only on labels.
9. Protect concurrent development with **one writer per exact file/worktree target**, verified non-overlapping paths, separate worktrees and branches, frozen shared API contract, own unit tests and Owner-approved scoped integration.
10. Keep **FOX2 localhost V0.1 offline/read-only** as first permitted *design target*, not an authorized build: synthetic fixtures must be labeled; no broker/order-write, margin, unattended trading, unrestricted data access, external secrets or LIVE by implication.
11. Preserve **C2A — Model, Thinking & Token/Credit Optimization**: verify actual product/model/mode/quota, use minimum sufficient reasoning, reuse relevant evidence, control context and retries, and optimize cost per safely accepted outcome. The 70/30 ratio is a target, not a forced gate.

---

# A. FOX2 GOVERNANCE CORE — `FOX2-GOVERNANCE-CORE-V1`

## A1. FOX2-only scope, source precedence and supreme Owner authority

- **FOX2 is a NEW, independent project.** Its requirements, policies, permissions, folders, releases, worktrees and acceptance processes are established and governed within FOX2 only. No document, approval, release receipt, Publisher, Source Lock or worktree from another project is inherited by default.
- **No cross-project policy import.** Other-project documents are reference material only; they acquire no FOX2 governance force through shared names, storage location, historical drafts or implicit references. An actually effective external legal, contractual or platform obligation is evaluated only when its issuer and applicability to FOX2 are evidenced. This clause never purports to disable binding law or real platform permissions.
- **OWNER SUPREMACY — FOX2 internal authority:** Owner is FOX2's highest decision-maker for business, Policy, BRD, budgeting, security posture, document publication, technical architecture, choice/assignment/removal of Agents, and delegation or withdrawal of technical roles and Git/DEV/release responsibilities. An earlier or subordinate **internal FOX2 procedure** must not impose a veto over an explicit, attributable, scope-bound Owner decision. Owner may establish the inaugural FOX2 Publisher role and modify/replace any FOX2-internal review workflow, subject to the bounded real-world exception below.
- **Operational boundary:** Owner's authority to approve or delegate is not proof that CHAT (or any Agent) possesses unavailable host credentials, cloud ACLs, protected keys, platform entitlements or third-party access rights. A technical step is `COMPLETED` only after real operation + objective evidence. Legal requirements, licensed/provider terms, external protected service policies and material safety invariants cannot be bypassed by editing an internal document. If a claimed superseding external control applies, identify its exact authority and FOX2-specific scope; absent proof, do not invent a veto.
- **Conflict precedence inside FOX2:** (1) mandatory applicable external law/provider/platform access restriction; (2) latest exact, attributable FOX2 Owner decision; (3) actually published FOX2-only governance; (4) FOX2 BRD/technical procedures in their delegated areas; (5) design drafts and general reference material. Preservation and audit of past decisions do not constitute an active restriction.
- **Scope isolation:** No cross-project synchronization, migration, archive, deletion, supersession or file changes follow from a FOX2 policy update. Any separately paused workflow remains paused until independently and explicitly reauthorized.

## A2. Invariants (mandatory within the released scope)

| ID | Control |
|---|---|
| `FOX2-INV-01` | Owner is the highest authority for FOX2 internal governance and technical delegation. Record the exact attributable decision and scope; do not claim credentials or completed operations merely from approval. |
| `FOX2-INV-02` | Owner decision, source content, host permission, publisher operation, Git commit, test result and deployment are distinct evidence classes; none may be fabricated. |
| `FOX2-INV-03` | Scope permissions and one-writer controls to observed FOX2 project/actor/task/host/paths; unknown actual technical access blocks only the affected technical action, not Owner policy-making. |
| `FOX2-INV-04` | Owner may delegate decisions across business and technical roles; real Library write, DEV edit, merge/push, provider access, deployment and LIVE require separately observed completion/permissions for the action claimed. |
| `FOX2-INV-05` | Protect existing tracked/untracked/ignored WIP and Git history; never silently reset, rebase, stash, delete, archive or force-push. |
| `FOX2-INV-06` | Financial data provenance, time correctness and risk safety are explicit; no default broker/order-write, margin, credentials or LIVE. |
| `FOX2-INV-07` | `UNKNOWN`, `NOT_RUN`, `CANDIDATE`, `DEFER`, `BLOCKED` and `PENDING` are not PASS. Keep authorization, observed write, readback and effectivity status accurately separated. |

## A3. FOX2 roles and Owner-controlled delegation

**Owner — SUPREME internal authority:** Sole final authority to create/replace FOX2 Policy, approve BRDs, decide risk acceptance, designate a Publisher, delegate technical rights/roles, accept or decline discretionary reviews, and approve scoped Git/DEV/integration/release steps. Owner may revoke or narrow a delegation. Reuse unchanged recorded decisions; no duplicate approval loops. A newer material policy revision receives a distinct immutable identity, even when prepared under an existing Owner instruction.

**CHAT — delegated coordinator and document Publisher when technically possible:** Under Owner's explicit FOX2 instruction, CHAT may author/revise policy, maintain a record of Owner decisions, upload documents to an actually writable Library directory, verify content/readback and write a transparent publication record. CHAT's ability to write a file is established only by a successful tool operation, not by a self-declared `protected_issuer` title. CHAT must not invent independent signatures, third-party approvals or host access.

**Technical executor / Git mirror writer / Integrator:** Owner-selected eligible actor with observed access and exact writable source/worktree boundaries. For irreversible changes, require operation-specific scope and affected-WIP safeguards; a document Publisher is not automatically a Git writer.

**COPILOT / CODEX:** Candidate implementers, selected after verified actual model/mode, quota, host, Git/worktree and task scope. Each supplies own test evidence; no rights from another project carry over.

**WORK / independent reviewer / other eligible reviewer:** Optional for discretionary document review when Owner elects; required only for specifically identified non-waivable external obligation or high-risk domain release with an approved project-specific safety requirement. Never invent a review PASS or impose a discretionary review that Owner has explicitly waived.

## A4. Capability / risk tiers

| Tier | Intended work | Essential gate | Forbidden by default |
|---|---|---|---|
| `L0 POLICY/DOC` | FOX2 Policy/BRD design, Owner decision recording, new-library bootstrap and file readback | Owner scope, actual destination write permissions, exact hash/manifest and explicit publication record | Claiming unperformed technical permissions/independent signatures, broker/LIVE |
| `L1 OFFLINE DEV` | Isolated localhost fixture-backed FastAPI/React development and tests | Explicit Owner-approved bounded task, source pin, actual Git/host access, one writer and evidence plan | LIVE, secrets, broker order-write, implicit push/merge |
| `L2 SENSITIVE` | Licensed live/read-only data, private accounts, cloud/provider/broker-adjacent work | Separate Owner/domain/risk decisions, external rights, actual measured controls and scoped grants | Any operation not explicitly granted; especially order-write/margin/LIVE |

No tier automatically unlocks the next; authenticated effects must be established at the actual host boundary, not inferred from prompt wording.

## A5. FOX2 product/data operating boundaries

- **First design milestone M1:** localhost web (React/TypeScript/Vite) + offline fixture API (Python/FastAPI) displaying market, sector and stock information and source/quality states. M0 foundation BRD-00..08 remains **Candidate** until individually verified and released.
- Core investment analysis: observable price, volume and turnover, evidence-based money flow, sector/market cycles, comparable peer and own-history valuation, capital/risk/profit protection. Observed turnover must not be labeled a measured net buyer/seller flow without valid fields.
- Each data value must preserve provider/instrument/venue, event/as-of/received timestamps as applicable, VN session/timezone, units/price basis, source revision, provenance, availability, freshness and provisional state. `UNKNOWN ≠ 0`; `SYNTHETIC` data remain synthetic even when timestamped recently.
- Research/backtests: no lookahead, repaint in accepted outputs, survival bias as unacknowledged evidence, or unvalidated promotion to investor recommendations. Model tests, out-of-sample and independent domain acceptance must be separately evidenced.
- DNSE or another market-data integration requires separate legal/access/provider approval and freshness failure tests. Read-only data access does not enable BUY/SELL/CANCEL, broker credentials, margin or automated execution. Keep secrets outside source code, fixtures, frontends and logs.

## A6. Locations, inventory and file handling

**FOX2 document path convention; existence and writer access must be verified for each operation:**

```text
/Trading_Candidates/FOX2/<CHANGE_ID>/       # Candidate authoring
/Trading/FOX2/00_Governance/                # Protected released Policy only
/Trading/FOX2/01_BRD/                       # Protected released BRDs only
/Trading/FOX2/02_Architecture/              # Released architecture
/Trading/FOX2/03_Data_Contracts/            # Released data contracts
/Trading/FOX2/05_Acceptance/                # Released acceptance records
/Trading_Archive/FOX2/                      # Controlled separate later operation
C:\Projects\FOX2                            # Proposed isolated local workspace, not asserted to exist as Git
```

- Use provider IDs, original revision, location, source family/scope, byte size, raw hash, sensitivity, licensing, release status and trusted receipt when available.
- Reconcile **smallest verifiably complete affected dependency closure** on routine change, including unbound common Governance dependencies. For an initial source inventory or unproven migration, enumerate pagination to exhaustion; one result page is not proof of completeness.
- Never transfer unrelated files merely because a folder exists. Archive/delete/migration require independent scope, referrer safety, retention, collision plan, verified readback and explicit authorization; no retention rule from another project is imported.

## A7. FOX2 inaugural Policy publication — Owner-first bootstrap

**A7.0 — FOX2-only inaugural release.** For FOX2's first internal Policy V1, Owner establishes the document Publisher and delegates CHAT to carry out the actual Library operation **using permissions the tools really grant**. No earlier project's reviewer, Publisher, external issuer, Git repository or BRD mirror is a prerequisite merely through historical association. Independent review or protected signing requires a separately evidenced, actually applicable higher obligation; Owner has declined an additional discretionary audit for this L0 document bootstrap.

**A7.1 — Minimal auditable release procedure:**

1. **Freeze release source:** Record exact `FOX2-POLICY-V1`, version, scope `FOX2 ONLY`, source file ID, byte length, raw SHA-256 and revision lineage; preserve preceding drafts separately.
2. **Owner decision:** Preserve the attributable Owner instruction to create/revise/publish FOX2 governance and delegate CHAT; record the exact digest/version being issued. Approval of one source hash is not approval of an unrecorded replacement.
3. **Actual Publisher action:** Owner is publication decision-maker. CHAT is document operator if the current Library session has upload rights. Attempt a new file at `/Trading/FOX2/00_Governance/FOX2_POLICY_V1.0.md` or a versioned equivalent; do not replace another observed effective file silently. No external protected key is assumed to exist.
4. **Readback:** List destination, read exact uploaded source and independently compare file ID, raw bytes/SHA-256, project scope and intended label. Record observed date/time and actual operator; no backdated/imaginary issuance.
5. **Evidence:** Create an Owner-decision-linked publication manifest containing actual output ID/path/hash and status. If upload or readback fails: `PUBLICATION_INCOMPLETE`, never `EFFECTIVE`. If a real external controlled issuance gate is demonstrated, stop only that affected issuance and record the named authority/evidence.
6. **Effective classification:** Only after steps 1–5 truly complete, record `FOX2_DOCUMENT_POLICY_PUBLISHED` and `RELEASED_EFFECTIVE(scope=FOX2, internal_document_governance_only)`. This label does **not** assert a protected signature, Git sync, DEV, broker, margin or LIVE. Review any future changes against the latest actually published FOX2 version.

**A7.2 — Separation of business rights from observable capability:** An Owner's superior decision can remove or replace internal FOX2 procedural limits; it cannot create a real permission denied by Google Drive, Git, OS, financial-data providers or a third-party system. Technical execution is gated by actual access/evidence. A mismatch must be reported with a specific remedy rather than an imaginary Publisher PASS.

**A7.3 — Later policy releases:** Use the same frozen identity + Owner decision + real write/readback + revocation/supersession evidence. Optional independent review is risk-directed, not an absolute inherited precondition. In particular, a simple policy revision does not wait for a new Git repository or a private code-worktree before internal document publication.

---

# B. FOX2 BRD LIFECYCLE, APPROVAL & PUBLICATION POLICY — `FOX2-BRD-POLICY-V1`

## B1. Canonical BRD ownership and change contract

A requirement has **one** `BRD_ID / revision / REQUIREMENT_ID` as its canonical business owner; cross-cutting controls and dependencies are separately linked. Identified candidate BRD domains: `00` common standards; `01` capital; `02` screening/discovery; `03` portfolio risk; `04` exit/profit protection; `05` market/sector/stock analytics; `06` data foundation; `07` research/backtests; `08` localhost dashboard. These domain labels are **not proof of release**.

Each BRD Candidate records owner, version, requirements, business rationale, inputs/units, outputs, non-goals, risk, sources/freshness, consumers, source set, acceptance IDs and provenance. A material BRD change carries a **Business Change Contract (BCC)**: exact source revision and SHA-256; changed requirements; positive/negative examples; transitive affected consumers; allowed/forbidden behavior; unresolved issues; proposed stage; risk-based review when applicable and Owner decision. A UI WP cannot redefine accepted domain calculations without Owner-approved change.

## B2. Distinguish Owner business decisions

**Case A — Owner approves BRD content only.** Record exact BRD/BCC version, decision scope and exclusions. Publish it via Owner-delegated actual Library writer/readback. Git mirroring is not a prerequisite for the BRD document to be published. No DEV request is inferred.

**Case B — Owner approves BRD and requests implementation.** Reuse the same frozen decision, then verify actual executor host/Git rights, source/acceptance and one-writer ownership for scoped implementation. Owner may issue internal technical delegation; the delegated Agent cannot claim OS/Git capabilities it does not possess. Do not repeat the unchanged Owner decision.

Any material change in accepted business/risk scope reopens BCC/decision only for the affected closure. Never silently merge Git edits back into a BRD; require an Owner-approved FOX2 Library revision and actual publication readback.

## B3. FOX2 BRD document → technical mirror (separate evidence tracks)

**Document lifecycle:** `DRAFT → OWNER_APPROVED_EXACT_REVISION → LIBRARY_PUBLISHED → SUPERSEDED/REVOKED`. **Implementation-source lifecycle, if needed:** `GIT_MIRROR_PENDING → GIT_MIRROR_VERIFIED → DEV_ELIGIBLE_AFTER_SCOPED_OWNER_GRANT`. Source publication is not held hostage by unavailable Git, and an effective document is not proof of code execution.

| Gate | Operation and actor | Evidence / success condition |
|---|---|---|
| `G0` | CHAT freezes FOX2 Candidate and bounded BCC/acceptance | Exact source version/file ID/raw digest, risk/consumer mapping |
| `G1` | Owner accepts exact BRD revision and scope; reviewer only if specifically required | Recorded decision and unresolved scope exclusions |
| `G2` | Owner/Owner-delegated actor with **actual Library rights** publishes BRD | `/Trading/FOX2/01_BRD/` output file ID, bytes/hash and verified readback; no external issuer assumed |
| `G3` | When implementation needs a Git mirror, Owner designates the authorized repository writer | Confirm actual private FOX2 repo, allowed path, worktree/branch/one writer; write identical content |
| `G4` | Verify real immutable `git show <commit>:<path>` against Library | Matching raw SHA-256 and correct FOX2 project, file revision and size |
| `G5` | CHAT records a project-native traceable mirror evidence receipt | Observed Library ID/revision/hash ↔ Git repo/full commit/path/hash, source freshness; no fabricated cryptographic signature |
| `G6` | CHAT checks R0–R7 before implementation prompt | Explicit Owner-bounded DEV decision, actually verified host/source/worktree and accepted tests |

If Library publishing succeeds and Git is absent, the BRD is `LIBRARY_PUBLISHED / MIRROR_PENDING`; do **not** downgrade published document status or claim `MIRROR_VERIFIED`. No code handoff until its applicable verified source and actual scoped technical authorizations exist. Never automatically write from Git into the canonical Library source; previous revisions remain accessible as history.

## B4. Source Binding Receipt schema — required fields

```yaml
project: FOX2
brd_id: <verified-id>
brd_revision: <immutable-approved-revision>
requirement_ids: [<verified-requirements>]
bcc_id: <approved-bcc>
acceptance_ids: [<approved-acceptance-ids>]
library_file_id: <actual-id>
library_path: /Trading/FOX2/01_BRD/<exact-file>
library_raw_sha256: <real-64-hex-digest>
library_size_bytes: <measured-size>
library_release_id: <actual-owner-authorized-library-release-record>
source_set_id: <real-source-set-id>
source_manifest_sha256: <real-64-hex-digest>
git_private_repo: <verified-repo>
git_full_commit_sha: <immutable-commit>
git_path: docs/brd_mirror/<exact-file>
git_raw_sha256: <real-64-hex-digest>
mirror_receipt_id: <real-traceable-project-native-receipt>
issuer_and_validity: <owner-delegation-actual-writer-rights-and-revocation-state>
status: <BRD_MIRROR_VERIFIED-or-PENDING-or-BLOCKED>
```

Placeholders are examples, **not verification**. A system may automate publishing/mirroring after Owner approval, proven file/repository permissions and successful negative tests. Mechanical file receipts document observable facts; do not imply protected signing or independent third-party trust without evidence. Retry must be idempotent, append-only for release history, and never silently overwrite.

## B5. BRD change, staleness and rollback

- Every later approved revision produces a **new** Library release, Git mirror commit, digest and receipt; do not alter or rewrite prior immutable source snapshots.
- Impact-analysis by requirement/dependency identifies affected WPs and contracts; mark them `STALE` and pause until re-pinned and reauthorized. Preserve completed unrelated tasks and WIP.
- Revoked/rolled-back Library source invalidates dependent BRD mirror receipt; historical Git content is history, not new authority.
- Negative acceptance tests: Owner approval without actual Library write/readback (`NOT_PUBLISHED`); Library publication without Git (`LIBRARY_PUBLISHED / MIRROR_PENDING`); mirror byte mismatch (`DIVERGED`); revoked source despite matching hash (`BLOCKED`); Agent editing canonical Library indirectly via Git (reject); no observed technical authorization (do not code).

---

# C. FOX2 AGENT PROMPT, ROUTING & WORK PACKAGE POLICY — `FOX2-AGENT-PROMPT-POLICY-V1`

## C1. Mandatory Routing Precheck before any executable assignment

`POLICY_CHECK → TASK_STATE_CHECK → ROUTING_PRECHECK(R0–R7) → ASSIGNMENT_CHECK → RESPONSE / PROMPT_PREPARATION`.

| Check | Required observed decision |
|---|---|
| **R0** | Check task, accepted results, existing tests and source snapshots first. Reuse complete validated work; no redundant reruns or initial Foundation recreation. |
| **R1** | Classify actual stage: L0 planning, protected document publication, DEV, test, review, integration or release. |
| **R2** | Check FOX2-only Owner and valid expressly applicable higher authority, BRD/BCC/acceptance, risk, `CODE_ALLOWED` and actual technical gates. Do not import restrictions from another project. Missing technical proof blocks that action, not internal document revision. |
| **R3** | Verify actual candidate Agent product, host/tool accessibility, model/mode, quota, access and independence. Never invent live availability. |
| **R4** | Compare CHAT, COPILOT, CODEX, WORK and other eligible Agents using **least cost per safely accepted result**, then consider 70/30 target. |
| **R5** | Inspect exact files/worktree, branch/base SHA, tracked/untracked/ignored WIP, single writer lease and allowed/denied paths. |
| **R6** | For executable DEV, verify FOX2 Library BRD and actual Git mirror when used, full commit/path/hash, source freshness and handoff/acceptance. L0 Policy/BRD publication needs its own readback only; it must not await Git. |
| **R7** | Name chosen **Role · Engine/Model · Thinking/Optimize mode · Scope**, operation order, evidence requirements and STOP boundaries; only after eligibility. |

CHAT must record `POLICY_CHECK`, `TASK_STATE_CHECK`, `R0–R7` and assignment disposition. Preparing a draft prompt is allowed at L0 as `PROMPT_PREPARED/NOT_EXECUTABLE`; it must not instruct protected execution unless both **SOURCE_READY** and **EXECUTION_AUTHORIZED** independently PASS. Each project-work answer includes a factual **Phân công** section identifying what is done now, blocked, waiting or unnecessary.

## C2. 70/30 resource allocation — Owner's latest decision

**Target** is Copilot **70%**, Codex **30%**, measured as counts of **accepted, eligible, material implementation WPs** at rolling checkpoints. No forced split by BRDs, source lines, tokens, risk weight, person-hours, cost or individual source modules. CHAT planning and standalone independent WORK reviews are **excluded** from denominator. For fewer than 10 eligible accepted WPs, report `TARGET_NOT_YET_MEASURABLE`; do not manufacture compliance. No artificial task splitting or duplicated work to inflate one Agent's share.

| Work family | Proposed first candidate | Conditions |
|---|---|---|
| BRD/BCC interpretation, design, scope and routing | **CHAT** | Architecture/security gets independent review when material. |
| Windows environment/Git read-only/source hash, IDE, frontend, React, dashboard, charts, ordinary fixes/tests/doc | **COPILOT** | Verified access/quota/model, approved path/write right for actual operation. |
| Straightforward FastAPI routes, routine backend/CRUD/mock adapters/fixtures/refactors and local integration | **COPILOT** often | Can move to Codex on technical complexity, capability, safety or lower accepted cost; backend label alone is not decisive. |
| Domain core/backend hard algorithms, risk/calculation correctness, historical data quality, point-in-time, concurrency, hard debugging | **CODEX** often | Accepted spec, right effort/quota, independent risk review when applicable. |
| Independent policy/safety/release review | **WORK**, qualified COPILOT, or other independent reviewer | Verifiable independence, access and actual reviewer grant. Never review one's own authored change as independent. |

If a checkpoint is risk-heavy, Codex may safely exceed 30%; UI-heavy checkpoints may exceed Copilot 70%. Record rationale/acceptance evidence and do not compromise safety to hit the ratio.

**Model policy:** Always observe actual selectable model/mode and quota. For Copilot, `Auto` plus `Efficiency/Balance/Intelligence` are only *candidate UI modes when observed*; these are not comparable to Codex thinking values. For Codex, `Light` for simple bounded tasks, `Medium` for ordinary coded spec, `High` for genuinely hard concurrency/architecture/safety only when those modes really exist and are eligible. Unknown model/quota = `UNKNOWN`, not an assumed actual setting.

## C2A. Model, Thinking & Token/Credit Optimization — `FOX2-AGENT-COST-001`

**Scope and effectivity.** This clause specifies operational decisions within `FOX2-AGENT-PROMPT-POLICY-V1`, **not a separate Policy**, and does not modify authority or release gates in A/B. It is effective only within this published FOX2 Policy V1.0. Objective: **minimize expected total token/credit and rework cost per safely accepted WP**, subject to correctness, source integrity, domain risk, independent review obligations and all authorization gates. Do **not** optimize raw token count at the expense of reliable acceptance. The 70/30 target from C2 applies to accepted material WP counts, **not** token allocation or a guaranteed 70/30 spend.

### C2A.1. Verified engine/model/effort matrix (proposed defaults; not current account capabilities)

| Executor / task | Lowest sufficient starting proposal | Escalate only on recorded conditions | Availability caveat |
|---|---|---|---|
| **CHAT** — routing, BRD interpretation, ordinary spec and policy delta | Current CHAT engine/model explicitly recorded + **Medium** where selectable | **High** for substantial architecture, broker semantics, concurrency, safety or a release-level decision | Actual model and effort must come from observed product/session; do not assume historical model names remain selectable. |
| **COPILOT** — Git inspection, repeated IDE tasks, simple docs and UI fixes | `Model: Auto` / `Optimize for: Efficiency` **only if supported** | `Balance` for routine implementation; `Intelligence` only for demonstrated higher reasoning burden | Record selected model if disclosed; when `Auto`, actual underlying engine remains `AUTO_UNRESOLVED` unless observed. Modes are Copilot-specific and **not** equivalent to Codex Thinking. |
| **CODEX** — bounded Git/simple fix, normal backend, critical core | **Light** for small authorized bounded changes; **Medium** for backend/API/algorithms with accepted spec | **High** for demonstrated hard architecture, concurrency, broker/financial safety, data time invariants or repeated material failures | Use actual product model and supported effort from the current agent host; do not assert a historic model or a non-selectable level. |
| **WORK** — independent review/readiness | **Medium** for targeted delta audit when independence/access/grant are verified | **High** for deep consequential audit, significant safety or release risk | WORK is **not** a compulsory reviewer for every trivial WP and not part of Copilot/Codex 70/30 counts. |
| **Other qualified Agent / deterministic tooling** | Cheapest actually eligible mode or deterministic read-only check | Only if normal tests and existing evidence cannot satisfy acceptance | Must pass the same routing, source, authority, reviewer independence and license constraints. |

**Selection rule:** verify actual `product`, `engine_model`, `mode`, `agent_host`, `quota_remaining` (if exposed), usage/billing model and access before executable dispatch. The named defaults are **suggestions**, not entitlements or verified live availability. If quota/model/capability is materially unknown, output `BLOCKED/UNKNOWN` for the executable assignment; CHAT may prepare a clearly non-executable L0 candidate instead. Compare CHAT, COPILOT, CODEX, WORK and other eligible options at R4; do **not** route to Copilot only to satisfy 70/30, or to Codex just because a task contains Python.

### C2A.2. Budget and accepted-cost ledger per Work Package

Before any executable WP, CHAT adds a *resource plan* bound to actual scope: `estimated_input_tokens`, `estimated_output_tokens`, `estimated_credits_or_requests`, `budget_source_and_confidence`, `retry_limit_or_review_threshold`, `expected_accepted_result`, `complexity_risk`, and `escalation_trigger`. Unknown usage prices or quotas are `UNKNOWN`, never invented; estimates are planning ranges, not facts. For read-only L0 drafting, unavailable budgets may be marked `NOT_MEASURED` without falsely representing DEV readiness.

At handoff/acceptance, record: `wp_id`, actor/model/mode, source-set, attributable measured token/credit usage **if observable**, run/retry count, time where reliably measurable, test/acceptance result, avoidable rework, reviewer cost if attributable, and route change reason. Do not claim financial savings if product billing/credit values are unavailable. Compare **total accepted cost** across agents, not price per request; when providers charge on incompatible units, keep separate columns rather than fabricate a conversion.

**Measurement:** `accepted_unit_cost = observed_total_cost / count(accepted_material_WPs)` **only when a comparable cost unit and complete attribution exist**; otherwise `COST_UNVERIFIED`. Also report `retry_rate`, `% accepted without rework`, `quota_remaining_if_known`, and actual Copilot/Codex accepted-WP ratio. Exclude aborted/blocked/draft/review-only WPs from the 70/30 denominator; do not suppress their actual consumed costs from an overall expenditure report. Do not artificially fragment WPs to game either metric.

### C2A.3. Minimum Necessary Context with immutable-source proof

Provide Agent with exact scope, BRD ID/revision, requirement/acceptance IDs, pinned Library/Git commit/hash/receipt, relevant API contracts, bounded read paths, necessary evidence and STOP conditions. **Do not paste the entire repository or all BRDs into every prompt** when a verified immutable reference and concise requirement slice suffice. However, token economy **must not replace** the receiving Agent's actual BRD/source hash/authority verification, relevant dependency closure, test requirements, safety instructions or independent review. Where access to those source references is unavailable, block executable assignment rather than supply unverified excerpts.

Prefer structured source manifest + pointers, concise delta from last accepted baseline, exact changed-path lists, targeted file reads and reusable fixture/test reports. Reuse still-valid hashes, tests, risk findings and read-only observations from R0; invalidate only affected evidence when source/contracts change. Compress verbose logs to reproducible command, key failures and artifact reference while keeping raw evidence accessible for authorized review. Never remove provenance, timestamps, negative tests or essential domain counterexamples solely to save tokens.

### C2A.4. Escalation, retries and STOP economics

Start at the lowest **supported** level sufficient for the verified risk, not always the cheapest nominal label. Escalate from Efficiency→Balance→Intelligence, or Light→Medium→High **only if those modes actually exist on the selected host** and concrete signals justify it: materially failed acceptance, complex root cause, architecture/concurrency/data/risk ambiguity, repeated failed bounded fix, or a release/safety decision. Record `prior_attempt_evidence`, `reason`, `target_mode`, estimated added cost, changed scope, and the separate reviewer/grant checks if necessary. For a straightforward repeated failure, prefer **one focused re-evaluation of the failing test and evidence**, then re-route/re-spec as appropriate instead of an open-ended high-thinking retry loop. A STOP or authorization issue is **never** solved by higher Thinking.

Prefer deterministic commands/tests/checks for known procedures. Run targeted tests before expanding to broader suites based on dependency impact, except where mandated full checks are release gates. Avoid double review of routine low-risk changes; **do not omit** required independent safety, source/release or domain reviews. Parallelize only if isolated paths, frozen contract and demonstrated cost/latency benefits outweigh coordination overhead.

### C2A.5. Mandatory prompt addendum (extends C5, no duplicate prompt master)

```yaml
resource_optimization:
  role_engine_model_thinking_scope: <actual-observed-identity-and-exact-scope>
  candidate_comparison_r4: <verified-options-and-accepted-cost-reason>
  minimum_sufficient_mode: <supported-setting-and-risk-rationale>
  input_token_target: <measured-or-estimate-or-UNKNOWN>
  output_token_target: <measured-or-estimate-or-UNKNOWN>
  credit_or_request_budget: <observable-budget-or-UNKNOWN>
  quota_observation: <actual-source-time-or-UNKNOWN>
  context_manifest: <immutable-sources-and-required-relevant-paths>
  evidence_reuse_manifest: <valid-cached-tests-and-invalidation-rule>
  retry_escalation_threshold: <bounded-trigger-and-STOP>
  usage_measurement_plan: <observable-provider-data-or-NOT_MEASURED>
  quality_release_gates_unchanged: true
```

For executable handoff, required identities, access, quota, source, grants and writer exclusivity must still be verified at R0–R7; placeholder/UNKNOWN **cannot** be upgraded to PASS merely because a budget field exists. A chosen model/mode is a **routing proposal** until the user-facing Agent/tool actually confirms and runs it. Never call a predicted token count a measured usage result.

### C2A.6. Negative acceptance checks for resource routing (proposed, NOT_RUN)

- `OPT-N01`: low-token prompt omits source authentication or required negative tests → **REJECT/BLOCK**.
- `OPT-N02`: Copilot quota/model or Codex mode unverified yet assigned as executable → **BLOCKED/UNKNOWN**.
- `OPT-N03`: 70/30 KPI used to override risk/reviewer/writer ownership → **REJECT ROUTE**.
- `OPT-N04`: premium/high setting chosen without complexity/failed-test/risk evidence → **REVISE COST PLAN**.
- `OPT-N05`: source/dependency changes make reused fixture/test evidence stale → **INVALIDATE affected evidence; re-test**.
- `OPT-N06`: invented cross-provider token-to-credit conversion or claimed savings with no usage observation → **COST_UNVERIFIED**.
- `OPT-N07`: disabling mandated test/review merely to meet budget → **REJECT**.
- `OPT-P01`: eligible observed mode, source/DEV and isolated scope verified, concise reference context, targeted tests PASS, actual usage/evidence captured → **ELIGIBLE FOR ACCEPTANCE REVIEW**, not permission to merge or LIVE.

## C3. One approved BRD → multiple WPs; no alternate BRDs

For each approved `BRD_ID`/revision, CHAT creates scoped WPs with **one accountable writing Agent, one bounded behavioral output**, owned requirement+acceptance IDs, dependency graph, allowed paths, unit tests, evidence and STOP. Splitting is optional; prefer one WP if parallelism adds more integration cost than it saves. Do not split an authoritative BRD by Copilot/Codex and do not permit Agents to edit canonical Library BRD or Git mirror directly.

**Domain-to-WP examples (not executable assignments):**

| BRD | Typical COPILOT WP | Typical CODEX WP | Business/contract owner |
|---|---|---|---|
| `00` standards | UI status/source labels, routine check | Shared backend schema if specifically assigned | Common governance; one contract writer |
| `01` capital | Inputs, dashboard, display/tests | Approved sizing/capital calculations | BRD-01; separate portfolio-risk veto |
| `02` discovery | Filter/screener UI | Ranking/selection logic | BRD-02 |
| `03` portfolio risk | Exposure warnings/visualization | Risk bounds and computations | BRD-03, independent safety review if material |
| `04` exits | Profit/exit advisory display | Protection/exit analysis | BRD-04 |
| `05` market intelligence | Market/sector/stock charts | Flow-evidence processing, valuation and cycles | BRD-05 and validated data contracts |
| `06` data | Fixture quality-state UI | Adapter/point-in-time/schema/freshness logic | BRD-06; external access separate |
| `07` research | Test UI / offline harness | Backtesting, leakage controls, validation | BRD-07; independent domain acceptance |
| `08` localhost | Primary React frontend | API/backend only as needed | BRD-08; UI never redefines core formulas |

## C4. Cross-Agent Git ownership and interface freeze

- Each material writer must have a **distinct verified worktree AND branch** and nonoverlapping writable file paths and writer lease; a branch name alone is insufficient. Use exact verified base SHA, checked HEAD/WIP and task/host-specific grants. Git mirror `docs/brd_mirror/**`, secrets and other Agents' scopes are denied to ordinary implementers.
- Shared API/schema/migrations/config are owned by **one** designated writer. Freeze accepted interface schema and fixtures before parallel frontend/backend WPs. If paths or contract overlap, serialize edits and allow the other Agent to act read-only/propose changes through an authorized handoff. No rebase/reset/stash/force push/merge without separately evidenced operation grants.
- Proposed only (not actual created): `work/FOX2-<TASK>-contract`, `work/FOX2-<TASK>-ui-copilot`, `work/FOX2-<TASK>-api-codex`; integration requires a separate authorized writer and accepted tests.

## C5. Required Agent execution prompt / WP record

```yaml
project: FOX2
task_id: <verified-task>
change_id: <verified-change>
wp_id: <one-unique-WP>
route:
  role: <actual-role>
  agent_product: <COPILOT-or-CODEX-or-other>
  engine_model: <observed-model-or-UNKNOWN>
  thinking_or_optimize_for: <actual-supported-setting>
  host_and_verified_quota: <evidence-or-UNKNOWN>
resource_optimization: <C2A.5-required-addendum-fields>
source:
  effective_policy_release: <actual-FOX2-owner-authorized-library-publication>
  brd_id: <approved-id>
  brd_revision: <approved-revision>
  requirement_ids: [<ids>]
  bcc_id: <accepted-BCC>
  acceptance_ids: [<ids>]
  source_set_id: <verified-set>
  source_manifest_sha256: <measured-hash>
  library_file_id: <verified-file>
  library_raw_sha256: <measured-hash>
  git_private_repo: <verified-repo>
  git_full_commit_sha: <real-immutable-commit>
  git_path: docs/brd_mirror/<exact-file>
  git_raw_sha256: <measured-hash>
  mirror_receipt: <observed-FOX2-library-to-git-evidence-or-not-applicable>
execution:
  phase: <READ_ONLY-or-DESIGN_ONLY-or-AUTHORIZED_MATERIAL_DEV>
  goal_and_exclusions: <bounded-behavior-and-nongoals>
  frozen_interface_dependency: <accepted-contract-ref>
  allowed_paths: [<explicit-paths>]
  forbidden_paths: [docs/brd_mirror/**, <other-agent-paths>, <secrets>]
  worktree_branch_base_wip: <observed-references>
  exclusive_writer_lease: <actual-lease>
  separate_dev_grant: <actual-grant>
  code_allowed: <verified-YES-or-NO>
  permitted_git_operations: [<explicitly-granted>]
  tests_positive_negative: [<accepted-test-ids>]
  evidence_destination: <verified-location>
  measured_usage_or_not_observable: <actual-telemetry-or-NOT_MEASURED>
stop_if: [authority_unknown, source_stale, sha_mismatch, receipt_missing,
          quota_unknown, worktree_collision, contract_drift, grant_absent,
          repo_mismatch, WIP_collision]
```

Never replace placeholders with guesses or treat a prepared draft as executable. The recipient must independently open exact `full Git commit:path` when Git is used, hash its raw content and verify the actual FOX2 provenance receipt and current scoped Owner authority before writing; return `SOURCE_RESOLUTION_VERIFIED / STALE / DIVERGED / UNKNOWN / BLOCKED` with evidence. Source verified still does **not** confer DEV rights.

## C6. Execution handoff, review, integration and STOP

Implementing Agent returns actual actor/model/mode, source receipt, branch/worktree/head/diff, changed paths, tests, positive/negative acceptance evidence, unresolved issues, measured (not guessed) quota cost, writer ownership, next actor and STOP. Risk-based independent review applies where Owner specifically requires it or a demonstrable external/safety obligation applies; it cannot be a blanket veto imported from another project. Integration needs scoped Owner decision, real Git permission, single integrator, green tests and current source. No hidden push/deployment.

**Minimum negative acceptance suite — proposed, NOT_RUN:**

- `V1-N01`: an external project source without express verified FOX2 applicability cannot be treated as binding FOX2 Policy; incomplete FOX2 Library write is not a release.
- `V1-N02`: Owner BRD approval without a completed and read-back FOX2 Library publication → `OWNER_APPROVED_NOT_PUBLISHED`.
- `V1-N03`: Library-published BRD without an applicable verified Git mirror → document remains `LIBRARY_PUBLISHED`; `MIRROR_PENDING` blocks Git-based DEV handoff only.
- `V1-N04`: matching hash but revoked Owner delegation, missing actual receipt, wrong Git commit or CRLF mismatch → block affected Git DEV handoff.
- `V1-N05`: `SOURCE_VERIFIED` and `CODE_ALLOWED=NO` → no code changes.
- `V1-N06`: two Writers on same file/worktree or missing exclusive lease → deny second writer.
- `V1-N07`: changed shared API contract / stale BRD during parallel execution → pause affected WPs and re-pin after review.
- `V1-N08`: tests PASS but review/merge/release absent → no integration claim, no LIVE.
- `V1-N09`: unknown Agent model/quota/access → do not emit executable assignment based on 70/30 target.
- `V1-N10`: Agent edits `docs/brd_mirror/**` / self-promotes a BRD → reject and request proper BRD change flow.
- `V1-N11`: synthetic data rendered as live or null treated as zero → reject acceptance.
- `V1-N12`: FOX2 policy work initiates unauthorized cross-project migration or accesses unrelated work-in-progress → block.
- `V1-P01`: exact Library-published BRD, source mirror where necessary, scoped Owner technical delegation, isolated Copilot/Codex WPs, frozen contract, measured tests and appropriately reviewed integration → eligible for Owner-authorized integration decision only.

---

# D. RELEASE CONTROL AND INTERPRETATION

## D1. Effective policy boundary

This consolidated FOX2 Policy V1.0 controls FOX2 internal document governance on and after a successful Owner-authorized Library write/readback with a verifiable release manifest. Section A controls authority and safety, Section B controls BRD lifecycle, and Section C controls Agent prompt routing and Work Packages. No standalone draft creates a second competing FOX2 policy.

## D2. Historical source and release evidence

The publication manifest, stored alongside the released policy, binds the actual final file ID/path/size/SHA-256, the Candidate REV5 source ID/hash, the Owner instruction, and the observed readback. Previous draft snapshots are retained solely as provenance and must not override the exact released Policy. Publication metadata is evidence of the document transaction, not proof of reviewer independence, host credentials, Git permissions or operational code release.

## D3. Explicit limits of this publication

- Owner has the highest authority for FOX2 internal decisions and can delegate document and technical responsibility; actual platform operations must still succeed under verified access.
- No cross-project documents, permissions or release checkpoints apply automatically. Existing separate workflows remain unchanged.
- `CODE_ALLOWED=NO` for policy publication; no Git merge, release of code, broker connection/order-write or LIVE is authorized by this document.
- Any later change to this V1.0 requires a new frozen source, accountable Owner decision, actual Library write/readback and supersession evidence under A7.
- Agent product/model/mode/quota and current Git ownership remain `UNKNOWN` until actually checked for the relevant handoff; do not infer readiness from this release.

## D4. Routing disposition for document publication

`POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK` applies to executable handoffs. This publication is an L0 document operation: CHAT is the delegated operator and verifies the Library source; COPILOT and CODEX are not assigned coding or Git tasks; WORK is not assigned a discretionary extra audit. Current technical entitlements are not presumed. Stop before any DEV/Git/LIVE activity without a separate scoped authority and evidence.
