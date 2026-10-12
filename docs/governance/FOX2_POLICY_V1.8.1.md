# FOX2 — POLICY V1.8.1 | CONSOLIDATED GOVERNANCE

**Document ID:** `FOX2-POLICY-V1`  
**Version:** `1.8.1`  
**Applicability:** `FOX2 ONLY`  
**Release date:** 2026-10-12 (Asia/Ho_Chi_Minh)  
**Document authority:** FOX2 Owner; CHAT acts as delegated Library document operator; an expressly Owner-assigned publisher such as WORK may perform this scoped document operation with observed Library access.  
**Change / supersession:** `FOX2-C5B-EXECUTION-ROUTING-SELECTOR-20261012`; supersedes V1.8 **only after** V1.8.1 Library publication, exact readback and release manifest. This release refines the Local Agent dispatch UX into an explicit three-stage Execution Routing Selector, removes redundant save-only options, and binds Owner-confirmed Agent/Model/Thinking configuration into the Bridge dispatch contract. All unaffected V1.8 controls remain in force. Preserve V1.0–V1.8 and existing Git evidence as immutable history.  
**Status:** `RELEASED_EFFECTIVE` for FOX2 internal governance **only upon successful V1.8.1 Library publication, exact byte readback and release manifest**. This document alone is not proof of publication.  
**Parent release:** V1.8 official Library source SHA-256 `226fecb094843d492e87c4768f5741726a4651b7556d5ec0abf3739e9720dd7b`; V1.8 Local Agent single-check dispatch remains immutable history.  
**Release verification:** See separate FOX2 V1.8.1 release manifest for the actual provider file ID, bytes, SHA-256, operation and receipt. The text alone is not evidence that a write occurred.  
**Exclusions:** V1.8.1 preserves the C6F.2A standing Copilot report-only authorization and Result Contract/schema v2. The Execution Routing Selector controls Owner choice and dispatch transport for an already checked executable WP; it does **not** itself create DEV, code-push, main-push, merge, Production API/broker, deployment or LIVE rights. Preferred native interactive UI is a presentation layer; equivalent explicit-confirmation fallback semantics remain authoritative when that UI is unavailable.

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
12. **Owner clarification 2026-10-12 — source-access routing:** CHAT validates ChatGPT Trading Library; COPILOT/CODEX receive applicable documents through Git/local snapshots; **WORK is permitted to use CHAT conversation/project context and ChatGPT Trading Library/other existing connected sources to the extent these are actually available in WORK**, with no artificial reduction of its existing access or execution role. Access permissions and tool capability remain distinct facts.
13. **Owner upgrade 2026-10-12 — Git-first operational loop:** FOX2 Git is the canonical *operational* record for work-package assignment, versioned implementation, sanitized tests/evidence, Agent report, CHAT review and handoff. Agents submit results through a task-scoped **branch push + PR/commit receipt** after actual Git capability, source and scoped write grants are verified. Library remains the authority for **issued Policy/BRD**; Git does not publish/promote them by itself. Direct pushes or merges to `main` by an implementing Agent are not authorized by this policy.
14. **Owner upgrade 2026-10-12 — one-action Local Agent dispatch:** after CHAT has completed and recorded the Agent Prompt Policy checks for an executable WP, CHAT presents an execution selection. Owner selection `EXECUTE_LOCAL_AGENT` authorizes CHAT to publish one immutable, task-bound dispatch artifact to FOX2 Git. The Local Bridge consumes that artifact and performs only runtime attestation; it must not repeat or override the completed Policy/task/routing/assignment decision checks. No selection means no local execution.
15. **Owner refinement 2026-10-12 — staged Execution Routing Selector:** after an executable prompt is ready, CHAT first offers the terminal manual-VS-Code path versus automated-Agent configuration; only the automated path opens Agent/Model/Thinking selection, and only after that configuration is explicitly confirmed does CHAT ask whether to dispatch through the Local Bridge. `SAVE_PROMPT_ONLY` and `SAVE_CONFIGURATION_ONLY` are removed. A preselected radio option is a recommendation only; explicit confirmation is required at each decision screen.

---

> **Owner source-delivery clarification 2026-10-12:** CHAT owns source upload/recovery; implementation tasks stay internally SOURCE_PENDING until CHAT completes remote verification and records the single GIT_SOURCE_READY=YES decision.

> **Owner extension 2026-10-12 — Agent Result Contract v2:** every new FOX2 Git-first Agent result must contain a human report, schema-validated machine manifest, verifiable acceptance/test/evidence mapping and an independent CHAT review receipt. Detailed normative controls: C6B–C6F. The source of truth for released Policy/BRD remains Library, while Git is the operational system of record for task/results.

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

**WORK — full permitted scope, no artificial rights reduction:** Owner expressly permits WORK to use CHAT conversation history, project context, ChatGPT Trading Library, connected applications and other sources when those are actually exposed to the WORK session by the platform. WORK is **not restricted to Git/local** and is **not limited to read-only or reviewer-only work** by this access-routing rule; it may perform research, planning, document operations and other Owner-delegated work within actual tool permissions. Independent review is optional when Owner elects except where an evidenced, specifically applicable obligation requires it. No document can manufacture a platform connection, credentials, issuer status, DEV/Git rights, provider entitlements or LIVE. Never invent an audit PASS or impose a discretionary review waived by Owner.

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
/Trading/FOX2/07_Agent_Handoff/             # Owner-approved operational task/handoff records; Library view/staging, Git operational counterpart
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
3. **Actual Publisher action:** Owner is publication decision-maker. CHAT or another expressly Owner-delegated document publisher is the operator only with observed Library upload rights. Each subsequent release is a **new, immutable version file** at `/Trading/FOX2/00_Governance/FOX2_POLICY_V<version>.md`; use the exact new version filename (this release: `FOX2_POLICY_V1.8.1.md`). Preserve V1.0/V1.1; never overwrite an effective source. No external protected key is assumed to exist.
4. **Readback:** List destination, read exact uploaded source and independently compare file ID, raw bytes/SHA-256, project scope and intended label. Record observed date/time and actual operator; no backdated/imaginary issuance.
5. **Evidence:** Create an Owner-decision-linked publication manifest containing actual output ID/path/hash and status. If upload or readback fails: `PUBLICATION_INCOMPLETE`, never `EFFECTIVE`. If a real external controlled issuance gate is demonstrated, stop only that affected issuance and record the named authority/evidence.
6. **Effective classification:** Only after steps 1–5 truly complete, record `FOX2_DOCUMENT_POLICY_PUBLISHED` and `RELEASED_EFFECTIVE(scope=FOX2, internal_document_governance_only)`. This label does **not** assert a protected signature, Git sync, Agent result push, DEV, broker, margin or LIVE. Review any future changes against the latest actually published FOX2 version.

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

If Library publishing succeeds and Git is absent, the BRD is `LIBRARY_PUBLISHED / MIRROR_PENDING`; do **not** downgrade published document status or claim `MIRROR_VERIFIED`. No code handoff until its applicable verified source and actual scoped technical authorizations exist. Apply the single `GIT_SOURCE_READY` checkpoint in C1B.1; a failed upload keeps the dependent task SOURCE_PENDING even if the Agent prompt is correct. Never automatically write from Git into the canonical Library source; previous revisions remain accessible as history.

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
| **R3** | Verify actual candidate Agent product, host/tool accessibility, model/mode, quota, access and independence; use C1A source matrix. Never invent live availability. |
| **R4** | Compare CHAT, COPILOT, CODEX, WORK and other eligible Agents using **least cost per safely accepted result**, then consider 70/30 target. |
| **R5** | Inspect exact files/worktree, branch/base SHA, tracked/untracked/ignored WIP, single writer lease and allowed/denied paths; separately verify evidence-branch writer before any report push. |
| **R6** | CHAT verifies FOX2 Library Policy/BRD authority; receiver verifies the copy accessible per C1A. For Git-based tasks verify pinned task commit, mirrored source where required, report destination/commit and handoff freshness. L0 Library publication is independent of Git. |
| **R7** | Name chosen **Role · Engine/Model · Thinking/Optimize mode · Scope**, operation order, evidence requirements and STOP boundaries; only after eligibility. |

CHAT must record `POLICY_CHECK`, `TASK_STATE_CHECK`, `R0–R7` and assignment disposition. Preparing a draft prompt is allowed at L0 as `PROMPT_PREPARED/NOT_EXECUTABLE`; it must not instruct protected execution unless both **SOURCE_READY** and **EXECUTION_AUTHORIZED** independently PASS. Each project-work answer includes a factual **Phân công** section identifying what is done now, blocked, waiting or unnecessary.

