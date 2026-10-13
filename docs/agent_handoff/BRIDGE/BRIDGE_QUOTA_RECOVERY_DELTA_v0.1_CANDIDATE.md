# FOX2 Bridge — Quota Exhaustion Recovery & Cross-Agent Handoff — Technical Delta Candidate v0.1

Status: CANDIDATE / DESIGN_ONLY / NOT_RELEASED / NO_DEV_GRANT
Date: 2026-10-13 (Asia/Ho_Chi_Minh)
Owner decision: user requested implementation of quota recovery and controlled Codex/Copilot handoff; Bridge is P0.
Parent: FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.3.md RELEASED_EFFECTIVE.
Authority: FOX2_POLICY_V1.8.2.md RELEASED_EFFECTIVE, policy raw SHA-256 552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc.
Exact released planning source commit: c9dc41b97ca8bc58f06cc2f3701832ba083422e3.
Scope: technical delta for BRG-050..091 plus BRG-100..102 tests. This candidate does not alter released v0.3, grant DEV, dispatch any Agent, authorize code push, grant merge or override blocked automated Gate A.

## 1. Requirement and trust invariants

- Quota exhaustion must not require remaining Codex/Copilot tokens to save the work already present in the isolated worktree.
- Bridge Git credentials and commit/push process must be operationally independent of Agent API quota. GitHub connectivity, write grants, local credentials and remote target remain independent gates.
- Only one live writer/process owns the worktree; checkpoint must freeze execution and exclude files being actively mutated. If termination/lock cannot be proven, STOP with QUARANTINED_UNSAFE_WIP.
- An executor can never self-assert authorized changed paths, successful tests, clean/complete files, success verdict, or handoff authority.
- No silent material substitution of agent, product, model or reasoning level. Re-route by CHAT R0-R7 against actual quota/access and Owner authority, issuing a newly signed/immutable dispatch with a successor worktree.
- Existing delivered and accepted evidence remains immutable. Partial checkpoint is not result acceptance and never counts as passing unrun tests.
- Bridge may only push an approved, sanitized checkpoint to a specifically permitted non-main checkpoint branch. An ordinary code write authorization, result report standing grant, or design release alone does not grant checkpoint code-diff push. If required permission unknown, local-only checkpoint and BLOCKED_GIT_GRANT.
- Local Bridge cannot bypass GitHub repository protections or fabricated control-plane trust; Gate A remains blocked until enforceable provenance is actually demonstrated.

## 2. Observable interruption classification

Capture exit code/signal, process termination, tool/version, sanitized stderr/stdout indicators, request/response metadata when available, and timestamp. Never infer quota exhaustion only from elapsed time or a generic process failure. Classification enum:

QUOTA_EXHAUSTED_CONFIRMED | RATE_LIMIT_RETRYABLE | AUTHENTICATION_FAILURE | NETWORK_FAILURE | AGENT_CRASH | PROCESS_CANCELLED | TOOL_UNAVAILABLE | UNKNOWN_INTERRUPTION.

For confirmed exhaustion require explicit provider/CLI evidence or uniquely documented tool output; store evidence excerpt with secrets redacted and confidence=CONFIRMED. Treat unclassified 429 as RATE_LIMIT_RETRYABLE until tool/provider semantics show quota depletion. If uncertain, UNKNOWN_INTERRUPTION; no automatic Agent switch. UI may show “quota unknown” with observed reason. Record remaining quota only if surfaced and verified, else UNKNOWN.

## 3. Recovery state machine

RUNNING → INTERRUPTION_OBSERVED → PROCESS_STOPPING → WORKTREE_QUIESCED → INVENTORY_COMPLETE → CHECKPOINT_VALIDATED → LOCAL_DURABLE → [GIT_GRANT_VERIFIED] → PUSH_PENDING → CHECKPOINT_PUSHED_PARTIAL → HANDOFF_REVIEW_PENDING → [fresh CHAT routing + Owner-approved transport] → SUCCESSOR_DISPATCH_READY.

Failure exits:
- PROCESS_STILL_ALIVE or ownership collision → QUARANTINED_UNSAFE_WIP (no commit/push).
- secrets, disallowed paths, binary/large files, symlinks escaping root, malformed/incomplete work → CHECKPOINT_BLOCKED_INSPECTION (local report only; never leak raw rejected contents).
- remote unavailable → PUSH_PENDING_RETRYABLE; retain locally durably, no claim remote delivery.
- permission/source mismatch → BLOCKED_GIT_GRANT / BLOCKED_SOURCE_DRIFT.
- not enough verified state to resume → HANDOFF_BLOCKED_UNKNOWN.
- no automatic successor dispatch, retries of code execution, PR, merge or LIVE.

