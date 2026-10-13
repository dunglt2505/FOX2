# FOX2 — Local Agent Bridge Technical Specification v0.4

**Document ID:** `FOX2-LOCAL-AGENT-BRIDGE-SPEC`  
**Version:** `0.4`  
**Project:** `FOX2 ONLY`  
**Status:** `RELEASED_EFFECTIVE / DESIGN_BASELINE / AUTOMATED_GATE_A_BLOCKED`  
**Date:** 2026-10-13  
**Purpose:** Technical implementation design for FOX2 local Agent dispatch, execution, Git result delivery, durable review discovery and CHAT review-return mechanics.  
**Released predecessor:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.3.md` — immutable historical release. v0.4 supersedes v0.3 **for new FOX2 Bridge document handoffs upon verified v0.4 Library release/manifest and exact Git readback**; old WPs remain bound to their immutable source unless explicitly rerouted.  
**Parent technical candidate:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.3_CANDIDATE.md` (WORK-audited source); v0.2 remains earlier history.  
**Owner standing Git decision:** `FOX2_BRIDGE_STANDING_GIT_BRANCH_GRANT_20261013.md`, Git commit `bcd78aabeaf7817b7d9b682a0180445293061f41`; branch `work/FOX2-REVIEW-EVENTS-bridge` created/readback at `c9dc41b97ca8bc58f06cc2f3701832ba083422e3`. This is a scoped Owner grant, NOT proof of runtime credential/GitHub branch enforcement.  
**Governance review counterpart:** `FOX2_POLICY_V1.8.2.md` (released governance authority).  
**Authority boundary:** This specification defines **HOW** Policy/BRD requirements are implemented. It does not create DEV, Git, merge, deployment, Production, broker, or LIVE authority; it cannot redefine BRD requirements or weaken Policy. Technical versions may evolve independently when governance/business semantics are unchanged.  
**Design decision:** FOX2-only. No multi-project registry, generic project abstraction, or cross-project runtime is included. A future project may clone/fork this Bridge implementation and adapt its project-specific bindings separately.

## Effective-source and handoff version lock — v0.4

**LATEST_EFFECTIVE != HIGHEST_VERSION_FILENAME.** For every *new* Copilot/Codex/Bridge task, CHAT resolves the latest Owner-approved, actually published FOX2 Policy and Technical Spec from their Library release records and exact-byte manifests, and then verifies the exact corresponding remote Git commit:path/blob before assigning. A Candidate can be read as non-binding research or planned delta but is never silently promoted. Existing accepted work does not auto-rebase to new documents.

- Active Policy: FOX2 Policy **V1.8.2 RELEASED_EFFECTIVE**, exact Library raw SHA-256 `552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc`, pinned Git source-set `c9dc41b97ca8bc58f06cc2f3701832ba083422e3`.
- Active Bridge technical baseline for **new** Bridge tasks: **v0.4 RELEASED_EFFECTIVE** only after its own Library exact-byte readback + version-specific manifest and immutable Git mirror readback. Its release manifest identifies its exact bytes and Git source commit. v0.3 is immutable history and MUST NOT be described as the current technical baseline once these checks pass.
- Current Owner standing review-event Git grant is a separately verified Owner decision; branch existence is not proof of a functioning Bridge publisher or a scoped remote IAM policy.
- A handoff MUST include `source_lock` with `policy_version/status/library_raw_sha256`, `technical_version/status/library_raw_sha256`, `technical_git_commit/path/blob_sha`, `owner_grant_commit/blob`, `task_wp_id`, `source_check_time`, `runtime_permission_matrix`, and `candidate_refs_nonbinding`. Missing, unverified or contradictory fields mean **BLOCKED_SOURCE_VERSION**; CHAT refreshes routing and regenerates the prompt, never silently falls back to v0.3 or a moving default branch.
- On any newer verified release, release supersession, source hash drift, Owner revocation or material task-scope change, STOP the affected new dispatch and rebind with fresh CHAT R0–R7. No software/model/Agent execution automatically gains DEV, push, merge or LIVE from a document release.

---

## 0. Normative boundary and source precedence

- **Policy:** authority, roles, permission classes, state/verdict semantics, required evidence classes, STOP/release gates.
- **BRD/Data Contract/Acceptance:** business/functional requirements and acceptance intent.
- **This Technical Specification:** branch/worktree topology, schema encodings, trust anchors, process isolation, persistence, replay/crash recovery, Git verification, queue/outbox design, observability and implementation tests.
- **Precedence:** applicable external restriction → Owner decision → released Policy → released BRD/Data Contract/Acceptance → released Technical Specification → candidates/drafts.
- **No rights by implementation:** a technically valid Bridge operation is still forbidden unless the applicable Policy/task grant exists.
- **Independent versioning:** technical-only changes do not force Policy/BRD version changes unless their owned semantics materially change.

---

## 1. Objectives

The FOX2 Local Agent Bridge shall provide a controlled, auditable, low-friction execution loop:

```text
Owner
  ↓
CHAT
  ↓
FOX2 Git Dispatch
  ↓
FOX2 Local Agent Bridge on Windows
  ↓
Codex CLI / GitHub Copilot CLI
  ↓
isolated FOX2 worktree
  ↓
tests + Result Contract v2
  ↓
GitHub task branch
  ↓
REVIEW_READY
  ↓
CHAT automated independent review
  ↓
ACCEPTED / REWORK / BLOCKED
```

Primary goals:

1. Remove manual prompt copy/paste when the Owner chooses Local Bridge execution.
2. Keep CHAT as the decision/routing owner and independent reviewer.
3. Keep Bridge limited to runtime attestation and execution transport.
4. Keep Codex/Copilot isolated from the main FOX2 working tree.
5. Preserve immutable Git evidence for dispatch, execution result, and review.
6. Automatically surface pushed Agent results to CHAT for review.
7. Prevent silent re-routing, silent model substitution, duplicate execution, auto-merge, and auto-rework loops.

---

## 2. Explicit FOX2-only scope

The Bridge is intentionally specific to FOX2.

### 2.1 Fixed project identity

```text
PROJECT_ID       = FOX2
REPOSITORY       = dunglt2505/FOX2
LOCAL_REPO       = C:\Projects\FOX2
BRIDGE_ROOT      = C:\Projects\FOX2-AgentBridge
WORKTREE_ROOT    = C:\Projects\FOX2-worktrees
```

The Bridge MUST reject any dispatch whose project, repository, workspace, or branch namespace does not match FOX2.

Example failure:

```text
LOCAL_RUNTIME_BLOCKED
reason = PROJECT_OR_REPOSITORY_MISMATCH
```

### 2.2 Non-goals

v0.3 does NOT implement:

- multi-project registry;
- FOX/Mantis/Silkworm support;
- generic reusable project profiles;
- multi-PC execution;
- concurrent Agent execution;
- cloud execution;
- inbound HTTP server;
- public webhook receiver on the local PC;
- auto-merge;
- auto-deploy;
- auto-rework dispatch;
- broker/LIVE execution.

Future projects may clone/fork this Bridge after FOX2 is proven stable.

---

## 3. Fixed Git topology

### 3.1 Control plane

CHAT-owned dispatch branch:

```text
work/FOX2-LOCAL-DISPATCH-chat
```

Purpose:

```text
CHAT → Local Bridge
```

Dispatch artifacts:

```text
docs/agent_handoff/<WP_ID>/
├── prompt/<PROMPT_ID>.md
└── dispatch/<DISPATCH_ID>.json
```

CHAT is the intended writer of the control branch. Bridge consumes it read-only.

### 3.2 Execution/result plane

One task branch per Agent execution:

```text
work/<WP_ID>-codex
work/<WP_ID>-copilot
```

