# FOX2 — CODE-FIRST / CHAT-FIRST Owner Directive, Coordination Correction and Work Routing

**Recorded:** 2026-10-19 by CHAT, on the explicit Owner instruction in this conversation
**Project:** FOX2 only
**Record class:** OWNER-APPROVED OPERATIONAL PRIORITY / GOVERNANCE CHANGE-IMPACT CANDIDATE / NOT AUTOMATIC POLICY EFFECTIVE
**Source status:** Candidate isolated from current governance/release branches; no implementation / dispatch / runtime authority claimed solely from this record.
**Owner direction:** agrees to switch from Bridge-first process bottlenecks to Code-First development and expressly asks to re-evaluate CHAT's avoidable delegations to WORK.

## 1. Corrected executive interpretation and source anchors

1. Policy v1.8.9 at `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359:docs/governance/FOX2_POLICY_V1.8.9.md` makes Codex/Copilot primary implementation engines; Bridge is optional transport/supervision, not a parallel governance engine. Project-wide PreExec applies to *new/re-scoped executable handoffs*, but material checks must match the selected execution route. No BLOCKED receipt may be called PASS.
2. The existing Master Plan `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9:docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md` identified two nonoverlapping lanes (Application versus Bridge) yet its 2026-10-17 scheduling directive prioritized BRIDGE_FIRST and kept APP-BATCH-B PAUSED until Bridge readiness.
3. The Owner's **2026-10-19** agreement supersedes this Bridge-before-application **scheduling dependency for planning and task preparation**, not the source/release or executable admission constraints of the old Master Plan. Resume coordination of offline APP-BATCH-B now. Do not silently rewrite that old immutable document: integrate this decision into the next governed Master Plan revision with proper source/release controls.
4. APP-BATCH-B work branch observed at `fc8aba202e15bddfcc5156b2c1bb36ed222329eb` (2026-10-19 check); frontend React/TypeScript code already exists. `docs/agent_handoff/FOX2-M1-A-APP-BATCH-B/task.md` says `PAUSED_AFTER_UI_SLICE / WAIT_BRIDGE_READY`; that scheduling HOLD is removed **for planning and fresh task readiness work**, not proof that current code execution is admitted. Existing local PreExec receipt is historical BLOCKED and must be reassessed on a correct app-specific DEV route.
5. Manual Admission infrastructure WP remains at exact remote receipt publication `1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d`: `PREEXEC=BLOCKED` because bridge_bootstrap_controls=FAIL (stored paused and two workers host-reported). A good CODEX marker does not remedy a Bridge runtime control failure. The bounded Owner infrastructure code grant is recorded at `c23d28bd56d9d06d64561dcf255b2d94227f6acc`.
6. Existing original immutable compatibility Dispatch001 publication `3f885b2d24cb131b5e96dfdb67a44677599197e2` and Canary009 branch HEAD `501822a33ef08c7365154913bbc677544856eee5` remain HOLD/no replay.
7. Baseline runtime code `f3d6468...` accepts execution_path MANUAL_LOCAL in Registry but `dispatch_normalizer.py` rejects it for Bridge; `ledger.py` enforces paused/stop_requested claims, while `request-exit` sets a sticky stop flag not cleared by `resume`. This is a real runtime engineering defect/contract gap, not a missing Owner decision.
8. This record is a source-bound directive and retrospective; it is not a replacement for a signed release authority, manifest update, effective policy publication, Windows state evidence, task-specific PreExec, or a new executable Dispatch.

## 2. New operating rule: CODE-FIRST with risk-proportionate gates

**Priority one:** produce a runnable, fully tested M1-A offline localhost FOX2 application, using accepted backend API/store/DSM and existing React UI, under existing BRD/TechSpec boundaries.

**Bridge:** remains a concurrent or later *infrastructure* delivery lane rather than a prerequisite to typecheck/build/test offline product. Finish Manual Local Admission/worker controls as a single consolidated engineering defect within its already authorized WP, not a succession of Owner-facing micro-WPs and administrative fix Dispatches.