## 4. Safe checkpoint algorithm

1. Detect explicit interruption or policy-constrained time/process signal, record the factual classification; do not kill a healthy executor just for suspected quota.
2. Stop accepting Agent writes; request graceful shutdown, then apply bounded safe termination under Bridge supervisor; verify child processes have exited, filesystem quiescence and exclusive ownership.
3. Snapshot authoritative baseline: WP_ID, dispatch ID, immutable source-policy hashes, base commit, branch, worktree root, allowed paths, current task grant, executor requested/resolved/observed config, git status (tracked/untracked/ignored), file hashes/diffs and tests actually observed. Inspect untracked files as well. Prevent accidental inclusion of ignored secrets and private market/account data.
4. Run ResultInspector against changed-path allowlist, sanitized output checks, evidence integrity, binary/size/symlink controls and provenance. Partial or potentially corrupt files may be retained in a protected local quarantine but are not marked resumable by default.
5. Persist atomic local checkpoint directory/record (write temp + fsync equivalent + atomic rename; WAL or journal where applicable), lock task to prevent duplicate recovery and save monotonically incremented recovery attempt.
6. If AND ONLY IF an independently verified scoped Git grant covers partial checkpoint and branch ownership: create an isolated checkpoint commit (not main, not release/result accepted branch), push with least-privilege Git identity, fetch remote readback and verify exact full SHA, base ancestry, content hashes, expected branch, report/manifest.
7. On push error, retain PUSH_PENDING and retry with bounded exponential backoff/idempotency key after revalidating grant and remote ancestry; do not rewrite or force-push.
8. Produce an immutable recovery receipt distinct from canonical complete Result Contract and notify CHAT via durable event/reconciliation if supported. Without remote readback status remains LOCAL_ONLY or PUSH_PENDING.
9. Handoff selection occurs only outside Bridge following fresh routing; successor always works from a new isolated worktree/base and explicitly scoped checkpoint import. Never reuse a dirty predecessor worktree.

## 5. Minimum checkpoint manifest

```json
{
  "schema_version": "fox2.bridge.recovery.v0.1",
  "kind": "PARTIAL_RECOVERY_CHECKPOINT",
  "wp_id": "FOX2-...",
  "original_dispatch_id": "...",
  "source_commit_sha": "<40hex>",
  "policy_sha256": "<64hex>",
  "interruption_class": "QUOTA_EXHAUSTED_CONFIRMED",
  "interruption_evidence_redacted": "...",
  "requested_executor": {"product": "CODEX", "model": "...", "thinking": "..."},
  "resolved_executor": {"product": "...", "model": "...", "thinking": "..."},
  "observed_executor": {"product": "...", "model": "...", "thinking": "..."},
  "writer_quiesced": true,
  "allowed_path_set_hash": "<hash>",
  "changed_paths": [{"path": "relative/path", "sha256": "<64hex>", "status": "MODIFIED"}],
  "tests": [{"id": "...", "observed_status": "NOT_RUN|PASS|FAIL", "evidence_path": "..."}],
  "completed_verified": [],
  "incomplete_or_unsafe": [],
  "remaining_scope": [],
  "checkpoint_state": "LOCAL_DURABLE|PUSH_PENDING|CHECKPOINT_PUSHED_PARTIAL",
  "remote_branch": null,
  "remote_commit_sha": null,
  "successor_dispatch_id": null
}
```

Manifest fields MUST derive from Bridge observation or verified immutable refs; no fabricated model/quota/test results. Separate raw quarantined WIP from exportable sanitized checkpoint. Credentials and raw private feeds never included.

## 6. Controlled successor selection and handoff

CHAT performs POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK; evaluates whether original task is complete, actual successor CLI installation/access/quota/model, current source/Policy binding, worktree writer and grants. Comparison includes COPILOT, CODEX, CHAT and WORK as appropriate. A successor cannot inherit the predecessor's dispatch/grant or claim already accepted work again. New execution requires Owner-selected path/config/transport when C5B applies, signed authenticated decision provenance, single-use dispatch, allowlist and explicit STOP.