### C1.1. Single-check / runtime-attestation rule — no duplicate governance evaluation

When CHAT has recorded `POLICY_CHECK=PASS`, `TASK_STATE_CHECK=PASS`, `ROUTING_R0_R7=PASS`, `ASSIGNMENT_CHECK=PASS`, applicable `GIT_SOURCE_READY=YES`, and `EXECUTION_AUTHORIZED=YES` in the immutable WP source, those **decision gates are checked once** for that exact task revision. A Local Agent Bridge must not rerun the business/BRD/routing decision process or demand a second Owner approval for unchanged scope.

The Bridge performs only **`LOCAL_RUNTIME_ATTESTATION`** immediately before launch: exact dispatch/task/policy/prompt hashes and immutable commit, configured workspace mapping, actual CLI/host/Git identity, remote/branch/base relationship, current writer lease/WIP collision, and operation permissions that can change at runtime. A runtime mismatch returns `LOCAL_RUNTIME_BLOCKED` with observed facts. It does not silently reroute, broaden/narrow scope, rewrite the prompt, self-grant permission, or convert the failure into a new Policy decision. CHAT resolves any changed decision inputs and issues a new task/dispatch only when needed.

## C1A. Source-access matrix and cross-agent handoff — Owner decision 2026-10-12

**Effective change:** This is a FOX2-only clarification of *routing and evidence responsibility*, not a reduction of any WORK permissions or a grant of DEV/Git/Production/LIVE. The Owner approved immediate operational application. Historically, the V1.0 source was superseded by an independently published V1.1; V1.2 supersedes V1.1 only after its own publication/readback/manifest. All prior source snapshots remain immutable.

| Role / product | Permitted and expected source route | Who verifies what | Do not infer |
|---|---|---|---|
| **CHAT (coordinator/publisher)** | ChatGPT Trading Library and available authenticated Git/connected sources | Verify FOX2 Library release, file identity, SHA-256, effectivity, exact revision and CHAT-to-Agent source manifest | CHAT's Library readback is **not** proof an Agent received identical bytes |
| **COPILOT (Windows/IDE)** | **Accessible local files or Git** on its observed host, including supplied verified snapshots | Open local/Git source and compare its raw bytes/hash against the CHAT-pinned identity; check actual workspace/WIP only after relevant gates | Never require direct access to a ChatGPT Trading Library path; that path is metadata, not a Windows path |
| **CODEX (coding agent)** | **Accessible local files or Git** in its verified workspace | Same independent readback of relevant bytes/commit:path and source receipt; protect one-writer constraints | No direct ChatGPT Trading Library access is presumed; no Git/DEV by association |
| **WORK (ChatGPT Work)** | **CHAT conversation/project context, ChatGPT Trading Library, Git, local or connected app sources when the particular WORK session actually provides them** | Directly inspect the accessible authority source where technically available; use correct Library vs Git/local receipts; report inaccessible routes as capability facts | **Do not downgrade WORK to Git/local-only; do not remove original rights, research, document creation, or authorized tool capabilities** |
| **Other eligible Agent** | Only actually exposed sources and task-specific Owner scope | Evidence for exact source it can open | No automatically inherited access or permission |

**Mandatory C5 handoff fields for every FOX2 work package:** `active_policy_version`, `active_policy_sha256`, `source_access_channel_per_agent`, `CHAT_authority_attestation`, `receiver_readback_evidence`, `model_mode_quota_observation`, `CODE_ALLOWED`, `DEV_grant_scope`, `STOP`. Fill actual values or `UNKNOWN/NOT_APPLICABLE`, never omit or infer permissions. Source publication and agent execution authorizations are independently checked. The receiving executor reports its own `source_access_channel`, not another agent's access restriction.

**POLICY_CHECK must not ask an Agent to prove access to a source surface it cannot access by design.** CHAT establishes the policy's Library authority and conveys `library_file_id`, version, raw SHA-256, receipt and (when necessary) exact bytes through an accessible channel. COPILOT/CODEX attest independently to **received Git/local bytes**, not to a fictitious direct Library readback. If Git/local snapshot is missing or mismatched, classify `LOCAL_SOURCE_MISSING` / `SOURCE_HASH_MISMATCH` and stop only dependent action; never classify `BLOCKED_POLICY_UNKNOWN` merely because the external Agent cannot browse ChatGPT Library. If WORK does have relevant CHAT/Library access, let it use that channel; if actual WORK access is not yet observed, label **WORK_ACCESS_NOT_VERIFIED**, **not** `WORK_ACCESS_DENIED`.

**C2A applicability:** Model/effort/quota must be reported from the actual executor where exposed. `AUTO_UNRESOLVED` or `NOT_EXPOSED` is an evidence status, not fabricated numeric quota. Handle genuinely material R3 blockers as defined by C1/C2A; avoid repeated impossible Library-access checks. The 70/30 objective cannot override correct source routing.

**Handoff conformance tests** (design invariants, not claimed runtime test PASS): `ACC-01` Copilot without ChatGPT Library but with correct local Policy SHA does **not** fail Library access; `ACC-02` local SHA mismatch STOP; `ACC-03` WORK with actual ChatGPT Library access is permitted to use it and is not downgraded to Git/local; `ACC-04` WORK platform access not visible remains NOT_VERIFIED and is not claimed enabled; `ACC-05` no source-attestation authorizes DEV, merge/push or DNSE Production; `ACC-06` unaffected V1.0 BRD releases and M1 evidence remain unchanged.

---

## C1B. Git as FOX2 operational system of record — effective V1.2

1. **Authority split:** Owner-approved, readback-verified **ChatGPT Trading Library** is authoritative for released Policy, BRDs and their acceptance baselines. The private `dunglt2505/FOX2` **Git repository** is authoritative for *operational* work packages, execution branches, source revisions, sanitized reports, evidence manifests, review outcomes and handoff history **after verified synchronization**. An unmerged task branch is a pending submission, not a released BRD, accepted result or runtime release.
2. **No more manual report relay as normal path:** CHAT writes or authorizes the WP task ticket and pins exact Git source identity; an eligible Agent reads Git/local, performs the granted operation, then publishes its report and sanitized evidence to a task branch. CHAT independently retrieves **the actual branch commit/PR files** from Git to check acceptance. A chat-only result is not `EVIDENCE_PUBLISHED`.
3. **Repo paths (proposed until actually created/verified):** `docs/governance/` for authorized Policy mirror; `docs/brd_mirror/` for released BRD/contract snapshots under delegated mirror publisher; `docs/agent_handoff/<WP_ID>/task.md` and `source_manifest.json` for pinned tasks; `reports/<WP_ID>/report.md` and `evidence_manifest.json` for task output. Code/tests remain in assigned source/test directories. GitHub Issue/PR may index the corresponding immutable commit and files, but mutable issue/branch text is not the evidence identity.
4. **One active task record per WP:** `WP_ID`, assigned actor, policy/BRD+manifest SHA, base full commit, branch, allowed paths, writer claim, test criteria, expected report path, classification, push capability and STOP conditions. The Owner/CHAT controls task state; Agent cannot self-authorize DEV or mark ACCEPTED/RELEASED in its report.
5. **Protected-source mirror:** CHAT is publisher/source verifier; only separately authorized mirror writer may copy exact released Policy/BRD raw bytes to Git, with raw byte hash/commit and receipt. Task Agents cannot change `docs/governance/**` or `docs/brd_mirror/**` by default. Library updates are not implied by Git push; Git data changes do not supersede a Library release.
6. **Evidence minimization:** Git stores reproducible, necessary, scrubbed logs, assertions/test summaries, checksums and links to authorized external artifact storage. No secrets, OTP, tokens, private account details, licensed raw DNSE feeds, personal data or oversized/private binaries merely to satisfy evidence capture. If evidence cannot be safely stored in Git, store an allowed manifest/hash/availability status and request a separately approved secure evidence channel.
7. **Push is not merge:** a successful branch push/PR is `SUBMITTED_FOR_REVIEW`, not `PASS`, `ACCEPTED`, `INTEGRATED`, `LIVE`, or authority for another task. CHAT must verify Git object identity, report contents and current gate status before acceptance.
8. **Access:** COPILOT/CODEX receive Git/local only; WORK retains its allowed CHAT/Project/Library/connected source access. Every actor's actual Git writer capability and report-writing scope are independently verified; no assumption from user intent or other actor's connection.

---

### C1B.1 — One implementation-source checkpoint: GIT_SOURCE_READY

**Simple rule:** CHAT completes source synchronization and verifies `GIT_SOURCE_READY=YES|NO` BEFORE issuing or assigning an implementation task/prompt. Reuse `source_manifest.json`, `SOURCE_INDEX.json` and the existing synchronization receipt; no additional gate, schema or approval workflow.