Purpose:

```text
Bridge / Agent → GitHub result
```

Mandatory Agent result:

```text
reports/<WP_ID>/
├── report.md
├── evidence_manifest.json
└── evidence/**        # optional, sanitized, minimal
```

### 3.3 Review-event plane

Bridge-owned review event branch:

```text
work/FOX2-REVIEW-EVENTS-bridge
```

Purpose:

```text
Bridge → Review Queue
```

Review event:

```text
review_events/<WP_ID>/<RESULT_COMMIT_SHA>.json
```

**Standing Bridge event-publisher grant (Owner decision 2026-10-13):** The Owner authorizes recurring Git write/push **only to the Bridge-owned review-event branch** and only for the above sanitized immutable event JSON paths, subject to authenticated Bridge service identity, writer exclusivity, secret/path inspection, fast-forward/ancestry validation and exact remote readback at each push. Per-event Owner approval is not required. This grant does NOT include source/code diffs, cross-WP output branches, Git control branch, CHAT review branch, merge or production. Current capability: branch EXISTS and CHAT verified its ref; actual Bridge-service credential and remote push remain UNKNOWN/NOT_VERIFIED.

### 3.4 CHAT review plane

CHAT-owned review receipt branch:

```text
work/FOX2-CHAT-REVIEWS
```

Review receipt:

```text
reviews/<WP_ID>/<RESULT_COMMIT_SHA>.json
```

---

## 4. Local filesystem layout

```text
C:\Projects\
├── FOX2\
│
├── FOX2-AgentBridge\
│   ├── .venv\
│   ├── src\
│   │   ├── bridge\
│   │   ├── adapters\
│   │   ├── git\
│   │   ├── runtime\
│   │   └── review\
│   ├── config\
│   ├── data\
│   │   └── bridge.db
│   ├── logs\
│   └── tests\
│
└── FOX2-worktrees\
    └── <WP_ID>\
```

The Bridge MUST NOT use `C:\Projects\FOX2` as the Agent editing workspace.

`C:\Projects\FOX2` is a reference/bootstrap repository only.

Each implementation execution uses an isolated worktree:

```text
C:\Projects\FOX2-worktrees\<WP_ID>
```

---

## 5. Required local tooling

Before Bridge implementation/execution:

```text
Git for Windows
PowerShell 7+
Python 3.13 x64
pip / venv
GitHub CLI (gh)
OpenAI Codex CLI
GitHub Copilot CLI
Visual Studio Code
WinGet / App Installer
```

SQLite server is NOT required; Python `sqlite3` is sufficient.

Docker, WSL, Redis and PostgreSQL are out of scope for MVP.

BRG-001 owns machine preflight.

---

## 6. Bridge components

```text
FOX2-AgentBridge
│
├── DispatchPoller
├── DispatchValidator
├── TrustAnchorVerifier
├── ReplayGuard
├── RuntimeAttestor
├── WorktreeManager
├── AgentRouter
│   ├── CodexAdapter
│   └── CopilotAdapter
├── ExecutionSupervisor
├── ResultInspector
├── GitDeliveryVerifier
├── ReviewOutbox
├── ReviewEventEmitter
├── ReviewReceiptWriter
└── LocalLedger
```

### 6.1 DispatchPoller

Responsibilities:

- poll/fetch only the configured FOX2 control branch;
- discover new dispatch artifacts;
- never scan arbitrary repositories;
- never execute files outside the dispatch path contract.

Initial polling interval:

```text
10–30 seconds
```

This interval is configuration, not Policy.

### 6.2 DispatchValidator

Validates:

- schema;
- `project == FOX2`;
- exact repository;
- dispatch ID;
- task/source/policy/prompt hashes;
- Owner selection receipt;
- requested Agent configuration;
- branch/base;
- path allowlist/denylist;
- `max_runs == 1`.

Validation failure means no Agent launch.

### 6.3 TrustAnchorVerifier

Dispatch authorization MUST NOT trust self-declared JSON authority fields alone. Before launch, verify the dispatch against configured control-plane trust anchors:

- exact FOX2 repository and configured control branch/ref;
- immutable dispatch commit and ancestry from an authorized CHAT control-plane base;
- task/prompt/source hashes and Policy binding;
- Owner selection receipt hash/ID and CHAT decision receipt;
- publisher provenance available from the configured authenticated Git/GitHub channel;
- no unapproved mutation between the decision receipt and dispatch payload.

**Selected MVP trust target:** `GITHUB_APP + ENFORCED_CONTROL_REF`. A dedicated FOX2 GitHub App/service identity remains the intended publisher, but **Gate A may certify this target only when the repository actually exposes and enforces a supported ref-control mechanism**.

If repository rulesets are used, Gate A must pin the exact ruleset ID/configuration and verify through authenticated GitHub readback that the control ref has effective `Restrict updates` and, where applicable, `Restrict creations`; only the dedicated publisher App/service actor may have the required operational bypass. Force-push/deletion prohibitions and any permitted administrative changes are evidenced separately. A ruleset or bypass list that is merely documented but not effective is `BLOCKED_TRUST_NOT_ENFORCED`.

**Observed FOX2 capability snapshot — 2026-10-13, revalidate at Gate A:** repository `dunglt2505/FOX2` is private and owned by account type `User`; repository-rulesets API returned `403` with `Upgrade to GitHub Pro or make this repository public to enable this feature`; observed branches, including `main`, reported `protected=false`. Therefore no protected-control-ref enforcement is currently proven and `AUTOMATED_GATE_A=BLOCKED_CAPABILITY_UNAVAILABLE`. This observation is capability evidence, not a request to change plan/repository ownership.

Publisher verification must identify the **authenticated publication evidence** that binds the dedicated App/service identity to the exact dispatch commit and the exact decision/selection receipt. Commit author/committer text, repository membership, ancestry, or an authenticated GET of the commit alone are not publisher proof. CHAT's authorized route to the App/service publisher, App installation identity, token/credential custody boundary, publication operation evidence and remote readback must be specified and verified before Gate A certification.

Initial publisher provisioning, supported control-ref enforcement, key/token rotation/revocation and failure behavior are explicit Gate A acceptance inputs. Until all are actually installed and verified, automated Bridge execution remains blocked; manual VS Code execution may remain available under separate routing.

If publisher/selection provenance cannot be verified, return `LOCAL_RUNTIME_BLOCKED / UNTRUSTED_DISPATCH_PROVENANCE`.

### 6.4 ReplayGuard

A dispatch is single-use.

Unique local identity:

```text
DISPATCH_ID
```

Persistent ledger ensures restart does not rerun the same dispatch. The Bridge MUST durably claim a dispatch in one transaction **before** Agent process creation. Minimum claim states:

```text
DISCOVERED → CLAIMED → STARTING → RUNNING → RESULT_INSPECTION → DELIVERY_VERIFY → TERMINAL
```

Persist `dispatch_id`, immutable dispatch SHA, claim time, requested configuration, resolved configuration, process identity when spawned, worktree/branch and last durable transition. On restart, reconcile non-terminal claims against actual process/worktree/Git state. Ambiguous state is `RECOVERY_REQUIRED` and MUST NOT relaunch automatically.

Duplicate outcome:

```text
DISPATCH_DUPLICATE_IGNORED
```

### 6.5 RuntimeAttestor

Bridge performs runtime facts only.

It MUST check:

- repository mapping;
- current Git executable;
- GitHub auth/identity;
- selected Agent CLI exists;
- selected model/mode is available;
- branch/base exists;
- worktree target is safe;
- no conflicting writer/WIP;
- required runtime Git permissions exist;
- prompt/task/policy/source hashes still match the exact dispatch binding;
- Policy binding is data-driven (`version`, raw hash, release manifest, Git path/commit) and is not hardcoded to one Policy version;
- requested Agent/model/mode is distinguishable from runtime-resolved and actually observed executor configuration;
- dispatch has not been executed.