**DEV, INTEGRATION, OPERATIONAL** gates must be separated:
- DEV: exact task/source/Owner code authority, current local agent route and worktree/writer, capability, route-appropriate shared PreExec and immutable delivery/readback. A Bridge worker being PAUSED is not a material prerequisite **for a truly independent manual development route**; it remains material for any route that actually depends on Bridge.
- INTEGRATION: code/test/API/fixture correctness; regression/security/negative tests, bounded Git result and CHAT diff/test intake.
- OPERATIONAL/RELEASE: Bridge installed singleton, durable claim/no-replay, recovery, protected Canary, independent review where required, release authority, provider/broker/LIVE. Preserve these gates completely.

**Critical prohibition:** changing the *classification* of a capability must reflect an independently executable route and a governed source/task binding, not suppress a failure to force PASS. Existing `MANUAL_LOCAL` Dispatch001 cannot be reinterpreted as free unrecorded `codex exec`; its published semantics/no-replay remain immutable.

No automatic broad authorization is implied for APP-BATCH-B coding just because priority changed. CHAT must check whether applicable Owner grants cover the still-pending integration/test slice and arrange a proper route-specific task/PreExec/readback; if insufficient, prepare scope-bound grant without replaying old approvals. No main/merge/deploy/provider/broker/LIVE authority is added.

## 3. CHAT-FIRST / WORK-EXCEPTION responsibility contract

FOX2 Skills read for this review: `fox2-project-health`, `fox2-status-roadmap`, `fox2-strategic-agent-triage`, `fox2-agent-route-runtime`, `fox2-governance-preflight`, `fox2-document-publication`, `fox2-source-resolver`, `fox2-result-review`, `fox2-feature-certification`, `fox2-agent-prompt-builder`. Their self-contained guards already say CHAT-FIRST; difficulty or document size is not by itself a reason to delegate.

**CHAT MUST DO DIRECTLY if actual tools, technical access and permission are available:**
- source resolver: live Git identity, manifests, hash/bytes, policy/authority distinction, current branches/worktree receipts as remotely observable;
- Policy/BRD/TechSpec/Dictionary/consumer impact, bounded architectural review, routing and task state decisions;
- design/source readiness, source-bound scope, prompt/task/dispatch candidate drafting and allowed Git candidate publication/readback;
- source/doc publication, Git–Library sync via an actually available authorized connector, version reconciliation, without automatically sending WORK;
- CHAT PreExec intake, Agent result/diff/tests/readback verification, routine QA, ACCEPT/REWORK/HOLD;
- feature-level status, roadmap, owner decisions, acceptance mapping, retrospectives, issue summary and follow-up actions;
- coordination and surgical next step selection; do not re-request an Owner decision already backed by the current authority.

**CODEX/COPILOT/HOST** perform work CHAT cannot truthfully do as a connected coordinator: local Windows process state, nontrivial product code/test/build/package and real host E2E, after task authorization and corresponding route/PreExec. CODEX current proposed pinned route for complex Bridge changes is `gpt-6.1-sol / medium / FULL_ACCESS` subject to fresh task-specific eligibility. No Agent execution from this document.

**WORK only when independence or deep specialized analysis is material**, for example independently verifying a safety-critical race/recovery/broker semantic, a major release/installed pre-Canary audit, a documented source-authority conflict for which CHAT would be an inappropriate sole reviewer, or a separate reviewer required by published acceptance/release criteria. The requester must name a concrete *independence question*, source lock, bounded deliverable and acceptance criterion. WORK must actually operate on accessible sources; no fabricated independent approval. One audit at a meaningful checkpoint, not after each subtask.

**CHAT must not delegate to WORK merely because:** 10+ files, a long report, Git/Library documents, metadata/hash comparison, repeated static checks, generic roadmap/status, ordinary PreExec receipt readback, writing a prompt, or a task is complex but within CHAT's tools and role. First attempt the direct permitted tool operations, report exact limitation, then route only residual work.