- **YES** only after CHAT has uploaded every source required by the task in its correct released revision to Git, observed a full remote commit, and read back the required files with matching raw byte count/SHA-256, version and canonical Library release receipt. The implementation prompt binds that full commit, paths and verification receipt. Unrelated missing documents do not block a complete scoped task.
- **NO** for missing/stale/mismatched/unreleased source, failed upload/push/readback, or blobs/local commits alone. CHAT keeps the dependent implementation task internally at `SOURCE_PENDING` and does not issue or assign it to an execution Agent. A correctly worded Agent prompt is not evidence of completed synchronization; do not send a blocked implementation task to an Agent to discover or repair missing source.
- **CHAT owns upload and recovery:** CHAT performs the authorized upload, records missing paths, failed operation/error (or `CAUSE_UNKNOWN`) and a precise next recovery action in the existing receipt/index, reuses verified files and repairs only the affected delta. An upload failure does not close the synchronization task. CHAT retains responsibility until remote readback matches the official source. Do not default recovery to WORK or require Owner ZIP/file relay.
- For transient technical errors, CHAT may retry a supported operation within its existing rights after checking its actual outcome. If access, integrity or safety/platform controls block recovery, CHAT reports the exact blocker and next authorized remedy and keeps `NO / SOURCE_PENDING`. On safety refusal, STOP the affected transfer; never split, re-encode or change transport/Agent to bypass it. Source recovery and read-only audit may continue only within independently authorized scopes.

**Gate ownership:** CHAT completes and verifies delivery before dispatch. Agent source checking at receipt is a supplementary integrity safeguard, not a substitute for CHAT's completed delivery or a transfer of recovery responsibility. If source subsequently changes/disappears or mismatches, the Agent stops the affected execution and returns the blocker to CHAT. WORK provides independent audit only when assigned. `GIT_SOURCE_READY=YES` confirms source readiness only; it never grants DEV, Git code push, main/merge, Production, broker write or LIVE. No Git-to-Library writeback. Result Contract v2/schema v2 and independent CHAT result acceptance remain unchanged.

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

**Scope and effectivity.** This clause specifies operational decisions within `FOX2-AGENT-PROMPT-POLICY-V1`, **not a separate Policy**, and does not modify authority or release gates in A/B. It is effective within the current actually published FOX2 consolidated Policy (V1.2 after its own release/readback). Objective: **minimize expected total token/credit and rework cost per safely accepted WP**, subject to correctness, source integrity, domain risk, independent review obligations and all authorization gates. Do **not** optimize raw token count at the expense of reliable acceptance. The 70/30 target from C2 applies to accepted material WP counts, **not** token allocation or a guaranteed 70/30 spend.

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

### C4A. Scope-separated Git push and evidence branch protocol

**Explicit grant matrix for each task or applicable standing reporter role** (each permission remains independent; default `NO` unless a verified task grant **or C6F.2A standing authorization** applies **and** actual technical access evidence passes):

| Gate | Permission when separately verified | Not implied |
|---|---|---|
| `GIT_SOURCE_READ` | Fetch/read exact authorized Git objects; preserve uncommitted work | Git write |
| `GIT_REPORT_WRITE` | Create/edit *sanitized* `reports/<WP_ID>/**` on assigned worktree/branch | DEV code editing |
| `GIT_REPORT_PUSH` | Commit and push *only* task report/evidence paths to the designated non-main branch; provide actual remote SHA | Push elsewhere, merge, release |
| `CODE_ALLOWED` / `GIT_CODE_PUSH` | Implement approved code paths and push only approved task branch with tests | `main`, merge, Production, order-write |
| `PR_CREATE` | Open a PR pointing to submitted branch/commit if supported and granted | Approval/merge |
| `MERGE_ALLOWED` | Separate authorized integration actor, approved PR/acceptance and final head verification | Production deployment |
| `PROVIDER_PRODUCTION` / `BROKER_WRITE` / `LIVE` | Distinct sensitive gates and third-party rights | Never inferred from any Git status |

- Prefer `work/<WP_ID>-<agent>` with a unique branch/worktree/owner. A task's isolated evidence push may be authorized even with `CODE_ALLOWED=NO` **only when** `GIT_REPORT_WRITE` and `GIT_REPORT_PUSH` have a valid scoped Owner authorization (either task-specific or **standing C6F.2A**) **and** independently observed host Git access/writer safety; no source-code mutation. **Do not request a new Owner report grant for each eligible Copilot WP covered by C6F.2A.**
- Before write/push confirm `origin`, full branch/base/HEAD, writer lease, current tracked/untracked/ignored WIP, exact allowed paths and remote destination; check sensitive-content/size constraints. No `git push --force`, no history rewrite, no direct `main` push, no unapproved checkout/reset/rebase/stash/clean or collateral file changes.
- Handle collisions by pausing and reporting. If push permission/credentials/branch authorization fails, return `PUSH_BLOCKED` with exact evidence, keep local outputs unchanged and notify CHAT; never say `GIT_SYNC_VERIFIED`, `PUBLISHED`, or `ACCEPTED` based only on local commit or chat transcript.
- Branch protection and PR rules are recommended defense-in-depth but **must be configured and tested**, not assumed from this policy. Until configured, the policy's no-direct-main rule is an operational prohibition and the absence of platform enforcement is a recorded risk.

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

### C5A. Mandatory Git-first handoff fields (in addition to C5/C2A)

```yaml
git_delivery:
  issue_or_task_ref: <existing-Git-ref-or-NOT_CREATED>
  git_source_ready: <YES-or-NO-for-this-WP-required-source-set>
  source_sync_receipt: <existing-receipt-at-observed-remote-commit-or-SOURCE_PENDING>
  task_file_at_commit: <full-commit:docs/agent_handoff/WP_ID/task.md>
  source_manifest_file_at_commit: <full-commit:path>
  source_policy_library_sha256: <CHAT-attested-policy-sha>
  source_brd_library_sha256: <CHAT-attested-brd-sha-or-NOT_APPLICABLE>
  approved_git_base_commit: <full-40-hex-sha>
  agent_branch_and_worktree: <verified-isolated-branch/worktree>
  owner_writer_lease: <verified-or-BLOCKED>
  permissions:
    git_source_read: <YES-or-NO>
    git_report_write: <YES-or-NO>
    git_report_push: <YES-or-NO>
    git_code_push: <YES-or-NO>
    code_allowed: <YES-or-NO>
    pr_create: <YES-or-NO>
    merge_allowed: <YES-or-NO>
    production_provider: <YES-or-NO>
    broker_write: NO
    live: NO
  allowed_report_paths: [reports/<WP_ID>/report.md, reports/<WP_ID>/evidence_manifest.json]
  allowed_code_paths: [<explicit-scoped-paths-or-empty>]
  required_acceptance_ids: [<ids>]
  evidence_redaction_policy: NO_SECRET_NO_PRIVATE_ACCOUNT_NO_UNLICENSED_RAW_FEED
  report_push_receipt_required: true
  output_branch_commit_sha: <AGENT_FILLS_AFTER_OBSERVED_PUSH>
  output_pr_url: <observed-URL-or-NOT_CREATED>
  stop_conditions: [MISSING_GRANT, WIP_COLLISION, SOURCE_DRIFT, SHA_MISMATCH, SECRET_EXPOSURE, PUSH_FAILED]
```

For implementation, C1B.1 requires actual GIT_SOURCE_READY=YES before dispatch; prompt correctness alone is insufficient. `UNKNOWN` remains unknown; labels in a planned WP are not permission evidence. If an assigned host cannot perform a permitted push, Agent stops that step and reports blocker. CHAT may read locally transmitted evidence as a contingency but must not mark the Git deliverable complete until actual remote readback.

Never replace placeholders with guesses or treat a prepared draft as executable. The recipient must independently open exact `full Git commit:path` when Git is used, hash its raw content and verify the actual FOX2 provenance receipt and current scoped Owner authority before writing; return `SOURCE_RESOLUTION_VERIFIED / STALE / DIVERGED / UNKNOWN / BLOCKED` with evidence. Source verified still does **not** confer DEV rights.

## C5B. Execution Routing Selector and Local Agent Bridge dispatch — `FOX2-LOCAL-DISPATCH-002`

**Purpose:** turn a fully checked Agent prompt/WP into an Owner-controlled execution choice without manual copy/paste when automation is desired, while preserving the immediate manual Visual Studio Code path and avoiding duplicate Agent Prompt Policy checks.