It MUST NOT repeat:

```text
POLICY_CHECK
TASK_STATE_CHECK
ROUTING_R0_R7
ASSIGNMENT_CHECK
```

Those are CHAT decision gates.

### 6.6 WorktreeManager

Creates an isolated worktree from the **immutable authorized base SHA**, not from a moving branch head. Before launch the Bridge verifies worktree HEAD equals the authorized base, path ownership is exclusive, and any pre-existing task branch matches the expected frozen head; branch movement never changes the execution source.

Source SHA-256 validation uses the **raw Git blob payload** at pinned full `commit:path`, matching canonical released bytes. Never substitute normalized text, Git object SHA-1, PowerShell re-encoding, BOM-added output or JSON reserialization. Prompt delivery must preserve verified payload bytes under an explicit adapter encoding rule, and checkout/filter/newline transformations are measured rather than silently accepted.

Forbidden:

```text
reset --hard on Owner workspace
git clean on Owner workspace
stash Owner work
rebase Owner branch
force push
direct main work
```

### 6.7 AgentRouter

Uses the Owner-confirmed requested configuration carried by dispatch. Resolve actual local capability at runtime and persist three distinct identities:

```text
requested_configuration
resolved_runtime_configuration
observed_executor_configuration
```

No silent substitution. A material mismatch blocks launch and returns control to CHAT; do not rewrite the dispatch in place.

If the dispatch requests a model/mode not available locally:

```text
LOCAL_RUNTIME_BLOCKED
reason = REQUESTED_AGENT_CONFIGURATION_UNAVAILABLE
```

### 6.8 ExecutionSupervisor

Responsibilities:

- launch one Agent process;
- bind working directory;
- capture stdout/stderr/exit code;
- enforce timeout;
- support controlled cancellation;
- kill child process tree if required;
- persist execution state before/after process boundaries;
- prevent parallel execution in MVP;
- isolate the child process tree using a Windows Job Object or equivalent kill-on-close/process-group mechanism;
- construct a minimal scoped environment; do not blindly inherit broad credentials/tokens;
- Bridge is the **sole remote result publisher** for MVP automated execution after `ResultInspector` passes; Agent subprocesses receive no result/event/review publisher credential and no unrestricted Git credential-helper access;
- Agent CLI authentication, if required, is a separately attested capability and must not expose Bridge publisher, provider, Owner or review-writer credentials;
- Job Object/process-group containment is not filesystem isolation: attest the actual sandbox/OS-account/ACL boundary, readable paths and permitted secret/auth scope before launch; if sufficient isolation cannot be demonstrated, automated execution remains blocked;
- record executable path, command hash/arguments in sanitized form, PID/process start identity and resolved runtime configuration;
- on cancellation/timeout/restart, reconcile and terminate only the owned process tree, never unrelated user processes.

MVP concurrency:

```text
MAX_ACTIVE_EXECUTIONS = 1
```

### 6.9 ResultInspector

After Agent exit, inspect actual Git state.

Compare:

```text
authorized paths
vs
actual diff
```

ResultInspector MUST NOT accept Agent self-report as authority for changed paths.

### 6.10 GitDeliveryVerifier

After `ResultInspector` passes, the **Bridge** creates/pushes the authorized result commit and then verifies remote reality against the **authorized base and exact immutable result commit**. Required checks include:

- remote branch resolves to the expected full result SHA;
- result SHA descends from the authorized base commit and does not contain an unexpected rebase/alternate ancestry;
- actual changed paths from `base..result` stay inside the task allowlist and outside denylist;
- mandatory report/manifest/evidence files are read from the exact remote result commit, not from the local working tree or moving branch head;
- raw remote blob bytes/hashes for material evidence match the submitted manifest/receipt;
- no unauthorized workflow/binary/secret path appears in the diff.

`LOCAL_HEAD == REMOTE_BRANCH_SHA` may be recorded as a convenience check but is **insufficient by itself**.

Only after all required remote checks:

```text
REMOTE_PUSH_VERIFIED = YES
RESULT_STATE = PUSHED_UNREVIEWED
```

A local commit is never equivalent to a remote-delivered result.

**Authority separation:** GitDeliveryVerifier for task result source/code branches still requires that task's own verified `CODE_ALLOWED/GIT_CODE_PUSH` or separately scoped report permission. The Owner's standing grant on the Bridge review-event branch grants only sanitized event metadata publication under §3.3, never recovered source-code checkpoint push. Result code push and review-event push are independent branches, grant records, inspections and remote receipts.

### 6.11 ReviewOutbox

After remote result verification, write a durable outbox row keyed by `REVIEW_KEY = FOX2:<WP_ID>:<RESULT_COMMIT_SHA>` in the same local durability boundary that records delivery completion. Event publication uses retryable idempotent outbox delivery. A crash after verification but before event push must leave an unsent outbox record that is reconciled on restart; never lose the review signal.

### 6.12 ReviewEventEmitter

Only after verified remote result push and durable outbox creation, emit:

```text
FOX2_REVIEW_READY
```

bound to exact full remote SHA.

**ReviewEventEmitter execution condition:** Bridge event output is permitted on the existing standing-grant branch only after verified task-result remote SHA, verified Bridge Git identity/scope, exact one-event path, no secret exposure, CAS/idempotency and fast-forward remote readback. A failed event push remains retryable in durable outbox; it cannot create a second semantic review receipt.

### 6.13 CHAT-side ReviewReceiptWriter

This component is **CHAT-side** and never runs with Bridge identity. Bridge may emit/reconcile review events but cannot write semantic review receipts.

Before semantic review, manual and scheduled CHAT review paths acquire one durable review claim keyed by `REVIEW_KEY`. A competing claimant reconciles/waits rather than running an independent competing review. CHAT review receipts are immutable per `REVIEW_KEY`. Creation uses compare-and-set semantics against the configured review branch/path: if no authoritative receipt exists, create exactly one; if an identical receipt exists, return `ALREADY_REVIEWED`; if a conflicting receipt exists, return `REVIEW_RECEIPT_CONFLICT` and require CHAT resolution. Never silently overwrite a receipt. Supersession is a separate lineage record referencing prior and successor review keys/result SHAs and an explicit CHAT disposition; timestamp/newer ancestry alone never suppresses an earlier result.

### 6.14 LocalLedger

SQLite:

```text
C:\Projects\FOX2-AgentBridge\data\bridge.db
```

Minimum entities:

```text
dispatches
executions
review_outbox
review_events
review_receipts_cursor
```

Critical unique constraints:

```text
dispatch_id UNIQUE
review_key UNIQUE
```

---

## 7. Dispatch contract

Dispatch technical contract for v0.3 uses a **version-neutral Policy binding** and requires a schema revision before executable Bridge certification. The existing released companion schema v1.1 is historical to Policy V1.8.1 and MUST NOT be reused if it hardcodes that Policy version.

Candidate target:

```text
FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v1.2-CANDIDATE
```

The actual schema file/version, version-neutral fixtures and negative fixtures must be separately created, validated and pinned **before Gate A validation**; this specification does not claim that file already exists.

Required conceptual structure:

```json
{
  "schema_version": "1.2",
  "project": "FOX2",
  "dispatch_id": "FOX2-DISPATCH-...",
  "dispatch_action": "EXECUTE_LOCAL_AGENT",
  "wp_id": "...",
  "agent_configuration": {
    "agent_product": "CODEX|COPILOT",
    "engine_model": "...",
    "thinking_or_optimize_for": "..."
  },
  "policy_binding": {
    "policy_id": "FOX2-POLICY-V1",
    "version": "<exact released version>",
    "raw_sha256": "<64-hex>",
    "release_manifest": "<immutable identity>",
    "git_path": "<path>",
    "git_commit_sha": "<40-hex>"
  },
  "task": {},
  "prompt": {},
  "source": {},
  "decision_receipt": {},
  "selection_receipt": {},
  "runtime_contract": {},
  "max_runs": 1
}
```

Bridge MUST verify exact prompt hash before execution.

---

## 8. CHAT → Bridge transport

CHAT does not connect directly to the local machine.

Transport:

```text
CHAT
  ↓
GitHub outbound API/write
  ↓
work/FOX2-LOCAL-DISPATCH-chat
  ↓
local Bridge outbound fetch/poll
```

Benefits:

- no static IP;
- no inbound firewall rule;
- no local public port;
- no NAT traversal;
- durable Git audit trail;
- immutable commit identity.

The Git commit containing a dispatch is the transport identity.

---

## 9. Agent execution

### 9.1 Codex

Bridge shall detect the installed Codex CLI capabilities at runtime.

Use non-interactive execution only when the locally installed CLI exposes the required capability.

Bridge must pin:

```text
working directory
selected model
selected effort/mode where supported
prompt
runtime restrictions
```

### 9.2 Copilot

Bridge shall detect installed Copilot CLI capabilities at runtime.

Use actual supported CLI arguments for:

```text
non-interactive prompt
model
machine-readable output
no interactive question mode
```

Do not invent a Thinking level not exposed by Copilot.

---

## 10. Agent Result Contract

Agent may produce implementation and test evidence, but maximum result state before independent CHAT review is:

```text
PUSHED_UNREVIEWED
```

Agent MUST NOT issue:

```text
ACCEPTED
INTEGRATED
MERGED
RELEASED
```

as governance decisions.

Mandatory result files remain:

```text
reports/<WP_ID>/report.md
reports/<WP_ID>/evidence_manifest.json
```

---

## 11. Automated review-return channel

### 11.1 Remote result verification

Flow:

```text
Agent done
  ↓
Bridge ResultInspector validates scope/evidence
  ↓
Bridge creates authorized result commit
  ↓
Bridge pushes task branch
  ↓
Bridge verifies remote full SHA
  ↓
PUSHED_UNREVIEWED
```

### 11.2 REVIEW_READY schema

Bridge emits:

```json
{
  "schema_version": "1.0",
  "event_type": "FOX2_REVIEW_READY",
  "project": "FOX2",
  "wp_id": "...",
  "dispatch_id": "...",
  "agent_product": "CODEX|COPILOT",
  "result_branch": "work/...",
  "result_commit_sha": "<40-char remote SHA>",
  "report_path": "reports/<WP_ID>/report.md",
  "manifest_path": "reports/<WP_ID>/evidence_manifest.json",
  "result_state": "PUSHED_UNREVIEWED",
  "remote_push_verified": true,
  "review_requested": true,
  "created_by": "FOX2_LOCAL_BRIDGE"
}
```

Review identity:

```text
REVIEW_KEY = FOX2:<WP_ID>:<RESULT_COMMIT_SHA>
```

### 11.3 Event storage

```text
branch:
work/FOX2-REVIEW-EVENTS-bridge

path:
review_events/<WP_ID>/<RESULT_COMMIT_SHA>.json
```

---

## 12. GitHub review trigger

GitHub Action:

```text
.github/workflows/fox2-review-ready.yml
```

Trigger:

```text
push to work/FOX2-REVIEW-EVENTS-bridge
path review_events/**/*.json
```

GitHub Action responsibilities are mechanical only:

- parse JSON;
- validate schema;
- verify result commit exists;
- verify mandatory result files exist at exact SHA;
- check WP/dispatch/path consistency;
- dedupe review event;
- publish/update Review Queue.

GitHub Action MUST NOT decide semantic acceptance.

Recommended permissions:

```yaml
permissions:
  contents: read
  issues: write
```

No `contents: write` unless later justified.

---

## 13. Review Queue

GitHub Issue is a lightweight queue/index, not authority and **not the durable source of truth**. Durable review discovery comes from immutable `review_events/**` plus the local/remote reconciliation cursor. If Issue publication fails, the event remains pending and must be retried/reconciled.

Title example:

```text
[FOX2][REVIEW_READY] <WP_ID> @ <SHORT_SHA>
```

Labels:

```text
fox2
chat-review-ready
agent-codex | agent-copilot
```

Issue contains:

```text
WP_ID
dispatch_id
result branch
result full SHA
report path
manifest path
REVIEW_KEY
```

Do not copy large evidence into the issue.

---

## 14. CHAT automated review

### 14.1 Review Watch

A ChatGPT scheduled/condition watch may periodically inspect FOX2 review-ready items **only after a capability pilot proves that the active environment can perform the required background Git/Issue reads and, where applicable, write the authoritative CHAT review receipt**. Until that pilot passes, use manual CHAT review while preserving the same `REVIEW_KEY` and receipt semantics.

MVP scheduling:

```text
hourly maximum cadence
```

If no unseen review is available:

```text
NO_NOTIFICATION
```

### 14.2 Intake gate

Before semantic review:

```text
REVIEW_EVENT_SCHEMA          PASS
RESULT_COMMIT_EXISTS         YES
REPORT_EXISTS                YES
MANIFEST_EXISTS              YES
WP_MATCH                     YES
DISPATCH_MATCH               YES
POLICY_BINDING_MATCH         YES
SOURCE_BINDING_MATCH         YES
```

Failure:

```text
BLOCKED_INTAKE
```

### 14.3 Independent review pipeline

```text
REVIEW_INTAKE
  ↓
SCOPE_REVIEW
  ↓
ACTUAL_DIFF_REVIEW
  ↓
TEST_REVIEW
  ↓
ACCEPTANCE_REVIEW
  ↓
SECURITY_REVIEW
  ↓
VERDICT
```

CHAT reviews the immutable `RESULT_COMMIT_SHA`, never a moving branch head.

### 14.4 Actual Git diff is authority

CHAT compares:

```text
authorized base SHA
→ exact result SHA
```

Actual changed paths override Agent-reported changed paths.

### 14.5 Test evidence

Distinguish:

```text
CLAIMED_TEST
EVIDENCED_TEST
```

No evidence means:

```text
UNVERIFIED
```

Never synthesize PASS.

### 14.6 Acceptance mapping

Each acceptance criterion should map:

```text
Requirement
→ implementation
→ test
→ evidence
→ verdict
```

Missing mapping:

```text
ACCEPTANCE_GAP
```

### 14.7 Security review

At minimum:

- credentials/secrets;
- `.env`;
- private keys/tokens;
- raw licensed/private data;
- unexpected binaries;
- unauthorized workflow permissions;
- forbidden paths;
- dangerous shell/CI changes.

---

## 15. Review verdicts

Only:

```text
ACCEPTED
ACCEPTED_PARTIAL
REWORK
BLOCKED
```

### ACCEPTED

Implementation/evidence satisfy the WP.

May set:

```text
integration_eligible = true
```

but MUST NOT imply merge authorization.

### ACCEPTED_PARTIAL

A bounded subset/evidence objective is accepted while explicitly named gates remain open. The receipt MUST record `accepted_scope`, `remaining_open_gates` and why downstream work is or is not eligible. It is never equivalent to full acceptance.

### REWORK

Task is repairable within bounded scope.

CHAT may prepare a rework prompt, but MUST NOT automatically dispatch it.

### BLOCKED

Material source, Policy, scope, security, or architecture issue prevents continuation.

