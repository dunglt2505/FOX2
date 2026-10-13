# FOX2 — POLICY V1.8.3 | GOVERNANCE-ONLY CONSOLIDATED

**Document ID:** `FOX2-POLICY-V1`  
**Version:** `1.8.3`  
**Release source:** Owner direct instruction 2026-10-13 — CHAT-FIRST Agent allocation routing delta. Supersedes V1.8.2 only after verified official release.  
**Applicability:** `FOX2 ONLY`  
**Release date:** 2026-10-13 (Asia/Ho_Chi_Minh)  
**Document authority:** FOX2 Owner; CHAT acts as delegated Library document operator for this Owner-authorized routing release only.  
**Change / supersession:** `FOX2-CHAT-FIRST-ROUTING-20261013`, bounded routing responsibility update to C1A/C2/C2A.7/C5 and A3. No rewrite of previously released policies, BRDs or technical specs and no execution authorization. Bridge Technical Spec v0.4 remains released/effective, independent of this policy revision. Preserves all prior FOX2 V1.8.2 invariants and gates.
**Status:** `RELEASED_EFFECTIVE`, contingent on verified release receipt for this exact V1.8.3 artifact. Owner explicitly requested "publish Policy, các tài liệu liên quan hết luôn" on 2026-10-13.
**Parent effective Policy:** `FOX2_POLICY_V1.8.2.md` — Library raw SHA-256 `552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc`, historical after V1.8.3 publication.
**Release verification:** This release is authoritative only at the protected FOX2 Governance Library path after successful upload, exact-byte readback and release-manifest verification. Candidate copies remain immutable historical inputs only.  
**Exclusions:** This release does not grant DEV, Git write, Bridge dispatch, merge, Production API/broker, deployment or LIVE rights. This release consolidates (1) Execution Routing Selector authority/confirmation semantics, (2) BRD/Policy governance-provenance clarification, (3) closed-loop review authority/state semantics, and (4) explicit Policy ↔ Technical separation. Branch topology, polling, local ledger, process supervision, Git command sequence, queue plumbing, crash recovery and similar implementation details are **not Policy** and belong in the Technical Specification.

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
8. Copilot is initially considered for Windows/IDE/local Git checkout and actual programming, frontend, dashboard, routine APIs/backend, offline fixtures and ordinary tests; remote GitHub metadata, release verification, Git source readback and task/Issue maintenance are done by CHAT directly when its existing connector is capable. Codex is initially considered for domain core, nontrivial backend/data invariants, quantitative/risk algorithms, concurrency and difficult integration. CHAT owns decomposition and routing; independent reviewer involvement is risk-based or expressly Owner-directed, and cannot create an unapproved blanket veto. Agent assignments are never automatic based only on labels.
9. Protect concurrent development with **one writer per exact file/worktree target**, verified non-overlapping paths, separate worktrees and branches, frozen shared API contract, own unit tests and Owner-approved scoped integration.
10. Keep **FOX2 localhost V0.1 offline/read-only** as first permitted *design target*, not an authorized build: synthetic fixtures must be labeled; no broker/order-write, margin, unattended trading, unrestricted data access, external secrets or LIVE by implication.
11. Preserve **C2A — Model, Thinking & Token/Credit Optimization**: verify actual product/model/mode/quota, use minimum sufficient reasoning, reuse relevant evidence, control context and retries, and optimize cost per safely accepted outcome. The 70/30 ratio is a target, not a forced gate.
12. **Owner clarification 2026-10-12 — source-access routing:** CHAT validates ChatGPT Trading Library; COPILOT/CODEX receive applicable documents through Git/local snapshots; **WORK is permitted to use CHAT conversation/project context and ChatGPT Trading Library/other existing connected sources to the extent these are actually available in WORK**, with no artificial reduction of its existing access or execution role. Access permissions and tool capability remain distinct facts.
13. **Owner upgrade 2026-10-12 — Git-first operational loop:** FOX2 Git is the canonical *operational* record for work-package assignment, versioned implementation, sanitized tests/evidence, Agent report, CHAT review and handoff. Agents submit results through a task-scoped **branch push + PR/commit receipt** after actual Git capability, source and scoped write grants are verified. Library remains the authority for **issued Policy/BRD**; Git does not publish/promote them by itself. Direct pushes or merges to `main` by an implementing Agent are not authorized by this policy.
14. **Owner upgrade 2026-10-12 — one-action Local Agent dispatch:** after CHAT has completed and recorded the Agent Prompt Policy checks for an executable WP, CHAT presents an execution selection. Owner selection `EXECUTE_LOCAL_AGENT` authorizes CHAT to publish one immutable, task-bound dispatch artifact to FOX2 Git. The Local Bridge consumes that artifact and performs only runtime attestation; it must not repeat or override the completed Policy/task/routing/assignment decision checks. No selection means no local execution.
15. **Owner refinement 2026-10-12 — staged Execution Routing Selector:** after an executable prompt is ready, CHAT first offers the terminal manual-VS-Code path versus automated-Agent configuration; only the automated path opens Agent/Model/Thinking selection, and only after that configuration is explicitly confirmed does CHAT ask whether to dispatch through the Local Bridge. `SAVE_PROMPT_ONLY` and `SAVE_CONFIGURATION_ONLY` are removed. A preselected radio option is a recommendation only; explicit confirmation is required at each decision screen.
16. **Owner refinement 2026-10-12 — closed-loop result review:** after an Agent result is actually pushed and the remote full commit SHA is independently verified, FOX2 may emit a durable `REVIEW_READY` event and use configured automation to trigger CHAT independent review without requiring a new Owner message for that same result. The trigger, GitHub Action, Issue/label queue or scheduler is never acceptance authority; CHAT reviews the exact immutable result SHA and records a separate review receipt. `REWORK` does not auto-dispatch another Agent, and `ACCEPTED` does not auto-merge or deploy.
17. **Owner clarification 2026-10-12 — Policy/BRD/Technical separation:** Policy governs authority, rights, mandatory invariants, required evidence classes, state/verdict semantics and STOP/release gates. BRD/Data Contract/Acceptance own business and functional requirements. Technical Specifications own implementation mechanisms and may version independently. Technical text cannot create authority, redefine BRD requirements or weaken Policy; Policy-only changes do not mechanically version-bump BRDs or Technical Specs unless their owned semantics materially change.