**Retrospective examples / corrective routing:**
- Git↔Library full documentation synchronization/check/reporting: CHAT directly handles available Git and Library connector operations and actual readback; WORK only a separate required independent audit, never primary executor by default.
- Delta analysis, manifest/source binding, code result intake, roadmap and 15 static checks already available: CHAT performs once; no broad repeated WORK audit without a distinct substantive question.
- Pre-Canary independent substantive audit of concurrent runtime and release safety: WORK is appropriate because genuine independence is required, once the tested candidate and evidence are ready.
- Windows worker Q0/Q1/process singleton checks: host/CODEX for inaccessible on-machine facts, not WORK simply to re-read Git documents.
- If CHAT can finish 80% and host is needed for 20%, CHAT completes 80% and sends a bounded 20% handoff.

**Audit tax check before WORK call** (all must be YES): independent viewpoint actually required; CHAT direct tools cannot satisfy the same criterion; exact source and scope locked; incremental finding useful for acceptance; no duplicated prior audit; result actionable. Otherwise `WORK=NOT_NEEDED`.

## 4. Priority and near-term sequence

**P0 / CHAT NOW:** mark 2026-10-17 BRIDGE_FIRST application scheduling dependency superseded by this Owner 2026-10-19 direction for planning. Live-check APP-BATCH-B branch/task, source set, code grants, current Codex availability and UI/API test scope. Select an independent DEVELOPMENT execution path supported by Policy/Dictionary/actual host; preserve any published immutable Dispatch from unrelated WPs. Do not require installed Bridge to PASS before APP typecheck/build unless actual selected route needs it. Do not create micro-WPs for capability fixups or repeat completed static audits.

**P1 / M1-A product:** CODEX after its fresh route-appropriate PreExec PASS and CHAT PASS_TO_ASSIGN, complete existing APP-BATCH-B as one product batch: React build/typecheck; four routes; UI/backend API integration; watchlist CAS, unavailable/provenance; security and offline localhost tests; bounded non-main results. Do not claim M1-A accepted before evidence.

**P2 / Manual Admission & Bridge:** reuse same authorized infrastructure WP and existing BLOCKED receipt as evidence; resolve runtime defects in a single consolidated engineering batch only when an executable safe development route is verified. Avoid making preflight depend on production-style Bridge singleton when selecting an independently supported development route. Installed runtime adoption and old immutable Dispatch001 are downstream post-code gated activities.

**P3 / independent checkpoint:** WORK only for genuinely independent high-risk Bridge/Canary audit as required; CHAT owns ordinary diff/result intake, source comparisons and documentation publication. Subsequent Canary009 separately authorized, single-use, no blind replay.

**P4 / later integration:** owner-approved release process and separate market/provider/broker entitlements after product readiness. No global Policy/Registry/Dictionary EFFECTIVE claims from this planning record.

## 5. Minimal routing/status scorecard

Every project status or Agent handoff must report: code deliverable completed/tested; current blocking technical fact; material remaining gate; who can directly fix it; the few exact source refs; and shortest next action. Avoid turning successful document publication into claims of actual product delivery.

```text
OWNER_DIRECTION=CODE_FIRST_CHAT_FIRST_APPROVED
OLD_BRIDGE_FIRST_SCHEDULING=SUPERSEDED_FOR_PLANNING
APP_BATCH_B=RESUME_READINESS_AND_PREPARATION_NOT_AUTOMATIC_EXECUTION
BRIDGE_DEFECT=REAL_CODE_AND_CONTROL_HANDOFF_GAP
INFRA_PREEXEC=BLOCKED_PRESERVED
INFRA_DISPATCH=NOT_PUBLISHED
ORIGINAL_DISPATCH001=HOLD
CANARY009=HOLD
CHAT_PRIMARY_ROUTING=YES
WORK_DEFAULT=NOT_NEEDED
WORK_EXCEPTION=INDEPENDENT_MATERIAL_AUDIT_ONLY
RELEASE_POLICY_UPDATE=NOT_DONE
RUNTIME_DEV_AUTHORIZATION=ROUTE_SPECIFIC_GATES_REQUIRED
```