---

## 16. CHAT review receipt

Path:

```text
branch:
work/FOX2-CHAT-REVIEWS

file:
reviews/<WP_ID>/<RESULT_COMMIT_SHA>.json
```

Conceptual schema:

```json
{
  "schema_version": "1.0",
  "review_key": "FOX2:<WP_ID>:<SHA>",
  "project": "FOX2",
  "wp_id": "...",
  "dispatch_id": "...",
  "authorized_base_sha": "...",
  "source_commit_sha": "...",
  "policy_binding": {"version": "...", "raw_sha256": "...", "git_commit_sha": "..."},
  "result_commit_sha": "...",
  "reviewer": {
    "role": "CHAT",
    "type": "INDEPENDENT_REVIEW"
  },
  "checks": {
    "intake": "PASS",
    "scope": "PASS",
    "diff": "PASS",
    "tests": "PASS",
    "acceptance": "PASS",
    "security": "PASS"
  },
  "verdict": "ACCEPTED|ACCEPTED_PARTIAL|REWORK|BLOCKED",
  "integration_eligible": false,
  "merge_authorized": false,
  "deployment_authorized": false
}
```

Review receipt is immutable per `REVIEW_KEY`.

---

## 17. Queue lifecycle

Operational labels:

```text
chat-review-ready
  ↓
chat-reviewing
  ↓
chat-reviewed-accepted
chat-reviewed-rework
chat-reviewed-blocked
```

Labels are operational UI only.

Authority remains:

```text
immutable result commit
+
CHAT review receipt
```

---

## 18. Rework chain

MVP rule:

```text
AUTO_REWORK_DISPATCH = NO
```

Example:

```text
Dispatch 001
→ Result A
→ CHAT Review A = REWORK
→ Rework Prompt prepared
→ Owner confirmation required
→ Dispatch 002
→ Result B
→ CHAT Review B
```

Rework result should reference its predecessor.

---

## 19. Review dedupe and supersession

Review dedupe key:

```text
FOX2:<WP_ID>:<RESULT_SHA>
```

If an identical authoritative receipt exists:

```text
ALREADY_REVIEWED
```

If a conflicting receipt exists for the same `REVIEW_KEY`:

```text
REVIEW_RECEIPT_CONFLICT
```

Do not overwrite. CHAT must resolve the conflict and preserve both evidence pointers.

If multiple results arrive for the same WP:

- do not automatically discard an older result;
- a newer result may supersede an older unreviewed result only when lineage is proven;
- otherwise review states remain separate.

---

## 20. State machines

### 20.1 Dispatch/execution

```text
NEW
→ VERIFIED
→ RUNTIME_ATTESTED
→ RUNNING
→ AGENT_DONE
→ RESULT_LOCAL_READY
→ PUSHED_UNREVIEWED
```

Failure states:

```text
LOCAL_RUNTIME_BLOCKED
AGENT_FAILED
PUSH_BLOCKED
CANCELLED
DISPATCH_DUPLICATE_IGNORED
```

### 20.2 Review

```text
REVIEW_READY
→ REVIEW_INTAKE
→ CHAT_REVIEWING
→ ACCEPTED | ACCEPTED_PARTIAL | REWORK | BLOCKED
```

Additional infrastructure states:

```text
REVIEW_EVENT_INVALID
QUEUE_PUBLISH_FAILED
BLOCKED_INTAKE
REVIEW_DELIVERY_UNVERIFIED
ALREADY_REVIEWED
```

---

## 21. Failure behavior

### 21.0 Crash/restart invariants

- A claimed dispatch is never automatically relaunched merely because the Bridge restarted.
- Non-terminal ledger state is reconciled against process identity, worktree Git state and remote refs.
- Ambiguous ownership/state becomes `RECOVERY_REQUIRED`; human/CHAT resolution is required.
- Verified remote result with unsent review event is recovered from `review_outbox`; review discovery must not be lost.
- Review receipt write is idempotent/CAS and cannot silently overwrite a prior receipt.


| Failure | Required state |
|---|---|
| Invalid dispatch schema | `LOCAL_RUNTIME_BLOCKED` |
| Prompt hash mismatch | `LOCAL_RUNTIME_BLOCKED` |
| Wrong repo/project | `LOCAL_RUNTIME_BLOCKED` |
| Requested model unavailable | `LOCAL_RUNTIME_BLOCKED` |
| Duplicate dispatch | `DISPATCH_DUPLICATE_IGNORED` |
| Agent non-zero exit | `AGENT_FAILED` |
| Forbidden diff | no result push / `PUSH_BLOCKED` or blocked result |
| Remote SHA mismatch | `REMOTE_PUSH_UNVERIFIED` |
| Review event invalid | `REVIEW_EVENT_INVALID` |
| Review queue unavailable | event retained; queue degraded |
| CHAT watch offline | durable event remains pending |
| Report missing | `BLOCKED_INTAKE` |
| Manifest invalid | `BLOCKED_INTAKE` |
| Secret detected | `BLOCKED` |
| Existing review receipt | `ALREADY_REVIEWED` |

No failure state may become ACCEPTED implicitly.

---

## 22. Security boundaries

### CHAT

May:

- publish authorized dispatch;
- read result;
- write review receipt;
- update review queue.

Not implied:

- main merge;
- deployment;
- automatic rework dispatch;
- LIVE/broker operation.

### Bridge

- use the minimum credential scope necessary for control-branch read, authorized result push and review-event publication;
- separate Bridge/service credentials from Agent subprocess environment where possible;
- never expose broad GitHub tokens, provider secrets or Owner credentials to the Agent prompt/stdout/stderr;
- sanitize environment/logging and store only required identifiers/hashes;
- process/worktree ownership must be attributable to the dispatch ledger entry.

May:

- read control branch;
- create isolated worktree;
- invoke selected Agent;
- validate local/remote Git state;
- push authorized task result;
- publish review event.

Not implied:

- alter Policy/BRD;
- re-route task;
- change Agent/model silently;
- push main;
- merge;
- deploy;
- write CHAT review receipt.

### Agent

May operate only within its authorized task/worktree/path contract.

Agent cannot self-accept.

### GitHub Action

Mechanical validator/queue publisher only.

No semantic acceptance.

---

## 23. Token/credit efficiency

Review Watch should not scan the full repo on every run.

Preferred flow:

```text
read incremental review-event cursor
  ↓
read authoritative CHAT review receipts for candidate keys
  ↓
reconcile durable event ↔ receipt state
  ↓
unseen immutable result remains?
  ├─ NO → STOP
  └─ YES
       ↓
    intake exact RESULT_COMMIT_SHA / REVIEW_KEY
       ↓
    validate event + task/source/policy binding
       ↓
    read exact result files + authorized-base diff
       ↓
    load only necessary Policy/BRD sections
```

`Issue`/label state may accelerate discovery but is never the STOP condition. `NO → STOP` is permitted only **after durable review-event ↔ authoritative-receipt reconciliation** proves there is no unseen result. Implementations should use an incremental cursor/delta rather than scan the full repository.

Do not reread the entire Policy when an exact Policy hash/version binding is already verified and only a scoped section is needed.

---

## 24. Implementation work packages

### 24.0 Phase prerequisite rule

A later phase cannot be certified solely because its code exists. Each phase requires the preceding gate evidence plus its own negative tests. In particular: receive-only trust/provenance precedes execution; durable claim/recovery precedes Agent launch certification; remote blob/ancestry verification precedes `REVIEW_READY`; durable review event reconciliation precedes queue automation; and background CHAT review capability must be piloted before closed-loop certification.


### Phase 0 — Machine readiness

**BRG-001 — Local prerequisite audit/install**