---

> **Owner source-delivery clarification 2026-10-12:** CHAT owns source upload/recovery; implementation tasks stay internally SOURCE_PENDING until CHAT completes remote verification and records the single GIT_SOURCE_READY=YES decision.

> **Owner extension 2026-10-12 — Agent Result Contract v2:** every new FOX2 Git-first Agent result must contain a human report, schema-validated machine manifest, verifiable acceptance/test/evidence mapping and an independent CHAT review receipt. Detailed normative controls: C6B–C6F. The source of truth for released Policy/BRD remains Library, while Git is the operational system of record for task/results.

# A. FOX2 GOVERNANCE CORE — `FOX2-GOVERNANCE-CORE-V1`

## A1. FOX2-only scope, source precedence and supreme Owner authority

- **FOX2 is a NEW, independent project.** Its requirements, policies, permissions, folders, releases, worktrees and acceptance processes are established and governed within FOX2 only. No document, approval, release receipt, Publisher, Source Lock or worktree from another project is inherited by default.
- **No cross-project policy import.** Other-project documents are reference material only; they acquire no FOX2 governance force through shared names, storage location, historical drafts or implicit references. An actually effective external legal, contractual or platform obligation is evaluated only when its issuer and applicability to FOX2 are evidenced. This clause never purports to disable binding law or real platform permissions.
- **OWNER SUPREMACY — FOX2 internal authority:** Owner is FOX2's highest decision-maker for business, Policy, BRD, budgeting, security posture, document publication, technical architecture, choice/assignment/removal of Agents, and delegation or withdrawal of technical roles and Git/DEV/release responsibilities. An earlier or subordinate **internal FOX2 procedure** must not impose a veto over an explicit, attributable, scope-bound Owner decision. Owner may establish the inaugural FOX2 Publisher role and modify/replace any FOX2-internal review workflow, subject to the bounded real-world exception below.
- **Operational boundary:** Owner's authority to approve or delegate is not proof that CHAT (or any Agent) possesses unavailable host credentials, cloud ACLs, protected keys, platform entitlements or third-party access rights. A technical step is `COMPLETED` only after real operation + objective evidence. Legal requirements, licensed/provider terms, external protected service policies and material safety invariants cannot be bypassed by editing an internal document. If a claimed superseding external control applies, identify its exact authority and FOX2-specific scope; absent proof, do not invent a veto.
- **Conflict precedence inside FOX2:** (1) mandatory applicable external law/provider/platform access restriction; (2) latest exact, attributable FOX2 Owner decision; (3) actually published FOX2-only Policy/governance; (4) released FOX2 BRD/Data Contract/Acceptance in their owned business/functional domains; (5) released Technical Specifications in their delegated implementation domains; (6) candidates, drafts and general reference material. A Technical Specification cannot override Policy or redefine BRD-owned requirements. Preservation and audit of past decisions do not constitute an active restriction.
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

**CHAT — delegated coordinator, direct GitHub/Library operator and document Publisher when technically possible:** Under Owner's explicit FOX2 instruction, CHAT may author/revise policy, maintain a record of Owner decisions, directly read/write authorized GitHub Issue/PR/docs/branches/immutable commits and manifests through connected tools, upload documents to an actually writable Library directory, verify content/readback and write a transparent publication record. CHAT's ability to write a file is established only by a successful tool operation, not by a self-declared `protected_issuer` title. CHAT must not invent independent signatures, third-party approvals or host access.

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

- **M1 product boundary:** M1 product scope, milestone semantics, accepted business/data invariants and acceptance intent are owned by the applicable released BRD/Data Contract/Acceptance/Roadmap source set. Test fixtures remain isolated from investor runtime; M1-A foundation evidence never establishes M1-B real-data acceptance. Framework/API/storage choices belong to the applicable Technical Specification.
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
3. **Actual Publisher action:** Owner is publication decision-maker. CHAT or another expressly Owner-delegated document publisher is the operator only with observed Library upload rights. Each subsequent release is a **new, immutable version file** at `/Trading/FOX2/00_Governance/FOX2_POLICY_V<version>.md`; use the exact new version filename for the version actually being released. For this Candidate, no release filename is effective until Owner publication approval; if V1.8.2 is approved, its release file must use the V1.8.2 identity and must not retain a stale V1.8.1 release label. Preserve V1.0/V1.1; never overwrite an effective source. No external protected key is assumed to exist.
4. **Readback:** List destination, read exact uploaded source and independently compare file ID, raw bytes/SHA-256, project scope and intended label. Record observed date/time and actual operator; no backdated/imaginary issuance.
5. **Evidence:** Create an Owner-decision-linked publication manifest containing actual output ID/path/hash and status. If upload or readback fails: `PUBLICATION_INCOMPLETE`, never `EFFECTIVE`. If a real external controlled issuance gate is demonstrated, stop only that affected issuance and record the named authority/evidence.
6. **Effective classification:** Only after steps 1–5 truly complete, record `FOX2_DOCUMENT_POLICY_PUBLISHED` and `RELEASED_EFFECTIVE(scope=FOX2, internal_document_governance_only)`. This label does **not** assert a protected signature, Git sync, Agent result push, DEV, broker, margin or LIVE. Review any future changes against the latest actually published FOX2 version.

**A7.2 — Separation of business rights from observable capability:** An Owner's superior decision can remove or replace internal FOX2 procedural limits; it cannot create a real permission denied by Google Drive, Git, OS, financial-data providers or a third-party system. Technical execution is gated by actual access/evidence. A mismatch must be reported with a specific remedy rather than an imaginary Publisher PASS.