1. **Prompt readiness state.** CHAT may expose the Execution Routing Selector only when the exact WP is `PROMPT_READY_TO_DISPATCH` and its immutable task record already contains PASS for C1 decision gates, `GIT_SOURCE_READY=YES` where required, `EXECUTION_AUTHORIZED=YES`, allowed/forbidden paths, branch/worktree plan, tests/evidence, STOP conditions and applicable grants. A draft or `SOURCE_PENDING` prompt has no executable selector.
2. **Preferred interaction component.** When the current ChatGPT client exposes an interactive form capability, CHAT SHOULD render each routing decision as a **single-select radio group plus an explicit confirmation CTA** (preferred label: `Xác nhận lựa chọn` / equivalent). A highlighted or preselected radio option is only the default recommendation and **is not Owner approval**. Only explicit confirmation advances the state. If native interactive UI is unavailable, CHAT must use a text/numbered single-choice fallback with the same explicit-confirmation semantics; fallback changes presentation, not routing logic.
3. **Screen 1 — Execution Path.** Present exactly two primary choices:
   - `MANUAL_VSCODE` — **Tự chuyển sang Visual Studio Code**. CHAT provides the normalized prompt already shown; confirmation terminates the CHAT dispatch workflow as `END_NO_BRIDGE`. No Agent/Model screen, Git dispatch artifact or Bridge action follows.
   - `CONFIGURE_AUTOMATED_AGENT` — **Thiết lập Agent / Model cho phương án tự động**. Confirmation advances to Screen 2.
   There is no `SAVE_PROMPT_ONLY` choice. If the Owner does not want to proceed, the Owner may simply not confirm a choice.
4. **Screen 2 — Agent / Model / Thinking configuration.** CHAT evaluates the already-routed task and presents a recommended configuration first, followed by eligible alternatives. Each selectable configuration must explicitly state: `agent_product`, `engine_model`, `thinking_or_optimize_for`, availability/observation status when known, and a concise reason for the recommendation. For Copilot, do not invent Codex-style Thinking levels; use the actual exposed model/mode, `AUTO`, or `NOT_EXPOSED` as appropriate. For Codex, use only model/effort values actually exposed or otherwise valid for the configured local executor. Explicit Owner confirmation freezes the selected configuration for the next screen. There is no `SAVE_CONFIGURATION_ONLY` terminal choice.
5. **Screen 3 — Transport decision.** After Screen 2 is confirmed, present exactly these routing actions:
   - `DISPATCH_VIA_LOCAL_BRIDGE` — publish the task-bound Git dispatch and send it to the configured Local Agent Bridge;
   - `BACK_TO_AGENT_CONFIGURATION` — return to Screen 2 without publishing a dispatch;
   - `CANCEL_EXECUTION` — terminate with no dispatch.
   Only explicit confirmation of `DISPATCH_VIA_LOCAL_BRIDGE` constitutes Owner dispatch intent.
6. **Selection integrity.** CHAT must not infer approval from a default radio selection, from merely viewing the form, or from an earlier Agent recommendation. Screen 1 manual confirmation ends the Bridge path. Screen 2 confirmation selects configuration only and does not authorize Bridge transport. Screen 3 Bridge confirmation authorizes only transport of the already authorized unchanged WP under its recorded grants.
7. **Git dispatch artifact.** After confirmed `DISPATCH_VIA_LOCAL_BRIDGE`, CHAT publishes one append-only machine-readable artifact conforming to `FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v1.1.json` at `docs/agent_handoff/<WP_ID>/dispatch/<DISPATCH_ID>.json` on the designated non-main operational branch. It binds `WP_ID`, exact task/source/policy/prompt identities, Owner-confirmed `agent_configuration`, selection receipt, workspace logical ID, branch/base, already-recorded decision receipts, applicable grants, STOP conditions, creation identity/time and `max_runs=1`. The Git commit containing this artifact is the transport identity consumed by the Bridge.
8. **Bridge scope.** The Bridge polls/fetches only configured FOX2 Git refs, accepts only schema-valid `EXECUTE_LOCAL_AGENT` artifacts for its configured workspace, and runs each `DISPATCH_ID` at most once. It performs `LOCAL_RUNTIME_ATTESTATION` from C1.1 and verifies that the requested Agent/Model/Thinking configuration is available and matches the dispatch. It must not silently substitute another Agent/model/mode. Unsupported or changed runtime configuration yields `LOCAL_RUNTIME_BLOCKED` and returns control to CHAT.
9. **No repeated governance evaluation.** The Bridge must not reinterpret the BRD, repeat C1 decision gates, change the selected Agent, edit governance files, broaden/narrow scope, escalate permissions, merge, deploy, or execute another task merely because it exists on Git.
10. **Runtime block/failure.** Hash mismatch, stale/revoked task, wrong repo/branch/base, missing CLI/auth, unavailable selected model/mode, writer/WIP collision, grant mismatch, forbidden staged path, duplicate dispatch, or unavailable host yields `LOCAL_RUNTIME_BLOCKED` / `DISPATCH_DUPLICATE_IGNORED` / `AGENT_LAUNCH_FAILED` as applicable. Preserve WIP; write no unauthorized code or report; return a factual receipt to CHAT.
11. **Result path unchanged.** Successful Bridge execution continues through existing Result Contract v2 and C6/C6F result-delivery controls. The dispatch artifact is not a result, acceptance, merge or release receipt. CHAT remains the independent reviewer.
12. **Idempotency and replay protection.** `DISPATCH_ID` is immutable and single-use. A retry after a transient failure requires an explicit CHAT-created retry dispatch that references the prior dispatch and preserves the same task scope/configuration unless CHAT has re-run the affected decision/configuration step because inputs changed. Branch polling alone never authorizes replay.

**Required CHAT response behavior after an executable prompt:** show the complete prompt, then Screen 1. If `MANUAL_VSCODE` is confirmed, stop the routing workflow. If `CONFIGURE_AUTOMATED_AGENT` is confirmed, show Screen 2; after configuration confirmation, show Screen 3. Never expose Bridge dispatch as the first routing choice, and never ask the Owner to repeat prompt/repository/grant data already recorded.

## C6. Execution handoff, review, integration and STOP

Implementing Agent returns actual actor/model/mode, source receipt, branch/worktree/head/diff, changed paths, tests, positive/negative acceptance evidence, unresolved issues, measured (not guessed) quota cost, writer ownership, next actor and STOP. Risk-based independent review applies where Owner specifically requires it or a demonstrable external/safety obligation applies; it cannot be a blanket veto imported from another project. Integration needs scoped Owner decision, real Git permission, single integrator, green tests and current source. No hidden push/deployment.

### C6A. Required execution → Git evidence → CHAT acceptance state machine

`TASK_PREPARED → TASK_SOURCE_VERIFIED → ROUTED_AUTHORIZED → PROMPT_READY_TO_DISPATCH → OWNER_EXECUTION_PATH_CONFIRMED → (MANUAL_VSCODE_END | AGENT_CONFIGURATION_CONFIRMED → OWNER_TRANSPORT_CONFIRMED → DISPATCH_PUBLISHED → LOCAL_RUNTIME_ATTESTED → IN_PROGRESS → LOCAL_EVIDENCE_READY → BRANCH_PUSH_VERIFIED → CHAT_REVIEW → ACCEPTED | REWORK | BLOCKED) → INTEGRATION_ELIGIBLE (separate) → INTEGRATED (if actually merged)`.

