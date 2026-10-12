# FOX2 — Git-first Task/Result Protocol v8 — Result Contract v2

**Controlling authority:** Released `FOX2_POLICY_V1.8.md`, sections C1A/C1B/C4A/C5A/C6A–C6F. This operational guide is not a separate policy or Git permission. **Supersedes protocol v7 for newly dispatched/re-scoped WPs**, without rewriting legacy submissions.

## Task source: publisher-managed

- `docs/agent_handoff/<WP_ID>/task.md`
- `docs/agent_handoff/<WP_ID>/source_manifest.json`
- `docs/governance/FOX2_POLICY_V1.8.md` and its release manifest (exact Library bytes and verified SHA-256)
- `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`
- `docs/agent_handoff/FOX2_AGENT_RESULT_TEMPLATE_v4.md`
- `docs/agent_handoff/FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v7.md`

Source access: CHAT validates official Library bytes; COPILOT/CODEX validate Git/local snapshot bytes; WORK retains its full available CHAT/Library/Git access. No actor may substitute an unverified source excerpt for immutable readback.

## Source-ready checkpoint before implementation

Use Policy C1B.1: `GIT_SOURCE_READY=YES` only after every required released source is at a pinned remote commit and raw-byte readback matches its release receipt. Otherwise task stays `SOURCE_PENDING`; no implementation handoff even if prompt is correct. Record the missing file/failed operation/error/next CHAT recovery action in existing source index/receipt. A scoped source-publisher/recovery task may continue from verified Library input; no DEV permission follows.


## Local Agent dispatch — single-check transport

For an implementation WP, CHAT completes Policy V1.8 C1/C5 decision checks **once** and records `PROMPT_READY_TO_DISPATCH`. CHAT then exposes Owner actions `EXECUTE_LOCAL_AGENT` / `SAVE_PROMPT_ONLY`. On `EXECUTE_LOCAL_AGENT`, CHAT publishes one append-only `docs/agent_handoff/<WP_ID>/dispatch/<DISPATCH_ID>.json` conforming to `FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v1.json`, bound to exact task/source/policy/prompt hashes and `max_runs=1`.

The Local Bridge does **not** re-run `POLICY_CHECK`, `TASK_STATE_CHECK`, `ROUTING_R0_R7` or `ASSIGNMENT_CHECK`. It validates the immutable decision receipt and performs only `LOCAL_RUNTIME_ATTESTATION`: repo/workspace mapping, current CLI/Git identity, dispatch/task/policy/prompt hash, expected branch/base/head, writer/WIP collision and runtime operation permission. Runtime failure returns `LOCAL_RUNTIME_BLOCKED`; duplicate dispatch returns `DISPATCH_DUPLICATE_IGNORED`. The Bridge never reroutes, modifies Policy/BRD, escalates rights, merges or deploys.

Successful launch enters the existing Result Contract v2 flow; the dispatch artifact is not result evidence or acceptance.

## Agent delivery: one WP branch, two mandatory files

- `reports/<WP_ID>/report.md` — R01–R12 human result; every requested item is classified DONE/PARTIAL/NOT_DONE and each acceptance/test has evidence/status.
- `reports/<WP_ID>/evidence_manifest.json` — valid Contract v2 JSON, including source/Policy SHA, actual Agent, grants, changed paths, executed tests, acceptance mapping, evidence hashes, blockers, security and next actor/gate.
- `reports/<WP_ID>/evidence/**` — sanitized minimal attachments, hash-pinned and cross-referenced, when needed.

Git report push is separate from code editing and merge. The Agent may commit/push **only** on its assigned non-main branch with observed writer lease, host permissions and `GIT_REPORT_WRITE=YES`, `GIT_REPORT_PUSH=YES`; otherwise report `PUSH_BLOCKED/LOCAL_ONLY` without claiming delivery. Verify no secret, raw licensed feed or private account data.

After push, the Agent sends only `repo | WP | branch | full remote commit SHA | PR URL or NONE | PUSHED_UNREVIEWED`; its in-commit manifest does not self-reference its own commit SHA.

## CHAT independent intake