**A7.3 — Later policy releases:** Use the same frozen identity + Owner decision + real write/readback + revocation/supersession evidence. Optional independent review is risk-directed, not an absolute inherited precondition. In particular, a simple policy revision does not wait for a new Git repository or a private code-worktree before internal document publication.

---

## A8. Policy ↔ BRD ↔ Technical Specification separation — `FOX2-GOV-TECH-SEP-001`

1. **Policy owns governance.** Policy defines authority, roles, permission classes, mandatory invariants, decision gates, evidence classes, canonical state/verdict semantics, STOP conditions and release boundaries.
2. **BRD/Data Contract/Acceptance own requirements.** They define business/functional behavior, data semantics, consumer obligations and acceptance intent. Policy does not silently rewrite business requirements; Technical Specifications do not redefine them.
3. **Technical Specifications own implementation.** They define architectures, branch/worktree topology, schemas/protocol encodings, process supervision, persistence, retry/recovery, polling, queue/outbox mechanics, Git commands, operating-system isolation, observability and test harness design.
4. **Authority does not flow upward from Technical.** A Technical Specification may implement a Policy grant but cannot create DEV/Git/provider/merge/deploy/LIVE authority, waive an Owner decision, or convert `UNKNOWN/NOT_RUN/CANDIDATE` into PASS.
5. **Independent versioning.** Policy, BRD and Technical Specifications version independently. A change in one document family requires revision of another only when the owned semantics of that other family materially change. Historical cross-references are provenance unless an explicit frozen compatibility dependency is declared.
6. **Contract boundary.** Policy may require a technical capability or evidence property (for example single-use dispatch, authenticated provenance, immutable remote result, idempotent review and no silent model substitution) without prescribing its implementation. The active Technical Specification must demonstrate how those requirements are met.
7. **Conflict handling.** When Technical text conflicts with Policy or BRD, implementation stops on the affected scope and the higher-authority source is applied; Technical is corrected rather than using the conflict as authority to change governance or requirements.

---

# B. FOX2 BRD LIFECYCLE, APPROVAL & PUBLICATION POLICY — `FOX2-BRD-POLICY-V1`

## B1. Canonical BRD ownership and change contract

A requirement has **one** `BRD_ID / revision / REQUIREMENT_ID` as its canonical business owner; cross-cutting controls and dependencies are separately linked. Identified candidate BRD domains: `00` common standards; `01` capital; `02` screening/discovery; `03` portfolio risk; `04` exit/profit protection; `05` market/sector/stock analytics; `06` data foundation; `07` research/backtests; `08` localhost dashboard. These domain labels are **not proof of release**.

Each BRD Candidate records owner, version, requirements, business rationale, inputs/units, outputs, non-goals, risk, sources/freshness, consumers, source set, acceptance IDs and provenance. A material BRD change carries a **Business Change Contract (BCC)**: exact source revision and SHA-256; changed requirements; positive/negative examples; transitive affected consumers; allowed/forbidden behavior; unresolved issues; proposed stage; risk-based review when applicable and Owner decision. A UI WP cannot redefine accepted domain calculations without Owner-approved change.

### B1.1 Governance provenance vs active operational governance

**Status:** `RELEASED_EFFECTIVE` under FOX2 Policy V1.8.2. Change ID: `FOX2-B1-GOVERNANCE-PROVENANCE-CLARIFICATION-20261012`.

1. **Policy reference inside a released business/technical document is release provenance by default.** A version such as `FOX2 Policy V1.0`, `V1.8` or another exact Policy version recorded inside an approved/released BRD, Roadmap, Contract, acceptance document or technical design identifies the governance context under which that document revision was approved/published. It does **not** permanently bind every future operation to that historical Policy version unless the document explicitly declares a specific frozen dependency that is legally, contractually or technically required.
2. **Active operational governance follows the current released Policy.** Review, handoff, implementation, testing, release, dispatch and other new actions are governed by the latest actually `RELEASED_EFFECTIVE` FOX2 Policy applicable at the time of that action, subject to exact Owner decisions and any evidenced external/legal/provider constraints. A historical Policy citation in an unchanged BRD does not override newer released FOX2 governance.
3. **Policy-only updates do not automatically version-bump business documents.** A Policy revision by itself does **not** trigger a new BRD/BCC/Roadmap/Contract revision, republish cycle or Git mirror solely to replace an old Policy number. Avoid mechanical document churn such as incrementing BRD versions only because governance version changed.
4. **Material-impact trigger remains mandatory.** Create/revise the affected BRD/BCC/Roadmap/Contract only when the new Policy materially changes a document-owned business requirement, accepted risk rule, acceptance semantics, data contract, consumer behavior, source-right invariant or another canonical requirement/invariant owned by that document. The smallest complete affected dependency closure is revised; unrelated documents remain unchanged.
5. **Historical releases remain immutable evidence.** Do not rewrite previously released BRD/Roadmap/Contract bytes merely to make their embedded Policy version look current. Their historical Policy references remain valid provenance and audit evidence. If clarification is needed, use the active Policy, release/transition receipt or current task/handoff metadata rather than mutating historical source.
6. **Metadata for new/revised documents should separate the two meanings.** Prefer fields semantically equivalent to `governance_provenance_at_release=<exact Policy version/hash>` and `operational_governance=latest actually RELEASED_EFFECTIVE FOX2 Policy applicable at action time`. Avoid ambiguous wording that suggests a release-provenance Policy number is a perpetual execution dependency.
7. **Executable handoffs still require exact Policy binding.** The phrase “latest released Policy” is a governance rule, **not** sufficient binding proof for an Agent task. At every new/re-scoped executable WP, CHAT must resolve the current released Policy and pin its exact `active_policy_version`, raw SHA-256, Library release manifest and Git commit/path under C5/C6F.0 before dispatch. Do not use the word `latest`, branch HEAD, Memory or chat summaries as the immutable task binding.
8. **Policy changes during an in-flight task do not erase prior evidence.** Apply C6F.0: CHAT evaluates material impact, preserves the in-flight task's frozen evidence and either issues a scoped transition/re-scope to the newer Policy or records why the existing exact binding remains valid for that unchanged in-flight scope. Agents never self-promote a task to a newer Policy revision.