- **Agent output:** Use `reports/<WP_ID>/report.md` plus machine-readable `reports/<WP_ID>/evidence_manifest.json` stating exact actor/product/model/effort/host, source and policy hash, base/branch/worktree/writer, changed paths, test commands and results (`PASS`/`FAIL`/`NOT_RUN`), positive/negative acceptance IDs, covered date/time, sanitized reproducible evidence pointers/hashes, risk/limitations, observed token or `NOT_MEASURED`, and STOP/next step. No synthetic PASS or guessed quota.
- **Commit and push:** After actual `GIT_REPORT_WRITE/GIT_REPORT_PUSH` gates, ensure report manifest and committed paths contain no secrets/licensed feeds; commit on designated branch; push to verified remote; capture the returned full remote commit SHA and optional PR. If any gate fails, use `EVIDENCE_LOCAL_ONLY/PUSH_BLOCKED` without claiming delivery.
- **CHAT independent readback:** Resolve the task branch/PR at a **specific immutable commit**; compare requested source/changes and real reports to expected WP/acceptance; verify file hashes/test evidence, clean scope, no unauthorized paths and no security leak. Record `ACCEPTED`/`REWORK`/`BLOCKED` as a separate decision with source commit and reviewer identity, and publish that decision through an authorized Git operation. Unreviewed Git report remains `SUBMITTED`, never automatically accepted.
- **Handoff and later phases:** Agent must supply concise final chat pointer (repo, branch, full commit, PR) only as navigation; Git is the operational evidence. CHAT's acceptance does not itself allow merge/push to main, execution of code, DNSE Production, broker or LIVE; apply separate gates and owner-controlled integrator.
- **Failure/negative checks** (design requirements until tested): `GIT-N01` no source receipt; `N02` report branch differs from authorized branch; `N03` direct main/force push; `N04` Git code change under report-only grant; `N05` secrets/private/licensed feed in evidence; `N06` local commit claimed as pushed; `N07` push without verified remote SHA; `N08` report PASS without test execution; `N09` self-acceptance/self-merge; `N10` outdated WP source/branch; `N11` false WORK access restriction. All reject or block affected step.

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
- `V1-N13`: executable prompt exists but no Owner `EXECUTE_LOCAL_AGENT` selection / no immutable dispatch artifact → Bridge does not run.
- `V1-N14`: Bridge repeats C1 policy/BRD/routing decision checks and changes the already-selected Agent/scope without changed inputs → reject Bridge behavior; return to CHAT.
- `V1-N15`: dispatch/task/prompt/policy hash or commit mismatch → `LOCAL_RUNTIME_BLOCKED`; no execution.
- `V1-N16`: same `DISPATCH_ID` observed again after one accepted launch → `DISPATCH_DUPLICATE_IGNORED`; no replay.
- `V1-N17`: runtime host/auth/WIP/writer permission changed after prompt preparation → `LOCAL_RUNTIME_BLOCKED`; preserve decision receipt but do not execute until CHAT issues the permitted recovery/retry.
- `V1-P01`: exact Library-published BRD, source mirror where necessary, scoped Owner technical delegation, isolated Copilot/Codex WPs, frozen contract, measured tests and appropriately reviewed integration → eligible for Owner-authorized integration decision only.

### C6B. Agent Result Contract v2 — mandatory contents and source-of-truth semantics (Owner 2026-10-12)

**Purpose:** CHAT must be able to reconstruct the exact task, actual actions, results, limits, test evidence and next-step gates from **Git alone**, without consulting an Agent's private conversation. Carried forward from V1.3: effective for **newly dispatched or re-scoped FOX2 WPs**; Result Contract v2 remains unchanged. Pre-existing submitted V1 work retains its historical receipt and may be reviewed with a clearly documented compatibility exception; do not silently retroactively label it noncompliant or accepted.

Each submission has exactly two mandatory human/machine entrypoints on its **task-owned Git branch**, plus narrow evidence attachments as needed:

1. `reports/<WP_ID>/report.md`: **human-readable executive result and decision request**; concise, usually 1–3 pages excluding evidence links.
2. `reports/<WP_ID>/evidence_manifest.json`: **machine-readable Agent Result Contract v2**, validated against `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json` (same released schema copy under FOX2 Library `/Trading/FOX2/07_Agent_Handoff/`). Do **not** silently accept legacy schema v1 for a new V1.8.1 WP.
3. `reports/<WP_ID>/evidence/**`: only sanitized, necessary outputs (logs, diffs, screenshots, test summaries, fixtures or validation artifacts); every cited file must be within a pinned Git commit and declared with `path + SHA-256 + claim/test/acceptance ID`. Large/raw data and secrets remain outside Git, with an approved **non-sensitive metadata pointer** only if allowed.

**Report sections that the Agent MUST fill (use `NOT_VERIFIED`, `NOT_RUN`, `NOT_APPLICABLE`, or `BLOCKED` truthfully rather than omit required sections):**

| ID | Required contents | CHAT checks |
|---|---|---|
| `R01` | **Identity:** project, task/WP/change IDs, submission version/time in UTC, Agent product, observed model/mode/host and source of any quota/usage readings | Same assigned WP; model/quota not invented |
| `R02` | **Authority and routing:** effective Policy version + SHA; `POLICY_CHECK`, `TASK_STATE_CHECK`, R0–R7, exact source channel, actual task-scope grants and STOP disposition | Owner/policy/source/grant evidence vs claimed actions |
| `R03` | **Pinned inputs:** full base commit, exact task and source-manifest paths and SHA-256, released BRD/contract revisions, dependencies and prior evidence reused or invalidated | No Candidate masquerading as Released; no stale source |
| `R04` | **Requested vs done:** brief task goal, deliverables requested, completed, partial, deferred, skipped, reasons, explicit exclusions and exact remaining work | No claim that partially completed = DONE |
| `R05` | **Change inventory:** every created/modified/deleted path, change intent, before/after SHA if available, whether within allowlist, WIP collision/worktree/lease evidence | Compare Git tree/diff, protected paths, no collateral edits |
| `R06` | **Tests and quality:** command/tool + environment + input/time window + actual execution timestamp + `PASS/FAIL/BLOCKED/NOT_RUN`, separate positive/negative IDs, repeatability and evidence references | No synthetic PASS; risk-based required coverage |
| `R07` | **Requirement/acceptance matrix:** each assigned requirement/acceptance ID → `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE`, concrete evidence IDs, deviations | PASS evidence resolves, nothing missing |
| `R08` | **Evidence index:** stable evidence IDs, relative sanitized path, SHA-256, time/provenance, claim/test links, what was actually observed vs interpreted | Every decisive claim traceable to bytes |
| `R09` | **Git delivery:** repository, task branch, original approved base SHA, current observed HEAD, push status, PR link if available, actual full remote commit SHA in external handoff receipt | Agent's local commit ≠ remote push; no main/direct merge |
| `R10` | **Risks/blockers:** severity, impact, factual reason, unresolved dependencies, source/data licensing, security scan/redaction and STOP triggers | Fail closed only affected gate, preserve WIP |
| `R11` | **Resource record:** attempts/retries, observed token/credit usage if exposed or `NOT_MEASURED`, selected model/mode and any escalation reason | No invented cost/quotas |
| `R12` | **Conclusion/next actor:** `READY_FOR_CHAT_REVIEW`, `PARTIAL`, `BLOCKED`, `LOCAL_ONLY` (Agent cannot say `ACCEPTED`); exact next action, proposed owner, prerequisites and decision requested from CHAT | Actionable without Agent conversation |

**Per-WP risk overlays:** A document/sync WP must include Library source ID/revision/hash ↔ exact Git path/blob/commit SHA matrix, readback status and CRLF/byte checks. A read-only/data WP includes source provenance, as-of/first-available time, coverage, rights/retention and `NOT_VERIFIED` for untested feeds. A DEV WP includes file diff, build/tests and dependency closure; finance/broker-sensitive work adds adversarial/safety evidence. Do not bulk collect irrelevant fields merely to satisfy formality.

### C6C. Machine Result Manifest v2 — schema, proof and anti-self-reference

- `evidence_manifest.json` must carry version, task/source/policy binding, executing Agent identity, scoped grants, start/end timestamps, requested/done/not-done work, changed paths, required test and acceptance matrices, evidence pointers/hashes, blockers, security attestation, resource measurement, delivery status and next-step proposal. Exact field types/conditional requirements are defined by `FOX2_AGENT_RESULT_SCHEMA_v2.json`. Validate syntax/schema and cross-field rules **before** claiming readiness; schema PASS is not functional test PASS.
- `submission_state` represents **Agent's delivery claim only**: `READY_FOR_CHAT_REVIEW | PARTIAL | BLOCKED | LOCAL_ONLY`. An Agent **must not** write `ACCEPTED`, `REVIEWED`, `MERGED`, `RELEASED` or mark its own gates as passed by reviewer. CHAT decision lives in **a separate reviewer-owned** `reports/<WP_ID>/chat_review_receipt.json` or authorized PR review/comment, tied to the observed immutable submission commit and reviewer identity.
- **Git commit self-reference rule:** an in-commit manifest cannot reliably embed the SHA of its own containing commit. Store **approved base commit, source commit and branch** in the manifest; after push, the **host-returned remote commit SHA** is supplied in the final Agent chat pointer, PR metadata or a separately authorized delivery receipt, never guessed or written recursively into the same commit. CHAT independently resolves remote branch/PR to its immutable full SHA and performs readback. Source `sha256` and evidence file `sha256` are hashes of actual **raw bytes**, not timestamps or only prose claims.
- A result has `BRANCH_PUSH_VERIFIED` only if actual remote ref at a full commit is observed and its manifest/report paths read back; a local commit, issue, chat message, Git blob or draft PR without required report bytes cannot substitute. PR creation is useful navigation, not automatic acceptance.
- The Git report folder is the **durable data record**. CHAT's own review receipt must preserve submitted commit SHA, review timestamp, reviewed evidence IDs, acceptance decisions, reviewer/authority and unresolved gates; no unverified acceptance on a moving branch.

