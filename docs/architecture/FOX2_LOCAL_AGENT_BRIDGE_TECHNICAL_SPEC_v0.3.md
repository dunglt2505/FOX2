# FOX2 — Local Agent Bridge Technical Specification v0.3

**Document ID:** `FOX2-LOCAL-AGENT-BRIDGE-SPEC`  
**Version:** `0.3`  
**Project:** `FOX2 ONLY`  
**Status:** `RELEASED_EFFECTIVE / DESIGN_BASELINE / AUTOMATED_GATE_A_BLOCKED`  
**Date:** 2026-10-12  
**Purpose:** Technical implementation design for FOX2 local Agent dispatch, execution, Git result delivery, durable review discovery and CHAT review-return mechanics.  
**Parent technical candidate:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.3_CANDIDATE.md` (WORK-audited source); v0.2 remains earlier history.  
**Governance review counterpart:** `FOX2_POLICY_V1.8.2.md` (released governance authority).  
**Authority boundary:** This specification defines **HOW** Policy/BRD requirements are implemented. It does not create DEV, Git, merge, deployment, Production, broker, or LIVE authority; it cannot redefine BRD requirements or weaken Policy. Technical versions may evolve independently when governance/business semantics are unchanged.  
**Design decision:** FOX2-only. No multi-project registry, generic project abstraction, or cross-project runtime is included. A future project may clone/fork this Bridge implementation and adapt its project-specific bindings separately.

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

### 6.11 ReviewOutbox

After remote result verification, write a durable outbox row keyed by `REVIEW_KEY = FOX2:<WP_ID>:<RESULT_COMMIT_SHA>` in the same local durability boundary that records delivery completion. Event publication uses retryable idempotent outbox delivery. A crash after verification but before event push must leave an unsent outbox record that is reconciled on restart; never lose the review signal.

### 6.12 ReviewEventEmitter

Only after verified remote result push and durable outbox creation, emit:

```text
FOX2_REVIEW_READY
```

bound to exact full remote SHA.

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