**Interpretation for existing FOX2 documents:** references such as `FOX2_POLICY_V1.0.md` in released BRD-00/06/08 v0.4 and `FOX2 Policy V1.8` in released Roadmap/P2 design are treated as governance provenance unless a specific clause proves an intentionally frozen dependency. They do not require a BRD/Roadmap version bump solely because a newer FOX2 Policy becomes effective.

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
| Remote GitHub Issues/PRs/commit/blob reads, Library inventories, source manifests, release status, routing/handoff/prompt creation | **CHAT directly** | Use existing authenticated connector when sufficient; avoid delegate-as-browser and duplicate Agent Git/Library scans. Preserve actual approval, authority, and readback. |
| BRD/BCC interpretation, design, scope and routing | **CHAT** | Architecture/security gets independent review when material. |
| Local Windows/macOS/VS Code, local Git checkout/worktree/files, frontend, React, dashboard, charts, ordinary coding and tests | **COPILOT** | Only local-host facts or material coding that CHAT cannot safely accomplish using current connectors; verified access/quota/model and approved path/write right for actual operation. |
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

### C2A.7. Owner CHAT-FIRST routing and remote Git/Library delegation minimization — effective V1.8.3

**Authority:** Direct Owner decision of 2026-10-13 recorded in `/Trading/00_Governance/TRADING_CHAT_FIRST_AGENT_ALLOCATION_OWNER_DIRECTIVE_20261013.md`; this section applies **inside FOX2** and supersedes only conflicting default suggestions about who should perform routine remote GitHub work. It does not remove mandatory R0–R7, C1B source readiness, C4A scope permissions, C5 evidence fields, separation of one-writer worktrees, or C6 acceptance/release gates. Project-specific norms remain separate; this is not an automatic cross-project migration.

**CHAT_FIRST_CAPABILITY_CHECK (required at R0/R4 before any delegated prompt):**

1. Identify the *smallest remaining task delta* after reusing accepted R0 evidence. For each unit of work ask: **Can CHAT complete this safely, completely and verifiably using its current authenticated Library/GitHub/project tools without a local workstation or material programming?** If **YES**, CHAT must perform it directly. Record `CHAT_DIRECTLY_COMPLETED` with relevant exact remote file/commit/hash and no Copilot/Codex assignment for that unit. Do not use Agents as remote GitHub browsers, metadata relays, duplicative Policy/BRD validators, or routine Issue-status updaters merely because the previous workflow did so.
2. CHAT direct scope normally includes Library inventory through pagination, released Policy/BRD/Technical status, latest-effective source selection and source locks; GitHub Issue/PR/branch/commit/blob/diff readbacks, authorized documentation/manifest writes, immutable remote evidence validation and task/status coordination. Direct writes still require actual connector permission, accurate current task scope, non-destructive Git constraints, secret screening and separately applicable publication rules. Having a tool does not grant an operation it is not authorized to perform.
3. Delegate to **COPILOT/CODEX** only **`LOCAL_ONLY_DELEGATED`** (Windows/macOS/VS Code, host process/credential/path, local checkout/worktree, local tests) or **`CODE_WORK_PACKAGE_DELEGATED`** (actual coding, debug/refactor, unit/integration tests and necessary *own-branch* Git edits/commit/push). An Agent may verify relevant received Git bytes and local worktree as a distinct receiving-side safety gate; it must **not** redo CHAT's whole Library/GitHub inventory or already accepted source hashes. Each delegated step includes precise reason CHAT cannot complete it directly, scoped paths/branch, Role · actual Model · Thinking/Optimize · Scope, evidence reuse and STOP.
4. When CHAT tools are **unavailable, blocked, lack rights, or cannot establish correct remote evidence**, report `CHAT_CAPABILITY_BLOCKED` with concrete limitation. Delegate just the missing capability to an eligible Agent only if independent permission and R0–R7 are satisfied; **never route around safety-tool refusal, credential restriction or Git authorizations** using another Agent/transport. Agent assignment is not an escape hatch for access limits.
5. Select WORK only when independent trust/security/release review materially warrants it or the Owner directs it, not for routine Git hash rechecks. Preserve qualification/independence rules. Calculate practical cost using minimum genuine local/coding delta, not every remote read delegated. The 70/30 target applies only to accepted **material coding WPs**, not to CHAT Git/Library tasks; never create artificial delegated WPs to meet it.
6. Record one of `CHAT_DIRECTLY_COMPLETED`, `LOCAL_ONLY_DELEGATED`, `CODE_WORK_PACKAGE_DELEGATED`, or `BLOCKED_CAPABILITY`, with remote/local reason, Owner decision scope, actual source snapshot and unresolved gate. Do not ask Owner for the same approved task-scope authorization multiple times. Do not fabricate Copilot/Codex model/remaining quota or exclusive writer when not exposed; local runtime attestation is separate from CHAT completion.

**Mandatory negative acceptance tests (design only, not claimed to have been executed):** `CF-01` CHAT connector can retrieve remote Git commit yet Copilot is asked to search Issue comments → **REJECT routing**; `CF-02` CHAT cannot inspect Windows worktree and delegates bounded host inspection → **ALLOW if R0–R7**; `CF-03` tool safety refusal triggers Agent workaround → **BLOCK**; `CF-04` Git metadata `push=true` is used as code grant → **BLOCK**; `CF-05` Copilot coding commit to approved own branch while CHAT independently validates remote result → **ALLOW if separately authorized**; `CF-06` candidate Shared Governance or another project policy is silently adopted as FOX2 authority → **BLOCK**; `CF-07` no numeric quota API but Agent claims quota PASS → **REJECT evidence**; `CF-08` already accepted immutable source is rehashed by multiple Agents without invalidation → **REJECT duplication**.