- Git;
- PowerShell;
- Python;
- gh;
- Codex CLI;
- Copilot CLI;
- VS Code;
- auth and PATH;
- create Bridge root/venv/worktree root.

No FOX2 source modification.

### Phase 1 — Receive-only Bridge

**BRG-010 — Bridge Core**
- Python package;
- config;
- logging;
- SQLite;
- process lock.

**BRG-020 — Dispatch Poller**
- poll control branch;
- discover immutable dispatch.

**BRG-030 — Dispatch Validator**
- Schema v1.2 Candidate;
- hash/identity validation;
- replay guard.

**BRG-040 — Runtime Attestation**
- CLI/auth/Git/repo/branch/base/model/WIP/writer checks.

Checkpoint A result:

```text
CHAT → Git → Local Bridge
```

works, but Agent is not launched.

### Phase 2 — Local Agent execution

**BRG-050 — Worktree Manager**

**BRG-060 — Codex/Copilot Adapters**

**BRG-070 — Execution Supervisor**

**BRG-080 — Result Inspector / Contract**

Checkpoint B:

```text
Bridge → Agent → local result
```

works, initially without remote result delivery.

### Phase 3 — Git result delivery

**BRG-090 — Task result commit/push**

**BRG-091 — Remote Push Verification**

Checkpoint C:

```text
Agent → GitHub → PUSHED_UNREVIEWED
```

### Phase 4 — Review event and queue

**BRG-092 — Review Event Schema**

**BRG-093 — Review Event Emitter + branch**

**BRG-094 — GitHub Action mechanical validator**

**BRG-095 — GitHub Issue Review Queue**

Checkpoint D:

```text
GitHub result → REVIEW_READY → queue
```

### Phase 5 — CHAT review loop

**BRG-096 — CHAT Auto Review Intake Contract**

**BRG-097 — Immutable-SHA Review Algorithm**

**BRG-098 — Review Receipt Schema/Writer**

**BRG-099 — REWORK/BLOCKED routing**

### Phase 6 — Certification

**BRG-100 — Independent closed-loop audit**

**BRG-101 — E2E certification**

**BRG-102 — Enable scheduled Review Watch / autostart**

---


### 24.1 Control acceptance ownership added by WORK redline

- **BRG-010:** singleton/process ownership and durable ledger boundary; restart must not create a second active owner.
- **BRG-030:** schema v1.2 Candidate, selected trust mechanism/provisioning, same `dispatch_id` with different payload negative case, raw-byte validation.
- **BRG-050:** exact-base worktree creation, moving-branch race rejection, Windows path/junction collision and ownership checks.
- **BRG-060/070:** requested/resolved/observed Agent configuration, sandbox/credential boundary, timeout/cancel/crash recovery and owned process-tree termination.
- **BRG-080/090:** ResultInspector must pass before Bridge publication; Agent cannot bypass Inspector or directly push with publisher credentials.
- **BRG-091:** repository/ref/base ancestry, exact remote commit and raw remote blob readback.
- **BRG-093/095:** outbox retry/idempotency plus event↔queue↔receipt reconciliation without Issue dependence.
- **BRG-096/098:** durable review claim, receipt CAS/conflict, full immutable binding and explicit supersession disposition.
- **BRG-100/101:** negative evidence for trust, isolation, replay, branch race, claim race and missing-queue recovery; not happy-path-only.
- **BRG-102:** capability pilot PASS for background read → exact review → authenticated receipt write → remote readback before closed-loop enablement.


## 25. Release gates

### Gate A — Transport / trust provenance

```text
CHAT → Git dispatch → Bridge receive/validate
```

No Agent launch.

### Gate B — Local execution / durable claim and isolation

```text
Bridge → Agent → local result
```

No automatic result push initially.

### Gate C — Result delivery / remote bytes and ancestry

```text
Agent → Git result → remote SHA verified
```

### Gate D — Review signal / durable outbox and reconciliation

```text
remote result → REVIEW_READY → queue
```

### Gate E — CHAT review dry-run / receipt CAS

CHAT reviews result but does not write review receipt automatically.

### Gate F — Closed-loop production / capability pilot

Enable:

- automatic review receipt;
- queue state update;
- scheduled Review Watch;
- Bridge autostart.

Still disabled:

```text
AUTO_REWORK_DISPATCH
AUTO_MERGE
AUTO_DEPLOY
```

---

## 26. Core acceptance criteria

- `AC-BRG-001`: Bridge accepts FOX2 only.
- `AC-BRG-002`: No inbound local port required.
- `AC-BRG-003`: Main FOX2 workspace is never used as Agent worktree.
- `AC-BRG-004`: Dispatch hashes are verified before execution.
- `AC-BRG-005`: Governance decision checks are not duplicated by Bridge.
- `AC-BRG-006`: Requested Agent/model/mode cannot be silently substituted.
- `AC-BRG-007`: A dispatch runs at most once.
- `AC-BRG-008`: Actual Git diff is validated against authorized paths.
- `AC-BRG-009`: Remote result full SHA is independently verified.
- `AC-BRG-010`: Agent maximum pre-review state is `PUSHED_UNREVIEWED`.
- `AC-BRG-011`: REVIEW_READY pins immutable remote result SHA.
- `AC-BRG-012`: GitHub Action performs no semantic acceptance.
- `AC-BRG-013`: CHAT reviews exact immutable SHA.
- `AC-BRG-014`: Scheduled/manual CHAT reviews dedupe.
- `AC-BRG-015`: REWORK never auto-dispatches.
- `AC-BRG-016`: ACCEPTED never auto-merges.
- `AC-BRG-017`: Review receipt remains distinct from Agent result.
- `AC-BRG-018`: Queue outage cannot destroy the underlying review event.
- `AC-BRG-019`: Bridge restart cannot replay a completed dispatch.
- `AC-BRG-020`: No secret is written to queue/review receipts.

---

## 27. Mandatory negative tests

1. Dispatch project != FOX2 → BLOCK.
2. Repo != `dunglt2505/FOX2` → BLOCK.
3. Policy hash mismatch → BLOCK.
4. Prompt hash mismatch → BLOCK.
5. Task/source hash mismatch → BLOCK.
6. Branch points to main → BLOCK.
7. Requested Agent CLI missing → BLOCK.
8. Requested model unavailable → BLOCK.
9. WIP/writer collision → BLOCK.
10. Duplicate dispatch → IGNORE.
11. Agent exits non-zero → FAILED.
12. Agent touches forbidden path → no normal push.
13. Agent claims PASS without executed evidence → CHAT does not accept claim.
14. Remote result SHA differs from local → unverified.
15. Fake REVIEW_READY SHA → reject.
16. Missing `report.md` → BLOCKED_INTAKE.
17. Invalid manifest → BLOCKED_INTAKE.
18. Duplicate REVIEW_READY → dedupe.
19. CHAT review receipt already exists → skip.
20. Secret in result/evidence → BLOCKED.
21. Agent writes `ACCEPTED` itself → ignored/violation.
22. REWORK result auto-launch attempt → prohibited.
23. ACCEPTED result attempts automatic main merge → prohibited.

---

## 28. Owner interaction model

Execution Routing Selector remains:

### Screen 1
- `MANUAL_VSCODE`
- `CONFIGURE_AUTOMATED_AGENT`

Manual VS Code ends Bridge routing.

### Screen 2
Owner confirms:
- Agent;
- model;
- Thinking/Optimize mode actually supported.

### Screen 3
- `DISPATCH_VIA_LOCAL_BRIDGE`
- `BACK_TO_AGENT_CONFIGURATION`
- `CANCEL_EXECUTION`

Only explicit confirmed Bridge selection creates a dispatch.