Successor inputs: frozen task scope, released source, remote verified checkpoint SHA (or independently vetted secure local copy if Git unavailable and explicitly permitted), completed/failed/unrun acceptance matrix, diff summary, missing steps, prior executor reason and guardrails. If prior checkpoint contains unauthorized code changes, predecessor work stays quarantined, not imported by default.

## 7. Acceptance matrix — add-on IDs (not silently added to released baseline)

BRG-QF-01: quota before first write — clean resumability, no invented diff.
BRG-QF-02: quota mid-file — do not treat partial file as valid.
BRG-QF-03: quota after tests before report — preserve observed logs, report generated by Bridge clearly identified.
BRG-QF-04: quota after full report before push — Bridge independent Git delivery (with scoped grant) and remote full SHA readback.
BRG-QF-05: retryable 429 vs confirmed quota — no false handoff.
BRG-QF-06: auth/network/crash vs quota — faithful distinct statuses.
BRG-QF-07: Agent quota exhausted while Git independent credentials valid — checkpoint remote readback succeeds.
BRG-QF-08: Git denied/expired credentials — local durable, remote not claimed, retry policy bounded.
BRG-QF-09: duplicate crash/restart/replay — exactly one remote checkpoint receipt per idempotency key.
BRG-QF-10: secret in untracked/ignored file — export blocked/redacted, no leak.
BRG-QF-11: actor still alive and writing — quarantine, no second writer.
BRG-QF-12: stale source or changed allowed path set — block reuse and repin.
BRG-QF-13: successor Agent quota unavailable — stop, no substitution.
BRG-QF-14: successor dispatch authorized — new worktree, new configuration/decision, no implicit privilege escalation.
BRG-QF-15: no Git permission for code diff — prohibit checkpoint code push even if report-only push is allowed.
BRG-QF-16: ambiguous provider quota signal — UNKNOWN, no silent switch.
BRG-QF-17: main/merge/PR commands denied under checkpoint grant.
BRG-QF-18: remote SHA/ancestry mismatch — delivery BLOCKED.
BRG-QF-19: incomplete tests/semantics — checkpoint partial never ACCEPTED.
BRG-QF-20: crash after push before event — durable reconciliation detects remote checkpoint without duplicate review.

Tests should run offline first with synthetic fixtures, then an explicitly authorized local-host E2E pilot. Never burn production Agent quota deliberately just to simulate exhaustion.

## 8. Implementation integration and gate mapping

- BRG-001: independently verify Windows host, CODEX/COPILOT observed CLI quota indicators, Bridge Git credential and Git scoped permissions; recorded evidence required, status UNKNOWN until observed.
- BRG-050..080: introduce interruption classifier, AgentProcessSupervisor quiescence, ownership lock, sanitized inventory and recovery ledger (only after Gate A + task-specific DEV).
- BRG-090..091: independent scoped Git checkpoint publisher with remote full SHA, ancestry/readback and pending retry (only after explicit checkpoint Git grant).
- BRG-092..099: optional durable recovery notification and CHAT review queue; no auto-rework or auto successor.
- BRG-100..102: independent negative test evidence including all BRG-QF cases.

## 9. Routing and permission snapshot at candidate authoring

R0: Existing Bridge v0.3 RELEASED; P0 Issue #10 open; no verified runtime. Avoid duplicate implementation.
R1: DESIGN_DELTA / PRE-DEV.
R2: Policy V1.8.2/source verified; AUTOMATED_GATE_A=BLOCKED_CAPABILITY_UNAVAILABLE, CODE_ALLOWED=NO, checkpoint code-diff push grant=UNKNOWN.
R3: CODEX/COPILOT host-installed/CLI-specific quota observability=UNKNOWN; account-specific remaining quota=UNKNOWN.
R4: CHAT authorized to document/design and track; COPILOT viable precheck candidate but access unknown; CODEX viable code candidate but no grant; WORK independent review candidate after material delta; no default Agent choice.
R5: actual Windows worktree, WIP and single-writer status=UNKNOWN.
R6: candidate may be documented on Git only as scoped governance/planning artifact; no source/implementation release claim.
R7: STOP before any runtime code edit or Agent execution; proceed with host precheck and independent design review, then separate scoped authorization.

This candidate is a proposal for integrating a technical-only delta into the released Bridge v0.3 successor; it is NOT self-effective and cannot substitute for Owner/CHAT release control.