**Explicit implementation boundary:** Owner's instruction changes *who performs eligible work*, not whether a task is approved or its Git/DEV/merge/LIVE permissions. This V1.8.3 document does not independently grant BRG-003 code import, code push, automated Bridge dispatch, merge or LIVE. Existing accepted WPs retain immutable historic sources; new/re-scoped handoffs use latest actually published effective sources and current CHAT-first routing.

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
- Concrete branch/worktree naming is Technical/Protocol configuration; Policy requires only distinct verified ownership, non-overlap, immutable base identity and separate integration authority.

### C4A. Scope-separated Git push and evidence branch protocol

**Explicit grant matrix for each task or applicable standing reporter role** (each permission remains independent; default `NO` unless a verified task grant **or C6F.2A standing authorization** applies **and** actual technical access evidence passes):

| Gate | Permission when separately verified | Not implied |
|---|---|---|
| `GIT_SOURCE_READ` | Fetch/read exact authorized Git objects; preserve uncommitted work | Git write |
| `GIT_REPORT_WRITE` | Create/edit only the task-bound sanitized result/evidence destination defined by the active Technical/Result Protocol | DEV code editing |
| `GIT_REPORT_PUSH` | Push only the task-bound result/evidence scope to its designated non-main destination; provide independently verifiable remote identity | Push elsewhere, merge, release |
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
chat_first_allocation:
  disposition: CHAT_DIRECTLY_COMPLETED|LOCAL_ONLY_DELEGATED|CODE_WORK_PACKAGE_DELEGATED|BLOCKED_CAPABILITY
  chat_direct_actions_and_evidence: <commit/sha/issue/library-or-NOT_APPLICABLE>
  delegated_local_or_coding_delta: <smallest-bound-scope-or-NONE>
  why_chat_cannot_safely_do_it: <observed-host/code-need-or-NOT_APPLICABLE>
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
  allowed_result_scope: <task-bound destination from active Technical/Result Protocol>
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

## C5B. Execution Routing Selector and Local Agent Bridge authority — `FOX2-LOCAL-DISPATCH-002`

**Policy purpose:** define when Local Agent execution may be selected and what authority/state guarantees must hold. **Implementation mechanics are not Policy** and are defined by the separately versioned FOX2 Local Agent Bridge Technical Specification.

1. **Prompt readiness.** The selector is available only for an exact immutable WP whose Policy/Task/Source/Routing/Assignment gates are recorded PASS, required source is ready, exact scope and STOP conditions are frozen, and execution authority for that WP exists. A draft or `SOURCE_PENDING` task is not executable.
2. **Observed UI capability.** Native Intelligent UI is an observed current-turn capability, not an assumed product feature. Native controls may be used only when actually rendered; otherwise use an explicitly identified text fallback. A default/preselected option is never Owner approval.
3. **Three-stage Owner intent.** The Owner separately confirms: (a) manual VS Code vs automated-Agent path; (b) Agent/Model/Thinking-or-Optimize configuration; and (c) Bridge transport vs back/cancel. Only explicit confirmation of Bridge transport authorizes publication of a dispatch for the already-authorized unchanged WP.
4. **Authenticated decision provenance.** A dispatch is executable only when its Owner selection and CHAT decision provenance can be verified against an authorized control-plane source/trust anchor. Self-declared JSON fields, labels, issue text or Agent claims are not sufficient authority.
5. **No silent substitution.** Requested configuration, runtime-resolved configuration and actually observed executor configuration are distinct evidence fields. Material mismatch blocks execution unless CHAT/Owner re-routes or re-authorizes as applicable.
6. **Single-use and bounded scope.** Each dispatch is immutable, single-use, bound to one WP/task/source/configuration/scope, and cannot broaden permissions. Runtime replay/retry behavior must preserve this invariant.
7. **Bridge role.** Bridge performs runtime attestation and transport/execution only. It must not repeat or override Policy/BRD/routing decisions, self-grant rights, edit governance authority, merge, deploy, or infer new scope.
8. **Result authority.** A dispatch is never a result or acceptance receipt. Maximum executor-delivery state before CHAT review is `PUSHED_UNREVIEWED` (or a precise delivery failure state). Result publication and review remain subject to C6/C6F.
9. **Technical boundary.** Dispatch schema encoding, Git branches/paths, polling, local worktrees, process launch, credentials, ledger/replay implementation, crash recovery and Git verification commands belong to the active Technical Specification and may evolve independently while preserving these Policy invariants.

## C6. Execution handoff, review, integration and STOP

Implementing Agent returns actual actor/model/mode, source receipt, branch/worktree/head/diff, changed paths, tests, positive/negative acceptance evidence, unresolved issues, measured (not guessed) quota cost, writer ownership, next actor and STOP. Risk-based independent review applies where Owner specifically requires it or a demonstrable external/safety obligation applies; it cannot be a blanket veto imported from another project. Integration needs scoped Owner decision, real Git permission, single integrator, green tests and current source. No hidden push/deployment.

### C6A. Execution → evidence → independent review state semantics

Canonical governance flow:

`TASK_PREPARED → SOURCE/ROUTING/AUTHORITY_READY → EXECUTION_SELECTED → RUNTIME_ATTESTED → IN_PROGRESS → RESULT_DELIVERED_OR_BLOCKED → PUSHED_UNREVIEWED → REVIEW_READY → CHAT_REVIEW → ACCEPTED | ACCEPTED_PARTIAL | REWORK | BLOCKED`.

`INTEGRATION_ELIGIBLE` and `INTEGRATED` are separate later states and never follow automatically from review. The Technical Specification/Result Protocol defines concrete Git paths, schemas, branch operations and transport mechanics.

Minimum governance requirements:
- executor evidence must identify actual actor/configuration, immutable source/task binding, actual changed scope, tests/evidence, unresolved issues and next gate;
- remote delivery must be independently verifiable before CHAT review;
- executor self-report cannot issue governance acceptance;
- negative conditions such as source mismatch, unauthorized mutation, false PASS, secret/licensed-data leak, replay or self-acceptance block only the affected gate and preserve WIP/evidence.

### C6B. Result Contract governance requirements