### C6D. CHAT intake protocol — deterministic review gates and dispositions

On receiving only a `repo + branch/PR + full remote commit` pointer, CHAT performs the following **in order**, reusing valid source evidence and reviewing only relevant changes:

1. **Resolve immutable submission**: verify repository/branch/PR/commit ancestry, exact WP ownership and observed Git ref; fetch `report.md`, `evidence_manifest.json` and relevant evidence from that commit. Missing/unavailable artifacts → `SUBMISSION_INCOMPLETE`, not ACCEPTED.
2. **Validate contract**: parse JSON, validate v2 schema, report/manifest consistency, timestamps and source hash, pinned policy/version and current scope; classify `SOURCE_STALE`, `CONTRACT_INVALID`, `NEEDS_MORE_EVIDENCE` or eligible for deeper checks.
3. **Reconcile actual diff/permission**: independently diff approved base vs submitted commit, compare **every** changed path to allowlist and task grant, check worktree/writer/branch status, protected mirror areas, sensitive data and WIP collisions; report-only rights never permit code edits.
4. **Trace evidence to claims**: verify attached evidence paths and SHA-256 at **submission commit** and link every material PASS to requirement/acceptance/test IDs and actual command/time/environment. A test that did not run stays `NOT_RUN`, and a local simulation is not proof of platform enforcement.
5. **Assess completeness and safety**: check requested/done/missing, residual risk, data licensing/provenance, negative controls, failed tests and dependency invalidation. Partial evidence may yield a useful accepted **sub-result**, but does not close the full WP.
6. **Record independent decision**: `ACCEPTED | ACCEPTED_PARTIAL | REWORK | BLOCKED` with exact checked commit, covered IDs, reviewer, reasoning, evidence IDs, remaining blockers and next Actor. Save separately via an authorized Git report update/PR review. `ACCEPTED` is not merge/DEV/Production/LIVE permission.

**Stop and failure contract:** wrong Git source/policy or authority, missing report/manifest, mismatched SHA, modified prohibited path, leaked secret/private-account/licensed DNSE raw feed, false PASS, stale acceptance, forged/unknown actor, unverifiable remote push, Agent self-acceptance or source race → stop affected intake with specific error and recommended recovery. Where network/tool access prevents CHAT's readback, record `REVIEW_BLOCKED_GIT_ACCESS`; do not fall back to trusting pasted results as Git acceptance.

**Minimum reception negative tests (design checklist until actually exercised):** `RESULT-N01` missing manifest; `N02` mismatched WP/policy/source; `N03` evidence link to absent/mismatched blob; `N04` PASS with NOT_RUN/no command or time; `N05` report-only branch includes runtime edits; `N06` Agent writes ACCEPTED; `N07` delivery claims remote commit inside itself or relies only on local commit; `N08` unverified/shifted branch SHA; `N09` secret/license breach; `N10` report and JSON disagree; `N11` partially completed WP marked done; `N12` tests were simulations but described as external enforcement. Each must be classified `BLOCKED/REWORK/NOT_VERIFIED` appropriately; never fabricate a test run.

### C6E. Compatibility, efficiency and no-overwrite rules

- v1 schema/reports remain accessible as **legacy evidence**; do not rewrite existing immutable submissions, PRs or policy files just to make them look v2-compliant. For new work, v2 is mandatory. A carried-over in-progress WP may use a CHAT-authored scoped transition receipt with explicitly marked missing v2 fields; no implicit PASS.
- **Minimal payload** is one clear Markdown result, one manifest JSON and small linked evidence; no 100-page transcript, duplicate raw logs or noisy full screenshots. Reuse previously verified checks only while source/hash/conditions remain stable. Archive/cleanup/migration outside FOX2 is not implied.
- WORK retains its authorized CHAT/Library/connected-source capabilities under C1A. COPILOT/CODEX receive Git/local snapshots only; all must use the same result-contract obligations when delivering WPs through Git, adjusted only for actual available interfaces and safety rights.

### C6F. Agent Result Delivery Assurance & mandatory Policy Binding (Owner 2026-10-12)

**Purpose and precedence:** Prevent an Agent reporting "DONE" locally while CHAT cannot locate verified work on Git. This clause adds deterministic delivery gating to the existing **one** FOX2 Policy family. It does **not** replace Result Contract/schema v2, create a second policy, grant DEV/report-push, or retroactively invalidate immutable previous tasks/results. CHAT owns task metadata, delivery destination, receipt intake and review decision. Agent retains only separately verified task-scoped Git privileges.

#### C6F.0 — Mandatory Policy Binding in every new/re-scoped Agent task and prompt

Before issuing a task, CHAT records and verifies these **exact, non-optional** fields in `docs/agent_handoff/<WP_ID>/task.md` **and** `source_manifest.json` (or a clearly linked immutable re-scope supplement): `project=FOX2`, `policy_id=FOX2-POLICY-V1`, `policy_version`, `policy_raw_sha256`, `policy_library_release_manifest`, `policy_git_repository`, `policy_git_path`, `policy_git_commit_full_sha`, `effective_status=RELEASED_EFFECTIVE`, `result_contract_version=2.0`, `result_protocol_version`, `task_source_commit_full_sha`, and `GIT_SOURCE_READY=YES|NO` with matching source receipt. All commits are full 40-hex identities. The task itself is located by a separate **CHAT-observed remote commit pointer** after publication, avoiding self-referential commit fields. Do not use `latest`, branch HEAD alone, Memory, chat summaries, or a legacy task file as binding proof.

The receiver MUST read Policy and release manifest from the frozen Git commit and recompute raw SHA-256; compare the pinned binding against the canonical Library release receipt and the current CHAT-approved task. On mismatch, stale revision, missing release manifest, or incompatible material policy change, return `BLOCKED_POLICY_MISMATCH` / `POLICY_REVALIDATION_REQUIRED` **without proceeding into the affected task**. If a newer Policy appears during execution, CHAT evaluates its impact, preserves the old task's evidence and either issues a scoped transition or expressly records why the old binding remains valid for the in-flight scope. Agents never self-promote to a new policy revision.

#### C6F.1 — CHAT-owned deterministic destination

Each new/re-scoped WP records a single `result_destination` in its authorized task: `repository`, `wp_id`, `tracking_issue_url_or_number`, `task_branch`, `task_git_commit`, `agent_result_branch` (one writer), `approved_base_commit`, `report_path=reports/<WP_ID>/report.md`, `manifest_path=reports/<WP_ID>/evidence_manifest.json`, `evidence_dir=reports/<WP_ID>/evidence/`, `report_schema_path=docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`, `git_report_write_grant`, `git_report_push_grant`, `pr_create_grant`, `result_receipt_required=true`, `chat_remote_readback_required=true`, `stop_conditions`. The Agent may not invent alternate target folders, filenames, shared mutable result indexes, or substitute a private chat/local folder for Git. A fixed naming convention is **not** a permission grant.