If native Intelligent UI is not actually rendered, the UI layer must use clearly identified text fallback semantics rather than pretending Unicode symbols are native controls.

---

## 29. Relationship to FOX2 Policy

This Technical Specification is subordinate implementation design. It translates Policy requirements into concrete mechanisms but does not itself authorize execution.

- Policy defines **what must be true**: authority, gates, evidence properties, state/verdict semantics, STOP/release boundaries.
- BRD/Data Contract/Acceptance define **what the product must do**.
- This specification defines **how the Bridge implements those constraints**.
- If this specification conflicts with Policy or BRD, stop the affected implementation and correct the Technical Specification.
- Technical version changes do not require Policy/BRD version changes unless their owned semantics change.
- Candidate v0.3 is designed against the governance decisions in FOX2 Policy V1.8.2 Candidate REV3, but neither candidate is effective until separately approved/released. [HISTORICAL, SUPERSEDED]: this sentence described the earlier v0.3 candidate checkpoint; the active FOX2 Policy now is V1.8.2 RELEASED_EFFECTIVE.

## 30. Historical v0.3 Candidate decision summary — NOT CURRENT AUTHORITY

> **Historical provenance only.** This section preserves the wording and design dispositions of the earlier v0.3 Candidate review and may contain superseded Policy/version or candidate statuses. It does not override this v0.4 released header, current Policy V1.8.2, §§32–36, or an immutable WP-specific binding.

v0.3 intentionally chooses:

```text
FOX2-only implementation
single Windows host
single active execution
GitHub as outbound-only message bus
Git control branch for CHAT → Bridge
isolated Git worktrees
Codex/Copilot CLI adapters
Result Contract v2
verified remote result SHA
REVIEW_READY event branch
GitHub Issue review queue
scheduled CHAT independent review
no auto-rework
no auto-merge
no auto-deploy
```

**This is deliberately not a generic Trading Bridge framework.**


## 31. Historical v0.3 WORK audit finding closure map — design dispositions only

| WORK finding | v0.3 disposition |
|---|---|
| F01 stale Policy/schema version coupling | Move Policy version to data-driven binding; require dispatch schema revision before Gate B. |
| F02 self-declared publisher/Owner confirmation | Add TrustAnchorVerifier and authenticated decision provenance gate. |
| F03 Agent/credential/push isolation | Add scoped credential/environment/process isolation requirements. |
| F04 weak HEAD/SHA verification | Require authorized-base ancestry, remote exact blobs/hashes and actual diff verification. |
| F05 crash between claim/launch | Add durable pre-spawn claim, recovery reconciliation and no automatic ambiguous replay. |
| F06 state/verdict/receipt inconsistency | Add `ACCEPTED_PARTIAL`; separate delivery, review and authority states. |
| F07 review receipt race/supersession | Add immutable per-REVIEW_KEY CAS receipt and explicit supersession lineage. |
| F08 Issue-only discovery loss | Make immutable review event/outbox + reconciliation cursor durable source; Issue is index only. |
| F09 unproven background review/write | Gate closed-loop on explicit capability pilot; manual fallback preserved. |
| F10 requested vs actual model | Persist requested/resolved/observed configuration separately; mismatch blocks. |
| F11 phase prerequisites | Add phase prerequisite rule and strengthen Gates A–F. |

All items remain **design candidates / NOT RUN** until implemented and evidenced.

---

## 32. v0.4 released technical delta — standing Bridge Git event writer

### 32.1 Scope and immutable authority

- Evidence: Owner standing grant `FOX2_BRIDGE_STANDING_GIT_BRANCH_GRANT_20261013.md` at Git commit `bcd78aabeaf7817b7d9b682a0180445293061f41`, blob `ca2d414c0daacda1ba5a20ed963e1eb314e7cc7b`; intended output ref `refs/heads/work/FOX2-REVIEW-EVENTS-bridge` exists and was read back at full SHA `c9dc41b97ca8bc58f06cc2f3701832ba083422e3`.
- Grant applies to one branch, one authenticated Bridge service identity on authorized FOX2 Windows host, one technical message family: `review_events/<WP_ID>/<RESULT_COMMIT_SHA>.json`. No code files, raw local worktree, secrets, DB or logs. Extra metadata families require Technical-path-contract review before use; cannot infer permission by directory prefix or branch ownership alone.
- No repeat Owner approval for the **same granted class** of review-event push; every push still requires automatic, noninteractive runtime verification. Any material change in identity/host/repo/branch/path/contract or security posture requires new routing/decision.
- Distinguish `OWNER_STANDING_GIT_SCOPE_GRANTED=YES`, `GITHUB_REF_EXISTS=YES`, `BRIDGE_GIT_AUTHORIZATION_OBSERVED=UNKNOWN`, `REPO_SIDE_BRANCH_ENFORCEMENT=NOT_PROVEN`, `BRIDGE_ORIGIN_PUSH_TEST=NOT_RUN`, `AUTOMATED_GATE_A=BLOCKED_CAPABILITY_UNAVAILABLE`. Branch creation and an Owner-signed grant do not establish GitHub-enforced writer restrictions.

### 32.2 EventWriter per-push algorithm

1. Require completed, verified remote task result and outbox `REVIEW_KEY=FOX2:<WP_ID>:<RESULT_COMMIT_SHA>`; never emit before canonical result verification.
2. Resolve the standing grant and verify configured service identity, local credential owner, exact repository/branch, verified expected branch tip and exclusive Bridge writer lease. If scope/identity uncertain, `BLOCKED_GIT_TRUST`, no push.
3. Render deterministic JSON at a path exactly matching `review_events/<WP_ID>/<RESULT_COMMIT_SHA>.json`; reject unrelated filenames, symlink/junction paths, unexpected file sizes, credential-bearing strings, code/diff attachment and mismatch of event identity.
4. Fetch/inspect the current branch ref, verify ancestry against previously accepted tip, perform compare-and-set style fast-forward commit; never force push, overwrite an existing incompatible event, or mutate branches owned by CHAT or another Agent.
5. Re-fetch remote branch, compare full SHA, ancestry and raw JSON blob hash to local receipt. Persist `EVENT_PUSH_VERIFIED` with full branch SHA and event hash; on network/permission failure preserve local durable outbox and return `EVENT_PUSH_PENDING/BLOCKED` rather than claiming review ready.
6. On restart reconcile by `REVIEW_KEY`; same exact event is idempotent, conflict yields `REVIEW_EVENT_CONFLICT`, no automatic escalation.

The GitHub account's broad write credential (if any) may not enforce one-branch restriction at server side; policy/Bridge-process allowlisting is defense in depth, NOT a substitute for Gate A authenticated enforced control-plane provenance. A synthetic positive/negative scoped pilot on the authorized output branch is required before claiming working Bridge push.

## 33. v0.4 released technical delta — quota exhaustion, checkpoint and successor handoff

### 33.1 Error classification and invariants

Source: `BRIDGE_QUOTA_RECOVERY_DELTA_v0.1_CANDIDATE.md` Git commit `25179960861e142bb973aa7a5538b067a17112cf` (separate Candidate reference). Quota/Agent API access must be decoupled from Bridge Git transport. Classify errors only using observed CLI/provider evidence:

`QUOTA_EXHAUSTED_CONFIRMED | RATE_LIMIT_RETRYABLE | AUTHENTICATION_FAILURE | NETWORK_FAILURE | AGENT_CRASH | PROCESS_CANCELLED | TOOL_UNAVAILABLE | UNKNOWN_INTERRUPTION`.