Every new/re-scoped WP must produce both human-readable and machine-verifiable result evidence sufficient for CHAT to reconstruct **what was requested, what actually happened, what changed, what was tested, what remains open and what authority was used** without relying on the Agent's private conversation. The exact filenames, schema serialization and evidence directory structure are Technical/Protocol concerns.

Required semantic categories are: identity/executor configuration; authority/routing/source binding; requested vs completed scope; change inventory; tests and positive/negative acceptance mapping; evidence hashes/provenance; remote delivery identity; blockers/security; measured resource usage when observable; and next actor/action. Missing information is explicitly `NOT_VERIFIED`, `NOT_RUN`, `NOT_APPLICABLE` or `BLOCKED`, never silently omitted or upgraded to PASS.

### C6C. Machine result semantics and anti-self-reference

Machine-readable result evidence must use the active Result Contract/Protocol and preserve immutable source/base identity, evidence hashes and truthful delivery state. An in-commit manifest must not fabricate the SHA of its own containing commit; remote result identity is established externally after push/readback. Schema validity is evidence-format validity only and never substitutes for functional/acceptance testing. Concrete schema fields live outside Policy.

### C6D. CHAT intake and disposition governance

CHAT reviews an exact immutable submitted result, independently verifies actual diff/scope/authority/source binding, traces material claims to evidence/tests, checks completeness/security and records one of: `ACCEPTED`, `ACCEPTED_PARTIAL`, `REWORK`, `BLOCKED`. `ACCEPTED_PARTIAL` states the bounded accepted portion and open gates. Tool/network inability to inspect required evidence yields a precise review blocker rather than trust-by-paste. Concrete intake commands, branch/path conventions and receipt serialization are Technical/Protocol concerns.

### C6E. Compatibility, efficiency and no-overwrite

Historical immutable submissions remain historical evidence and are not rewritten merely to conform to newer contracts. New/re-scoped work uses the current applicable Result Contract/Protocol. Keep result payloads minimal but sufficient, reuse still-valid evidence by immutable identity, preserve source/WIP, and never use compatibility handling to create a false PASS or implicit permission.

### C6F. Agent Result Delivery Assurance, Policy Binding and Review Authority

**Purpose:** require deterministic, independently verifiable delivery and review without prescribing Bridge/Git implementation mechanics. Technical encodings and transport procedures live in the Result Protocol / Technical Specification.

#### C6F.0 — Exact Policy/source binding for every new or re-scoped task

Every executable or report-producing task binds the exact currently applicable released Policy identity, immutable task/source identity, applicable result protocol/contract, source-readiness state and STOP conditions. “Latest”, moving branch HEAD, Memory or chat summary is not immutable binding proof. A Policy change during an in-flight task triggers CHAT impact evaluation; evidence is preserved and the task is either explicitly transitioned or allowed to finish under its still-valid frozen binding. Agents never self-promote Policy revisions.

#### C6F.1 — Deterministic destination and evidence classes

Before execution, CHAT must bind a deterministic result destination and expected evidence classes so the submitted result can be located and verified without guessing. The concrete repository paths, branch naming and schema fields are Technical/Protocol concerns. `GIT_SOURCE_READY`, delivery readiness and execution authority are distinct gates; none implies another.

#### C6F.2 — Authority isolation and authenticated publisher provenance

Report/evidence write/push, application-code write/push, PR creation, merge, provider access, broker write and LIVE are separate authorities. A publisher identity or Owner selection must be verifiable from the authorized control plane; self-asserted metadata is not authority. The existing FOX2-only standing Copilot report-publisher authorization remains report-only and is valid only when its actor/host/repository/scope and runtime access conditions are actually satisfied. It never grants application-code mutation or merge/Production/LIVE.

#### C6F.2A — Standing Copilot report-publisher authorization — carried forward unchanged

The Owner-approved standing Copilot report-publisher authorization remains valid only for the **GitHub Copilot Pro reporter role on the authorized FOX2 Windows host**, for properly registered and source-bound FOX2 WPs, subject to actual identity/access, exclusive-writer, permitted-path and security verification at execution time.

It authorizes only sanitized report/evidence write and push to the task-designated **non-main** result destination when the applicable task/source/result contract allows it. It does **not** authorize application-code write/push, main push, force-push, merge, provider/broker access, Production, LIVE, arbitrary identities/hosts, CODEX, WORK, or other projects.

Owner may revoke or narrow this standing authorization. A material Policy transition requires CHAT to revalidate that the authorization still applies. When all conditions above remain true, a repeated per-WP report grant is not required. Concrete path/branch encoding and result transport mechanics belong to the active Result Protocol/Technical Specification.

#### C6F.3 — Delivery state and executor identity semantics

A local file/commit or “DONE” message is not remote delivery. Before independent review, a result may be `PUSHED_UNREVIEWED`, a bounded partial/failure delivery state, or blocked; it may not self-issue governance acceptance. Delivery evidence must distinguish `requested_configuration`, `resolved_runtime_configuration` and `observed_executor_configuration`; silent material substitution is forbidden. Canonical delivery/manifest encoding is defined outside Policy.

#### C6F.4 — CHAT acknowledgement and canonical review dispositions

CHAT independently resolves the exact immutable remote result, verifies source/policy/task lineage, actual changed scope, report/manifest/evidence and applicable tests before recording delivery verification. Delivery verification is separate from semantic acceptance. Canonical CHAT dispositions are `ACCEPTED`, `ACCEPTED_PARTIAL`, `REWORK`, or `BLOCKED`; `ACCEPTED_PARTIAL` must state the accepted boundary and remaining open gates. CI, Issue/label state, Agent self-report or notification alone is never acceptance.

#### C6F.5 — `REVIEW_READY`, idempotency and authoritative review receipt

Automated/manual review discovery is eligible only after verified remote delivery bound to a full immutable result SHA. Manual and automated review share one stable `REVIEW_KEY` for the same immutable result. Queue/notification/scheduler components are transport/index only. Exactly one authoritative CHAT review receipt may exist per `REVIEW_KEY`; duplicates must resolve idempotently, and supersession requires explicit lineage rather than overwrite. Queue or automation failure must leave the underlying pushed result discoverable for manual/recovered review.