At that immutable SHA: read both mandatory files; validate schema; compare task/base, scope, actual Git diff, source hashes and grant allowlist; validate claimed evidence and tests against real bytes; check blockers/security and decide `ACCEPTED`, `ACCEPTED_PARTIAL`, `REWORK` or `BLOCKED` in a **separate CHAT-owned review receipt**. Agent-submitted results are `PUSHED_UNREVIEWED` until that review. No self-acceptance, direct main push, merge, DEV, DNSE Production or LIVE by implication.

## Failure handling and legacy compatibility

Missing implementation source → `SOURCE_PENDING / GIT_SOURCE_READY=NO`; missing/mismatched report or evidence → `SUBMISSION_INCOMPLETE/CONTRACT_INVALID`; absent remote SHA/readback → `GIT_DELIVERY_NOT_VERIFIED`; missing rights → `PUSH_BLOCKED`; diff outside authorized paths or secrets → `BLOCKED`. Reuse v1 reports solely as legacy evidence, never silently convert to v2 or fabricate tests. The sync to Git is PENDING until CHAT completes upload and verifies exact bytes at a full commit.

## Mandatory CHAT pre-dispatch responsibility (Policy C1B.1)

CHAT owns upload and recovery. Complete and verify every required released source at a full remote commit BEFORE assigning/issuing an implementation task or prompt. If GIT_SOURCE_READY=NO, keep the implementation task internally SOURCE_PENDING; do not hand it to an Agent to discover or repair missing documents. CHAT records the blocker and precise recovery action, repairs permitted deltas and rechecks remote raw bytes/version/hash. Agent source checking is supplementary; WORK audit is only when assigned. Safety refusal means STOP, no bypass. YES grants source readiness only, never DEV/merge/Production. Result Contract/schema v2 remain unchanged.

## Policy Binding and delivery assurance — mandatory new/re-scoped WP

CHAT publishes and pins in task + source manifest: Policy ID/version/raw SHA-256/release manifest/Git path/full commit, source binding, Result Contract v2, **one predetermined** repo/branch/report/manifest/evidence destination, Issue locator, separate report-write/report-push grants and STOP conditions. Agent checks exact Policy bytes before work; mismatch -> BLOCKED_POLICY_MISMATCH. CHAT verifies `REPORT_DELIVERY_PATH_READY=YES` before executable Git-deliverable handoff; if NO, repair intake rights before dispatch. Existing V1.2 task is historical only, never silently reused.

End-of-task Agent emits `FOX2_AGENT_DELIVERY_RECEIPT` with actual execution status, actual delivery status, Git remote commit (or NONE), branch/PR, report/manifest/evidence, actual permission/blockers and next action. `PUSHED_UNREVIEWED` is valid only after true remote push; if no grant use `PUSH_BLOCKED` or `LOCAL_ONLY` and do not claim completion delivered. CHAT separately reads result at that SHA, issues `RESULT_DELIVERY_VERIFIED=YES|NO`, then independently decides acceptance. Neither a local commit, GitHub Issue, PR nor chat message substitutes. Schema v2 is unchanged. No runtime/main/merge/Production/LIVE grant.

## Reusable report-only authorization — C6F.2A (carried forward in V1.8)

FOX2 Owner now grants GitHub Copilot Pro reporter role **standing internal authority** to write/push **only** `reports/<WP_ID>/**` on its CHAT-designated `work/<WP_ID>-copilot` non-main branch after checking the actual host/git identity, WIP/writer lease, and allowed-path staged diff. **No new per-WP Owner grant** is required for qualifying Copilot report publications. The task still defines exact Policy binding, report paths, issue, branch and source commit. Valid source identity and host/branch/writer checks cannot be skipped. If host Git access is absent or write would touch another file/branch, STOP `PUSH_BLOCKED`, preserve local results and inform CHAT. `PR_CREATE`, DEV, merge, provider and LIVE are not implied.

The standing policy allowlist is **not an enforced GitHub directory ACL**. Copilot must push a result commit and provide its full remote SHA. CHAT independently validates report, schema v2 and evidence before `RESULT_DELIVERY_VERIFIED`, and separately decides acceptance. v2 schema remains unchanged.