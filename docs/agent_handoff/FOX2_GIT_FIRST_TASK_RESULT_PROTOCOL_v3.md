# FOX2 — Git-first Task/Result Protocol v3 — Result Contract v2

**Controlling authority:** Released `FOX2_POLICY_V1.4.md`, sections C1A/C1B/C4A/C5A/C6A–C6E. This operational guide is not a separate policy or Git permission. **Supersedes protocol v2 for newly dispatched/re-scoped WPs**, without rewriting legacy submissions.

## Task source: publisher-managed

- `docs/agent_handoff/<WP_ID>/task.md`
- `docs/agent_handoff/<WP_ID>/source_manifest.json`
- `docs/governance/FOX2_POLICY_V1.4.md` and its release manifest (exact Library bytes and verified SHA-256)
- `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`
- `docs/agent_handoff/FOX2_AGENT_RESULT_TEMPLATE_v3.md`
- `docs/agent_handoff/FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v3.md`

Source access: CHAT validates official Library bytes; COPILOT/CODEX validate Git/local snapshot bytes; WORK retains its full available CHAT/Library/Git access. No actor may substitute an unverified source excerpt for immutable readback.

## Source-ready checkpoint before implementation

Use Policy C1B.1: `GIT_SOURCE_READY=YES` only after every required released source is at a pinned remote commit and raw-byte readback matches its release receipt. Otherwise task stays `SOURCE_PENDING`; no implementation handoff even if prompt is correct. Record the missing file/failed operation/error/next Publisher action in existing source index/receipt. A scoped source-publisher/recovery task may continue from verified Library input; no DEV permission follows.

## Agent delivery: one WP branch, two mandatory files

- `reports/<WP_ID>/report.md` — R01–R12 human result; every requested item is classified DONE/PARTIAL/NOT_DONE and each acceptance/test has evidence/status.
- `reports/<WP_ID>/evidence_manifest.json` — valid Contract v2 JSON, including source/Policy SHA, actual Agent, grants, changed paths, executed tests, acceptance mapping, evidence hashes, blockers, security and next actor/gate.
- `reports/<WP_ID>/evidence/**` — sanitized minimal attachments, hash-pinned and cross-referenced, when needed.

Git report push is separate from code editing and merge. The Agent may commit/push **only** on its assigned non-main branch with observed writer lease, host permissions and `GIT_REPORT_WRITE=YES`, `GIT_REPORT_PUSH=YES`; otherwise report `PUSH_BLOCKED/LOCAL_ONLY` without claiming delivery. Verify no secret, raw licensed feed or private account data.

After push, the Agent sends only `repo | WP | branch | full remote commit SHA | PR URL or NONE | PUSHED_UNREVIEWED`; its in-commit manifest does not self-reference its own commit SHA.

## CHAT independent intake

At that immutable SHA: read both mandatory files; validate schema; compare task/base, scope, actual Git diff, source hashes and grant allowlist; validate claimed evidence and tests against real bytes; check blockers/security and decide `ACCEPTED`, `ACCEPTED_PARTIAL`, `REWORK` or `BLOCKED` in a **separate CHAT-owned review receipt**. Agent-submitted results are `PUSHED_UNREVIEWED` until that review. No self-acceptance, direct main push, merge, DEV, DNSE Production or LIVE by implication.

## Failure handling and legacy compatibility

Missing implementation source → `SOURCE_PENDING / GIT_SOURCE_READY=NO`; missing/mismatched report or evidence → `SUBMISSION_INCOMPLETE/CONTRACT_INVALID`; absent remote SHA/readback → `GIT_DELIVERY_NOT_VERIFIED`; missing rights → `PUSH_BLOCKED`; diff outside authorized paths or secrets → `BLOCKED`. Reuse v1 reports solely as legacy evidence, never silently convert to v2 or fabricate tests. The sync to Git is PENDING until publisher pushes and CHAT independently verifies exact bytes at a full commit.