#### C6F.6 — No automatic authority escalation after verdict

`REWORK` may prepare a bounded rework proposal but does not auto-dispatch another execution. `ACCEPTED`/`ACCEPTED_PARTIAL` does not authorize main merge, deployment, provider/broker write or LIVE. Any next execution/integration step requires its own applicable routing and authority gates.

#### C6F.7 — Automation capability and Technical Specification boundary

Closed-loop automation may be enabled only after the required platform/background-review/write capabilities are actually demonstrated for the target environment; otherwise use the manual review path without changing governance semantics. Branch topology, polling cadence, workflow files, event storage, SQLite/outbox/ledger design, process isolation, crash recovery, retries, Git commands and schema serialization belong to the separately versioned Technical Specification. Technical changes do not require a Policy revision unless these governance invariants change.

#### C6F.8 — STOP / release boundary

STOP the affected action on unverified or mismatched Policy/task/source binding, untrusted decision provenance, unsafe WIP/writer collision, unauthorized mutation, unverifiable remote delivery, material executor substitution, evidence/security failure or denied platform access. Do not evade platform controls or infer a right from documentation alone.

---

# D. RELEASE CONTROL AND INTERPRETATION

## D1. Effective Policy boundary

FOX2 Policy V1.8.2 is `RELEASED_EFFECTIVE` after successful protected-Library publication, exact-byte readback and release-manifest verification. It supersedes V1.8.1 as active FOX2 governance from that release point. V1.8.1 remains immutable historical evidence and parent provenance.

## D2. Historical source and release evidence

Publication manifests and historical checkpoints preserve what was true at their stated version/date. They are provenance, not current task/runtime state. Superseded operational wording never overrides current C5B/C6F rules or newer verified task/result receipts.

## D3. Explicit limits of this release

- Owner remains the highest internal FOX2 authority, subject to real platform/external restrictions.
- This Policy release grants no DEV, Git code push, merge, provider/broker access, Production or LIVE by itself.
- Library release/readback establishes document effectivity only; it does not prove Agent/model/quota/worktree/provider capability.
- Historical BRD/Roadmap Policy version strings remain governance provenance unless an explicit frozen dependency says otherwise.
- Technical Specifications cannot grant rights, redefine BRD requirements or weaken this Policy.

## D4. Routing disposition after release

`POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK` governs executable handoffs. CHAT or another expressly Owner-assigned actor operates only within actual tool rights. Copilot standing report-only authority remains bounded by C6F.2A and is not a DEV grant. No technical entitlement is presumed from publication.

## D5. V1.6 result-delivery rollout checkpoint — distinct from effective document Policy

> **HISTORICAL CHECKPOINT:** statements below describe the stated historical version/date. Superseded operational wording does not override current C5B/C6F, V1.8.2 released semantics, or newer verified task/result receipts.

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

> **HISTORICAL CHECKPOINT:** statements below describe the stated historical version/date. Superseded operational wording does not override current C5B/C6F, V1.8.2 released semantics, or newer verified task/result receipts.