The **GitHub Issue/WP ID is the discovery locator**, not the evidence store. Immutable source-of-truth for the Agent result is the remote repo/branch/**full commit** plus report/manifest/evidence files. CHAT's review is independent and can be recorded in an authorized separate reviewer-owned receipt or PR review. No need for all Agents to edit one global status file. Version subsequent submissions by commits, not `final-final-v2` filenames.

#### C6F.2 — Pre-dispatch delivery-path gate and authority isolation

CHAT records `REPORT_DELIVERY_PATH_PREPARED=YES` when (a) Policy/source pins are released and remote-readback verified, (b) a WP-specific task and deterministic destination are published at a full Git commit, (c) **either** an explicit WP-scoped grant **or the reusable C6F.2A standing Copilot report authorization** applies to the actual reporter, (d) the final receipt/failure path and unique task branch/workspace plan are defined, and (e) a tracking Issue identifies the WP. Ephemeral host facts such as current Git authentication, branch ancestry/head, WIP collision and writer ownership may be satisfied by the C1.1 **Local Runtime Attestation** immediately before Agent launch rather than being redundantly re-evaluated by CHAT and then by the Bridge. `REPORT_DELIVERY_PATH_READY=YES` exists only after the required runtime facts are attested (by CHAT if already observed or by the Bridge at launch). **Standing authorization eliminates repeated OWNER GRANT per Copilot WP; it does not eliminate runtime safety attestation.** Otherwise execution remains `DELIVERY_SETUP_PENDING` or `LOCAL_RUNTIME_BLOCKED` as applicable.

`GIT_SOURCE_READY=YES` and `REPORT_DELIVERY_PATH_READY=YES` are independent; neither grants `CODE_ALLOWED`, `GIT_CODE_PUSH`, `main` push, merge, provider rights, broker write or LIVE. Unknown or revoked Git identity/access, writer/worktree state, or task/source binding blocks the affected push; **do not mistake a document authorization for enforced GitHub filesystem/path permissions**.

#### C6F.2A — Standing Copilot Result Publisher (Owner-approved, FOX2-only)

**Owner decision 2026-10-12:** grant **once**, for FOX2 and only the **GitHub Copilot Pro reporter role actually operating on the authorized FOX2 Windows host** (initial candidate `FoxLe-PC`), a **reusable internal permission** to author and push **report/evidence files** for every properly registered, source-bound FOX2 WP. No repeated CHAT/Owner per-WP report approval is required, including for current Issue #5/P1, so long as all conditions below pass. This is **not** a grant to arbitrary Git identities, CODEX, WORK, other projects, or unauthorized hosts. Owner can revoke/change this standing authorization at any time and CHAT must record revocation; a policy/version supersession requires revalidation as specified by C6F.0.

- **Default root:** `reports/`, with **one deterministic child** per WP: `reports/<WP_ID>/report.md`, `reports/<WP_ID>/evidence_manifest.json`, optionally `reports/<WP_ID>/evidence/**` (only saved sanitized proof). The canonical Git result remains schema **v2**, unchanged. Do not write one shared mutable report for different WPs, and do not write outside this subtree.
- **Branch:** one designated non-main `work/<WP_ID>-copilot` branch per WP (not one shared branch across Agents); CHAT publishes branch name/source pointer in each task, but a **new grant is unnecessary** for an eligible WP. One writer per branch/worktree; old submissions immutable by pinned commit.
- **Reusable authorization:** `GIT_REPORT_WRITE=AUTHORIZED_BY_STANDING_C6F_2A` and `GIT_REPORT_PUSH=AUTHORIZED_BY_STANDING_C6F_2A`. `GIT_SOURCE_READ` remains subject to actual Git access; issue comments and `PR_CREATE` are independently permitted only if task/host capability or existing authorized role permits them. Absence of PR rights does not prevent valid report-only Git submission with remote pointer.
- **Required real-world technical verification:** correct repo/remote, Copilot host/login, non-destructive auth/access check (no token disclosure), remote branch ancestry/expected head, exclusive writer and clean task-local changes, no excluded secrets/licensed raw DNSE data, allowed-path-only staged diff. Record model/mode/quota when exposed; report `NOT_EXPOSED` rather than fabricate. If any of these fail, preserve WIP and return `PUSH_BLOCKED/LOCAL_ONLY`, not `PUSHED_UNREVIEWED`.
- **No GitHub path ACL claim:** GitHub repo-wide write permissions can technically reach non-report paths. A prompt or standing FOX2 Policy is a procedural **allowlist, not a GitHub-enforced path restriction**. Until provider-level rulesets/branch protection or a separately restricted report repository / verified CI guard actually enforce this boundary, independent CHAT diff check and no merge remain mandatory. Never label guardrails `ENFORCED` without testing them. If production-grade path enforcement becomes necessary, authorize and test an appropriate technical control separately.
- **Hard denial for this role:** `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `MAIN_PUSH=NO`, `MERGE_ALLOWED=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO`, no other repo/file changes, no force-push, reset, rebase, credential exfiltration or silent WIP cleanup.
- **Receipt/acceptance:** after each actual push, Agent returns `FOX2_AGENT_DELIVERY_RECEIPT` with **result** remote SHA; CHAT independently reads both required files and schema/evidence from that SHA, sets `RESULT_DELIVERY_VERIFIED`, then separately decides acceptance. Standing authorization never self-accepts a result or closes an Issue.

This authorization was activated under V1.7.1 and is **carried forward unchanged by V1.8.1**; current WPs bind to the effective V1.8.1 Policy after its Library release and exact Git Policy readback. Historical P1 execution remains owner-reported and its missing evidence remains missing. It allows result publication without repeating owner grant; it does **not** validate an unobserved Copilot identity or retroactively certify P1.

#### C6F.3 — Mandatory end-of-execution delivery receipt

Every Agent **must reply** with a short externally observed `FOX2_AGENT_DELIVERY_RECEIPT` containing `WP_ID`, `ACTUAL_AGENT_MODEL_HOST`, `POLICY_VERSION_SHA_AND_COMMIT`, `TASK_COMMIT`, `SOURCE_COMMIT`, `EXECUTION_STATUS`, `DELIVERY_STATUS`, `REPO`, `BRANCH`, `REMOTE_COMMIT_SHA_OR_NONE`, `PR_URL_OR_NONE`, `REPORT_PATH`, `MANIFEST_PATH`, `EVIDENCE_COUNT`, `REMOTE_READBACK_STATUS`, `REPORT_WRITE/PUSH_GRANT_STATUS`, `CODE_ALLOWED`, `OPEN_BLOCKERS`, `NEXT_ACTOR/ACTION`. Allowed operational delivery statuses: `PUSHED_UNREVIEWED`, `PUSH_BLOCKED`, `PUSH_FAILED`, `LOCAL_ONLY`, `SUBMISSION_INCOMPLETE`, `SOURCE_BLOCKED`. The required committed schema-v2 manifest retains its own schema enumerations; map more detailed receipt-only failure statuses to schema v2 without inventing new JSON fields or states.

A local commit, saved file or message "done" is not a pushed result. If report push is not authorized or fails, the Agent reports exact error/observed facts, keeps work intact and returns `REMOTE_COMMIT_SHA=NONE` for the result (source SHA remains separately stated). Do not claim Git delivery; do not send secrets or copied raw provider data in the chat fallback. CHAT takes ownership of the permitted recovery route; do not rerun completed P1 merely because delivery is missing.

#### C6F.4 — CHAT delivery acknowledgement precedes acceptance

After receiving the pointer, CHAT resolves the **full immutable result commit** and exact WP/branch/PR ancestry, reads `report.md` plus `evidence_manifest.json` from that **same commit**, validates schema v2, recomputes material evidence/raw hashes, compares result diff/allowlist/grants and source/policy binding, and independently sets `RESULT_DELIVERY_VERIFIED=YES|NO` in an authorized CHAT-owned receipt/comment. The receipt binds the submitted commit, reporter, verification time, file paths/hashes and failure reason. `NO` yields `DELIVERY_PENDING`, `SUBMISSION_INCOMPLETE`, `DELIVERY_INVALID`, `PUSH_BLOCKED` or a precise access failure; never ACCEPTED. `YES` only confirms that CHAT received a valid inspectable delivery; the **separate** C6D evaluation decides `ACCEPTED | ACCEPTED_PARTIAL | REWORK | BLOCKED`.

No issue creation, notification, CI PASS, self-attestation, PR URL, or receipt text alone proves remote byte delivery. Any future GitHub Actions validation is supplementary and must be configured/tested independently; it is **not claimed to be installed or enforced** by this release.

#### C6F.5 — Closed-loop discovery, failure and historical transition

A WP cannot close based solely on `EXECUTION_DONE`; a missing result remains visible at its tracking Issue until the independent CHAT acknowledgement/review is recorded. CHAT checks result state when an Agent declares completion or submits a receipt; no continuous background monitoring is implied without an actual authorized automation. On missing report or unauthorized push, CHAT provides exact allowed remediation (grant, scoped publisher or evidence-only recovery). Preserve existing results, WIP, prior commits and prior decisions. An inherited P1 task pinned to obsolete Policy V1.2 remains **historical only**; reuse the already-published V1.6 transition history, then bind any new result handoff to the effective V1.8.1 Policy and a verified task/receipt before re-contacting Copilot. Do not backdate or silently rewrite the old record.

#### C6F.6 — Dispatch STOP / release boundary

No Local Agent execution may start until the stable C1 decision gates for the exact WP revision are recorded PASS and, after Owner selection, C5B `LOCAL_RUNTIME_ATTESTATION` passes. **Do not repeat the completed Policy/task/routing/assignment decision evaluation inside the Bridge.** Recheck only runtime facts that can materially change between prompt preparation and launch. Report-only tasks may use the standing Copilot reporter authorization of C6F.2A when applicable; other reporters require their scoped grant. No policy change creates Git branch protection, production credentials, merge entitlement or scheduled monitoring. STOP on unverified/mismatched policy or dispatch SHA, bad task source, missing destination, writer conflict, outside-scope mutation, unsafe content or denied platform action; never evade platform controls.

---

# D. RELEASE CONTROL AND INTERPRETATION

## D1. Effective policy boundary

This consolidated FOX2 Policy V1.8.1 controls FOX2 internal document governance and Git-first work-package routing on and after a successful Owner-authorized Library write/readback with a verifiable release manifest. Section A controls authority and safety, Section B controls BRD lifecycle, and Section C controls Agent prompt routing and Work Packages. No standalone draft creates a second competing FOX2 policy.

## D2. Historical source and release evidence

The publication manifest, stored alongside the released policy, must bind the actual V1.8.1 file ID/path/size/SHA-256, parent V1.8 lineage/hash, the retained reusable Copilot report-only decision, the staged Execution Routing Selector decision, and the observed readback. Previous draft snapshots are retained solely as provenance and must not override the exact released Policy. Publication metadata is evidence of the document transaction, not proof of reviewer independence, host credentials, Git permissions or operational code release.

## D3. Explicit limits of this publication

- Owner has the highest authority for FOX2 internal decisions and can delegate document and technical responsibility; actual platform operations must still succeed under verified access.
- No cross-project documents, permissions or release checkpoints apply automatically. Existing separate workflows remain unchanged.
- `CODE_ALLOWED=NO` for policy publication; no Git merge, release of code, broker connection/order-write or LIVE is authorized by this document.
- Any later change to this V1.8.1 requires a new frozen source, accountable Owner decision, actual Library write/readback and supersession evidence under A7.
- Agent product/model/mode/quota and current Git ownership remain `UNKNOWN` until actually checked for the relevant handoff; do not infer readiness from this release.

## D4. Routing disposition for document publication

`POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK` applies to executable handoffs. This V1.8.1 policy publication is an L0 document operation: CHAT or an expressly Owner-assigned Publisher such as WORK performs the actual Library write/readback and source verification; COPILOT has an Owner-internal standing report-only authorization **subject to separate actual Git capability checks**, not an unconditional executable dispatch; CODEX is not assigned coding or Git push tasks by this release; WORK retains full access when actually available and has no discretionary extra audit assignment. Current technical entitlements are not presumed. Stop before any DEV/Git/LIVE activity without a separate scoped authority and evidence.

## D5. V1.6 result-delivery rollout checkpoint — distinct from effective document Policy

- `POLICY_V1.6_PUBLICATION`: PASS only when Library upload, exact-byte readback and manifest are observed.
- `GIT_FIRST_ROUTING_DESIGN_AND_RESULT_CONTRACT`: ADOPTED with Owner decision, but `GIT_HANDOFF_MIRROR=VERIFIED_ONLY_FOR_EXACT_SCOPED_BRANCH_AND_COMMIT` when remote readback and grants are demonstrated.
- `TASK_RESULT_PUSH`: NOT_GRANTED until actual Agent host/credential, task branch and scoped grant verification.
- `M1_V04_MIRROR`: 8/8 released source files + 2 companion files verified at source commit `1e1972cb204ac780e68878c34f6a59d205bdb18c` on `work/FOX2-M1-V04-SOURCE-RECOVERY-chat-20261012`; source/review receipt finalized at `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`. This is YES **on that branch/commit only**, not on main; no runtime or DEV readiness follows.
- `FOX2_M1_0_WINDOWS_PREFLIGHT`: Copilot execution claimed externally; no pinned result report/manifest on Git yet. `RESULT_DELIVERY_VERIFIED=NO`; historical V1.2 task retained but superseded by a separately published V1.6 result-recovery task only after its Git readback.
- `CODE_ALLOWED=NO`, `GIT_DOCUMENT_WRITE/PUSH=ONLY_IF_SEPARATELY_OWNER_GRANTED_AND_VERIFIED`, `MERGE=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO` **for this L0 policy-publication task only**. Future separately authorized scoped report pushes may be allowed while code remains prohibited.

- `GIT_SOURCE_READY`: YES only for the WP-specific required source set after real remote publication/readback; failed upload keeps the dependent implementation SOURCE_PENDING.
- `AGENT_RESULT_CONTRACT_V2`: carried forward unchanged from V1.3 and mandatory for new authorized Git-first WPs; schema/template review design validation is **not** remote Agent execution or CHAT acceptance.
- Existing draft Git PRs and previously submitted evidence retain actual independent review status; V1.6 does not retroactively grant push or merge. `REPORT_DELIVERY_PATH_READY` and `RESULT_DELIVERY_VERIFIED` must be evidenced separately.

## D6. V1.7.1 reusable-report authorization checkpoint (V1.7.0 integrity erratum)

- `POLICY_V1.7.1_PUBLICATION`: only PASS after published Library raw-byte readback and release manifest; Git mirror must be checked at its own pinned remote commit.
- `STANDING_COPILOT_REPORT_AUTHORIZATION`: **OWNER_APPROVED** for future registered FOX2 WPs at `reports/<WP_ID>/**` on one non-main Copilot branch per WP. No repeated WP-specific approval when C6F.2A applies.
- `COPILOT_TECHNICAL_ACCESS` / `EXCLUSIVE_WRITER`: **UNKNOWN** until actually checked on the Windows host/identity. No automatic push task completion or remote result.
- `GITHUB_PATH_ACL_ENFORCEMENT`: **NOT_VERIFIED / NOT_CLAIMED**. Private-repository Rulesets API returned `403` while evaluating availability on 2026-10-12; no bypass, plan-upgrade or public-repository conversion is authorized. Do not infer GitHub path protections from this internal Policy.
- `P1_RESULT_DELIVERY`: still `PUSH_BLOCKED/NOT_VERIFIED` pending actual Copilot host and result commit; Issues/PRs remain open; P1 tests are not retroactively PASS.
- For this Policy document operation: `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `MAIN_PUSH=NO`, `MERGE_ALLOWED=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO`.


## D7. V1.8 Local Agent dispatch checkpoint

- `AGENT_PROMPT_POLICY_DECISION_CHECKS`: **SINGLE-PASS** for the exact immutable WP revision; Bridge cannot duplicate or override them.
- `LOCAL_DISPATCH_SELECTION`: Owner-selected `EXECUTE_LOCAL_AGENT` is required before CHAT publishes an executable dispatch artifact; `SAVE_PROMPT_ONLY` produces no dispatch.
- `DISPATCH_TRANSPORT`: Git append-only `docs/agent_handoff/<WP_ID>/dispatch/<DISPATCH_ID>.json`, schema v1, `max_runs=1`, bound to exact task/prompt/policy/source identities.
- `BRIDGE_RUNTIME_ROLE`: runtime attestation + CLI invocation only; no BRD/Policy/routing reinterpretation, no self-grant, no main/merge/deploy.
- `RESULT_CONTRACT_V2`: unchanged; all result publication and independent CHAT acceptance controls remain in force.
- `UI_BUTTON_STATUS`: Policy defines the selection semantic. A visual one-click button/quick action is used only when the current ChatGPT client/integration technically exposes it; otherwise the exact action selection text is equivalent and CHAT still performs the Git dispatch operation.

## D8. V1.8.1 Execution Routing Selector checkpoint

- `EXECUTION_ROUTING_UI`: preferred interactive form is one single-select radio group plus explicit confirmation CTA per screen; preselection is not approval. Equivalent explicit-confirmation text fallback is permitted when native UI is unavailable.
- `SCREEN_1_EXECUTION_PATH`: exactly `MANUAL_VSCODE` or `CONFIGURE_AUTOMATED_AGENT`. Confirmed `MANUAL_VSCODE` terminates `END_NO_BRIDGE`; no `SAVE_PROMPT_ONLY` option exists.
- `SCREEN_2_AGENT_CONFIGURATION`: Owner confirms one explicit Agent/Model/Thinking-or-Optimize configuration after CHAT shows a recommendation and eligible alternatives. No `SAVE_CONFIGURATION_ONLY` option exists.
- `SCREEN_3_TRANSPORT`: exactly `DISPATCH_VIA_LOCAL_BRIDGE`, `BACK_TO_AGENT_CONFIGURATION`, or `CANCEL_EXECUTION`; only confirmed Bridge transport creates a dispatch.
- `DISPATCH_SCHEMA`: `FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v1.1.json`; dispatch binds the Owner-confirmed Agent configuration and the three-stage selection receipt. Bridge may not silently substitute Agent/model/mode.
- `AGENT_PROMPT_POLICY_DECISION_CHECKS`: remain **SINGLE-PASS** for the exact immutable WP revision. Bridge performs runtime attestation only.
- `RESULT_CONTRACT_V2`: unchanged; result publication and independent CHAT acceptance controls remain in force.