Generic HTTP 429, idle timeout, quota display gaps and transport failures are NOT proof of `QUOTA_EXHAUSTED_CONFIRMED`. Never consume paid tokens deliberately solely to probe availability. All requested/resolved/observed product/model/mode and actual quota data or `UNKNOWN` are distinct. Preserve one writer, no silent Agent substitution, no unsafe WIP cleanup.

### 33.2 Recovery state machine

`RUNNING → INTERRUPTION_OBSERVED → PROCESS_STOPPING → WORKTREE_QUIESCED → INVENTORY_COMPLETE → CHECKPOINT_VALIDATED → LOCAL_DURABLE → PUSH_PENDING → CHECKPOINT_PUSHED_PARTIAL → HANDOFF_REVIEW_PENDING`.

For process still writing/unknown handle, `QUARANTINED_UNSAFE_WIP`; for unsafe paths or secrets, `CHECKPOINT_BLOCKED_INSPECTION`; for missing scoped code-push permission, `BLOCKED_GIT_GRANT` with local durable checkpoint only; for missing Git remote access, `PUSH_PENDING_RETRYABLE`; for unverified/mismatched source, `BLOCKED_SOURCE_DRIFT`. These states do not count as result PASS, final delivery or CHAT acceptance.

### 33.3 Safe checkpoint + Git-plane separation

- Quiesce entire Agent process tree under exclusive supervisor lease before reading mutable worktree; inventory tracked, untracked and ignored candidate files without uploading secrets or unexpected binary data. Existing Owner worktree is never reset, cleaned, stashed, rebased or overwritten.
- Freeze source baseline, WP/dispatch ID, allowed-path set hash, source-commit/policy hash, requested/resolved/observed executor identity, interruption evidence redacted, exact diff/file SHA-256, observed test outcomes and remaining steps. Treat unfinished files as partial/quarantined until safely reviewed.
- Commit crash-safe local metadata/manifest (journal or atomic store) with idempotency key. Never rely on an Agent's self-description of completeness.
- **Actual source/code checkpoint** may be pushed only under a separate, exact-WP `GIT_CODE_PUSH` grant to its approved isolated *task code branch*. The one-branch standing review-event grant is **not** a shortcut. If such permission is absent, store safely locally and request scoped routing; no Git code push.
- **Sanitized checkpoint status events** on `work/FOX2-REVIEW-EVENTS-bridge` are *not yet authorized output formats by this candidate*: future event schema/paths need explicit Technical acceptance. Even then, they do not transport raw source/WIP.
- Git checkpoint remote SHA + ancestry + changed-path raw blob verification precedes `CHECKPOINT_PUSHED_PARTIAL`; full canonical result delivery remains `PUSHED_UNREVIEWED` after ResultInspector and report contract.
- Successor Copilot/Codex may read only a verified safe checkpoint with **new CHAT R0–R7**, current Policy/source, actual model/quota/host, new single-use Owner-approved dispatch and new isolated worktree. The Bridge cannot silently choose a new Agent or reuse the old grant, and no retry automatically broadens rights.

### 33.4 Recovery manifest minimum

`schema_version`, `wp_id`, `original_dispatch_id`, exact `source_commit_sha`, `policy_raw_sha256`, `allowed_path_set_hash`, `interruption_class`, `interruption_evidence_redacted`, `requested_executor`, `resolved_executor`, `observed_executor`, `writer_quiesced`, `changed_paths` with SHA-256/size/type, `test_observations`, `complete_verified`, `incomplete_or_unsafe`, `remaining_scope`, `local_checkpoint_id`, `checkpoint_state`, optional verified `remote_commit_sha`, optional `successor_dispatch_id`. All fields factual, absent observations `UNKNOWN/NOT_RUN`, no raw credentials.

### 33.5 Mandatory recovery acceptance (all NOT_RUN)

- `BRG-QF-01..04`: quota before write, mid-file, after tests before report, after report before push.
- `BRG-QF-05..08`: 429 vs quota, auth/network/crash, Git independent identity while quota exhausted, denied Git credential/remote.
- `BRG-QF-09..12`: replay idempotency, secret leak block, concurrent writer still active, source/allowlist drift.
- `BRG-QF-13..16`: successor quota absent, approved successor new dispatch, code checkpoint push without grant denied, ambiguous quota classification.
- `BRG-QF-17..20`: forbidden main/merge/PR, remote SHA/ancestry mismatch, incomplete tests not acceptance, crash after remote push before outbox replay.

Run synthetic offline fixtures first, with independently authorized and isolated test writes, followed by separate permissioned host pilot; no deliberate quota depletion. No claimed PASS until observed evidence.

## 34. BRG-002 evidence and BRG-003 source preservation plan

- Latest Owner-supplied Copilot BRG-002 inventory: 20 INCLUDE (`pyproject.toml`, `README.md`, 13 Python source, 5 test files) with recorded SHA-256; 3 REVIEW_REQUIRED (config example and 2 self-reported evidence reports), 3 runtime EXCLUDE (DB/lock/log), 52 generated EXCLUDE, `.venv` 2482 files excluded as a directory; 2 SQLite WAL/SHM sidecars emerged from a read-only SQLite open and remain untouched. Ledger/test discovery evidence is **Copilot-reported**, not independent Git source proof.
- Bridge code exists at `C:\Projects\FOX2-AgentBridge` but not in Git. BRG-010/020 reportedly partly built; 59 test IDs inventoried, old report says PASS but **not independently rerun**. No rewriting or loss of original source.
- BRG-003 preferred Git import destination (planning, not yet granted): `agent_bridge/` folder within `dunglt2505/FOX2` on a separate non-main source-baseline branch and isolated worktree. Never import the original runtime DB, logs, keys, temp, bare control.git, sidecars, cache, egg-info or venv. Existing source containing user-specific paths must undergo a scoped redaction/security review; separate raw snapshot with hashes before any approved edits.
- **BRG-003 code import is NOT covered** by the standing event-writer grant. CHAT must confirm a one-time scoped BRG-003 source-import grant, source-file allowlist, path ownership, actual writer/credential and result destination before any file copy/commit/push. Once the exact WP grant is effective, its own bounded commits need no reapproval per commit.
- Independently rerun offline 59 tests on a verified Git baseline with Python isolated test cache/temp under separately authorized operation, preserving originals. Treat Gate A trust-provenance and missing dispatch control branch as distinct issues; creating the branch alone does not pass Gate A.

## 35. v0.4 release/readiness disposition

This section describes **document release effectivity only**, not runtime acceptance. The status values for permissions and Gate A remain negative until separately evidenced.

- `POLICY_V1.8.2`: RELEASED_EFFECTIVE, unchanged.
- `BRIDGE_SPEC_V0.3`: SUPERSEDED for new Bridge document handoffs after v0.4 verified publication; immutable historical evidence, still pinned for prior WPs.
- `BRIDGE_SPEC_V0.4`: RELEASED_EFFECTIVE document baseline upon Library exact-byte release manifest and Git readback; no DEV, no Git code-push or runtime Bridge execution grant.
- `STANDING_OWNER_EVENT_BRANCH_GRANT`: YES for defined review-event metadata; `BRIDGE_REVIEW_EVENT_BRANCH_EXISTS`: YES; `BRIDGE_HOST_CREDENTIAL/BRIDGE_ORIGIN_PUSH`: UNKNOWN/NOT_VERIFIED.
- `BRG-003`: scope-design candidate, write permission absent pending routing/Owner release; `BRG-QF-01..20`: NOT_RUN.
- `AUTOMATED_GATE_A`: BLOCKED_CAPABILITY_UNAVAILABLE; release Gates B–F not certified from source inventory.
- STOP on source/role/quota/host/worktree mismatch, unauthorized code diff, WIP collision, secret exposure, failed remote readback, untrusted publisher, or attempting to expand standing grant to code or CHAT control branch.