- `POLICY_V1.7.1_PUBLICATION`: only PASS after published Library raw-byte readback and release manifest; Git mirror must be checked at its own pinned remote commit.
- `STANDING_COPILOT_REPORT_AUTHORIZATION`: **OWNER_APPROVED** for future registered FOX2 WPs at `reports/<WP_ID>/**` on one non-main Copilot branch per WP. No repeated WP-specific approval when C6F.2A applies.
- `COPILOT_TECHNICAL_ACCESS` / `EXCLUSIVE_WRITER`: **UNKNOWN** until actually checked on the Windows host/identity. No automatic push task completion or remote result.
- `GITHUB_PATH_ACL_ENFORCEMENT`: **NOT_VERIFIED / NOT_CLAIMED**. Private-repository Rulesets API returned `403` while evaluating availability on 2026-10-12; no bypass, plan-upgrade or public-repository conversion is authorized. Do not infer GitHub path protections from this internal Policy.
- `P1_RESULT_DELIVERY`: still `PUSH_BLOCKED/NOT_VERIFIED` pending actual Copilot host and result commit; Issues/PRs remain open; P1 tests are not retroactively PASS.
- For this Policy document operation: `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `MAIN_PUSH=NO`, `MERGE_ALLOWED=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO`.


## D7. V1.8 Local Agent dispatch checkpoint

> **HISTORICAL CHECKPOINT:** statements below describe the stated historical version/date. Superseded operational wording does not override current C5B/C6F, V1.8.2 released semantics, or newer verified task/result receipts.

- `AGENT_PROMPT_POLICY_DECISION_CHECKS`: **SINGLE-PASS** for the exact immutable WP revision; Bridge cannot duplicate or override them.
- `LOCAL_DISPATCH_SELECTION`: Owner-selected `EXECUTE_LOCAL_AGENT` is required before CHAT publishes an executable dispatch artifact; `SAVE_PROMPT_ONLY` produces no dispatch.
- `DISPATCH_TRANSPORT`: Git append-only `docs/agent_handoff/<WP_ID>/dispatch/<DISPATCH_ID>.json`, schema v1, `max_runs=1`, bound to exact task/prompt/policy/source identities.
- `BRIDGE_RUNTIME_ROLE`: runtime attestation + CLI invocation only; no BRD/Policy/routing reinterpretation, no self-grant, no main/merge/deploy.
- `RESULT_CONTRACT_V2`: unchanged; all result publication and independent CHAT acceptance controls remain in force.
- `UI_BUTTON_STATUS`: Policy defines the selection semantic. A visual one-click button/quick action is used only when the current ChatGPT client/integration technically exposes it; otherwise the exact action selection text is equivalent and CHAT still performs the Git dispatch operation.

## D8. V1.8.2 — Execution Routing Selector / Intelligent UI checkpoint

- `EXECUTION_ROUTING_UI_CAPABILITY`: native Intelligent UI is capability-dependent on the active model/runtime/client and is considered present only when actually rendered in the current response. CHAT must not infer capability from product-level availability alone.
- `EXECUTION_ROUTING_UI`: when `NATIVE_INTELLIGENT_UI_RENDERED`, prefer one native single-select radio group plus explicit confirmation CTA per screen; preselection is not approval. Otherwise use `TEXT_FALLBACK` with the same explicit-confirmation semantics and clearly identify it as fallback.
- `NO_FAKE_NATIVE_UI`: Unicode/text symbols such as `◉`, `○` or bracketed button text may be used only as plain-text fallback representation and must never be described as a rendered native ChatGPT Intelligent UI control.
- `SCREEN_1_EXECUTION_PATH`: exactly `MANUAL_VSCODE` or `CONFIGURE_AUTOMATED_AGENT`. Confirmed `MANUAL_VSCODE` terminates `END_NO_BRIDGE`; no `SAVE_PROMPT_ONLY` option exists.
- `SCREEN_2_AGENT_CONFIGURATION`: Owner confirms one explicit Agent/Model/Thinking-or-Optimize configuration after CHAT shows a recommendation and eligible alternatives. No `SAVE_CONFIGURATION_ONLY` option exists.
- `SCREEN_3_TRANSPORT`: exactly `DISPATCH_VIA_LOCAL_BRIDGE`, `BACK_TO_AGENT_CONFIGURATION`, or `CANCEL_EXECUTION`; only confirmed Bridge transport creates a dispatch.
- `DISPATCH_TECHNICAL_CONTRACT`: the active Bridge Technical Specification/dispatch schema must bind Owner-confirmed configuration and authenticated selection/decision provenance. Policy does not pin a schema filename/version; Bridge may not silently substitute Agent/model/mode.
- `AGENT_PROMPT_POLICY_DECISION_CHECKS`: remain **SINGLE-PASS** for the exact immutable WP revision. Bridge performs runtime attestation only.
- `RESULT_CONTRACT_V2`: unchanged; result publication and independent CHAT acceptance controls remain in force.

## D9. V1.8.2 — Closed-loop Review governance checkpoint

- `REMOTE_RESULT_GATE`: `REVIEW_READY` is eligible only after verified remote push and a pinned full immutable result SHA; local-only or moving-head references are insufficient.
- `REVIEW_KEY`: `FOX2:<WP_ID>:<RESULT_COMMIT_SHA>` is the idempotent identity shared by manual and scheduled review.
- `AUTOMATED_REVIEW_TRIGGER`: configured Bridge/GitHub/ChatGPT automation may automatically surface an unseen `REVIEW_READY` item to CHAT without a new Owner message for the same result.
- `QUEUE_AUTHORITY`: GitHub Action, Issue, label, notification and scheduler are transport/index only; none may emit semantic acceptance.
- `CHAT_REVIEW_AUTHORITY`: CHAT independently reviews the exact immutable result SHA and records `ACCEPTED | ACCEPTED_PARTIAL | REWORK | BLOCKED` in a separate authoritative review receipt.
- `AUTO_REWORK_DISPATCH`: **NO**. REWORK may prepare a prompt, but a new execution still follows the applicable Owner routing/confirmation flow.
- `AUTO_MERGE_DEPLOY`: **NO**. ACCEPTED/`INTEGRATION_ELIGIBLE` does not authorize main merge, deployment, Production/provider/broker write or LIVE.
- `TECHNICAL_SPEC_BOUNDARY`: branch/path conventions, polling, workflow implementation, trust-anchor verification, process isolation, Git verification, local ledger/outbox, crash recovery, queue plumbing and review-receipt concurrency stay in the separately versioned FOX2 Local Agent Bridge Technical Specification.

## D10. V1.8.2 release interpretation checkpoint

The Owner explicitly ordered publication of the reviewed REV4-derived Policy. The following interpretation points remain normative:

1. Native Intelligent UI is used only when actually rendered; otherwise use a clearly identified text fallback.
2. A preselected/default choice never counts as Owner approval.
3. Screen 1 remains `MANUAL_VSCODE` vs `CONFIGURE_AUTOMATED_AGENT`; confirmed manual VS Code ends the Bridge path.
4. Screen 2 remains Agent/Model/Thinking-or-Optimize configuration only.
5. Screen 3 remains Bridge / Back / Cancel; Bridge dispatch requires explicit confirmation.
6. A verified remote result may create `REVIEW_READY`; the trigger itself never means acceptance.
7. Manual and scheduled review of the same `REVIEW_KEY` resolve to one authoritative CHAT review receipt.
8. `REWORK` does not auto-dispatch; `ACCEPTED`/`ACCEPTED_PARTIAL` does not auto-merge/deploy.
9. Policy contains authority/invariant semantics only; implementation mechanisms belong to separately versioned Technical Specifications.
10. Technical Specifications cannot grant rights, redefine BRD requirements or weaken Policy.
11. This Policy release itself creates no DEV, Git code-push, merge, deployment, provider/broker or LIVE authority.

## V1.8.3 release delta and transition — 2026-10-13

- **Only affected FOX2 governance rule:** R0/R4 task-owner selection and who performs remote GitHub/Library/source tasks. Owner's CHAT-FIRST decision is effective within FOX2 upon successful Library publication/manifest and Git readback; source version for new prompts is V1.8.3.
- **Unchanged:** Bridge Technical v0.4, SFR v0.1 Candidate, FOX2 BRD/Data Contracts, accepted code/evidence, Review/Result Protocol, R0–R7 safety and C4A/C5/C6 execution gates, source and runtime release tests. Existing Accepted/blocked WPs are not silently rerun or granted new rights.
- **Cross-project scope:** Owner's shared routing directive may guide CHAT immediately in other projects; no FOX2 Policy inheritance or automatic release of another project's Policy/DEV/LIVE. Trading-wide migration/sync remains paused unless separately authorized.
- **Verification limit:** The policy publication is documentation/effectivity evidence only; automatic tool delegation enforcement and Bridge runtime capabilities require separate verified implementation and tests.
