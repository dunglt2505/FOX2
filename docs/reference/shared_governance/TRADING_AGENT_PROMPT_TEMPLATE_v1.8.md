# TRADING — Complete Agent Prompt Template v1.8 — CHAT-FIRST Source Lock & Minimal Delegation

**Date:** 2026-10-13. **Status:** `OWNER_DIRECTED_EFFECTIVE_TEMPLATE` after actual Library upload, raw-byte readback and template release manifest; before then candidate/not active.
**Parent:** `TRADING_AGENT_PROMPT_TEMPLATE_v1.7.md` (retains the v1.6 mandatory identity, Git, safety and evidence ZIP clauses). **Operating source:** `TRADING_AGENT_EVIDENCE_HANDOFF_POLICY_v1.8.md` (plus retained v1.7 unchanged obligations).
**Projects:** FOX / FOX2 / Silkworm / Mantis / future Trading projects, **only when each project has authenticated its own active policy and applicability**. **Purpose:** prevent divergent Trading Library, Git and Agent document versions. Not a business BRD or trading authorization.

## Mandatory header for EVERY delegated task (do not omit)

```text
Project / Task ID / Checkpoint / Priority:
CHAT_CAPABILITY_CHECK: CHAT_DIRECTLY_COMPLETED | LOCAL_ONLY_DELEGATED | CODE_WORK_PACKAGE_DELEGATED | BLOCKED_CAPABILITY
CHAT_DIRECT_ACTIONS_DONE: <remote-Git/Library/Issue/manifest-evidence-or-NOT_APPLICABLE>
DELEGATION_REASON: <exact-host-or-coding-delta-that-CHAT-cannot-complete-or-NONE>
Role · Agent · Engine/Model (actual or Auto/UNKNOWN) · Thinking · Scope:
Owner / acceptance authority: CHAT / designated Owner
Source repository, worktree, branch, expected/current HEAD:
POLICY_RESOLVED_AT_UTC:
LATEST_EFFECTIVE_RESOLVED_AT_UTC:
POLICY_BASIS: <exact approved policy title/version/Library path/status>
PROMPT_TEMPLATE_BASIS: <exact approved template title/version/Library path/status>
PROJECT_GOVERNANCE_BASIS: <Owner approval and actual canonical baseline>
LIBRARY_INVENTORY_CURSOR_EXHAUSTED: TRUE/FALSE
DOCUMENT_SOURCE_OF_TRUTH: CHATGPT_LIBRARY_AUTHORING + APPROVED_GIT_EXECUTION_MIRROR
DOC_SYNC_STATUS: PUBLISHED_FOR_AGENT | DOC_SYNC_PENDING | DOC_SYNC_BLOCKED
DOC_SOURCE_LOCK: <manifest path, manifest hash, Git commit>
DOC_GIT_REPOSITORY / DOC_GIT_REF / DOC_GIT_COMMIT:
REQUIRED_DOCS: <table below>
UNPUBLISHED_DOC_DELTA: NONE | <named blockers>
AGENT_PREFLIGHT_COMMAND: <exact checked-out repo command>
DOC_SOURCE_ACCESS: VERIFIED | NOT_VERIFIED
CODE_ALLOWED: YES | NO
POLICIES_APPLIED_REQUIRED: YES
PROMPT_POLICY_CHECK: PASS | FAILED (only after literal check)
ZIP_REQUIRED: YES | OPTIONAL | NOT_APPLICABLE; REASON:
CENTRAL_EVIDENCE_ROOT: C:\Projects\TradingHandoffs when ZIP needed
```

| document_id | Library version/path/file_id | Status/effective precedence | Git path/immutable commit | SHA-256/Git blob | Readable by Agent? |
|---|---|---|---|---|---|
| Each applicable source | EXACT, not "latest" | Approved effective or separately-authorized Draft | Verified | Observed hash | YES / BLOCKED |

## CHAT-FIRST pre-routing allocation — mandatory Owner decision 2026-10-13

1. First perform `POLICY_CHECK → TASK_STATE_CHECK → R0–R7 → ASSIGNMENT_CHECK` using the latest **effective policy for that specific project**. This template does not automatically install FOX2 governance into FOX/Silkworm/Mantis and cannot supersede a higher-authority constraint.
2. Before spending any Copilot/Codex/WORK tokens for GitHub metadata, issue/PR, remote commit/blob/hash, Library source, manifest, release verification or policy-status lookup: **CHAT MUST use its available authenticated tools to do those tasks itself**, provided the action is permitted and tool output can be verified. The same work cannot be routinely delegated again. Record `CHAT_DIRECTLY_COMPLETED` with evidence.
3. Agent delegation MUST be the smallest genuinely **local-host or coding delta**: Windows/macOS workstation/IDE/worktree/process state, local-only credentials and tests, substantive implementation/refactor/bugfix, and necessary permitted own-code-branch local Git commit/push. Do not ask an Agent to enumerate Library versions, parse GitHub Issue comments or repeat a full remote manifest CHAT already knows. Receiver may perform a scoped independent *received-bytes* integrity check; this is not duplicate whole-source audit.
4. If CHAT cannot do a remote operation due to tool limitation, return `BLOCKED_CAPABILITY` or route narrowly to an otherwise eligible Agent only after the relevant Policy gates. **Never bypass a safety refusal by switching agents/tools**, never invent Git write rights or extrapolate a GitHub `push=true` bit into `CODE_ALLOWED`.
5. Reduce repeated Owner prompts: reuse existing exact bounded grants when still effective, but do not infer new DEV/merge/LIVE permissions from a template or routing directive. Reuse accepted task evidence; stop only on actual material invalidation or changed authority/source.
6. WORK is an independent specialist only when consequential, not a routine duplicate Git browser. Record why CHAT could not do delegated step and actual model/mode/quota where exposed; `UNKNOWN` or `NOT_EXPOSED` are not PASS.

**Reference:** `/Trading/00_Governance/TRADING_CHAT_FIRST_AGENT_ALLOCATION_OWNER_DIRECTIVE_20261013.md`. This template is not a new core Trading Policy, grants nothing and does not resume paused Trading-wide synchronization.

## Pre-send gate — CHAT MUST perform

1. Paginate the shared Trading Library governance and project source folders to exhaustion; resolve the latest **approved applicable** policies and BRD by Owner decision, not version number alone.
2. For every material required doc, match Library bytes/hash/status to the Git publication manifest **and the target accepted commit**; unreleased branch candidates are not accepted DEV baselines. Identify current unmerged/unpublished changes and whether they affect this task.
3. Confirm Agent can read source file/commit in its actual repository/worktree; if not, transfer exact authorized specs or STOP. No implicit ChatGPT Library access.
4. Verify current branch and worktree ownership, safety and applicable evidence root; no reset/rebase/merge/push by default.
5. `CODE_ALLOWED=YES` only if `DOC_SYNC_STATUS=PUBLISHED_FOR_AGENT`, every required source is accessible & hash-confirmed, no required doc has a later approved unpublished revision, and all ordinary safety/scope gates pass. Otherwise STOP `DOC_SYNC_BLOCKED`.
6. Include task-relevant policy clauses inside the prompt; list `POLICIES_APPLIED` and require the Agent to report actual git/lock results and `POLICY_VERSION_DRIFT`.

## Agent at start of task

- Confirm its actual branch/HEAD/worktree, expected commit and local source lock. Run the pinned checker; report `DOC_PREFLIGHT_PASS|FAIL`, actual verified file count, source-lock SHA and unresolved deltas.
- On FAIL/UNKNOWN, do **not** work around by reading old `reports/recovered` or silent cherry-pick, do not start modifying code. Return to CHAT for publication/authority decision.
- Preserve current task's pinned snapshot; material Library revision during work requires CHAT-issued amended handoff (never autonomous hot-swap).
- Only after source gate, proceed in allowed scope, retain original v1.6 test, safety, evidence and final `EVIDENCE_ZIP:` footer clauses. Do not mistake source-integrity PASS for Algorithm/Risk/Release acceptance.

## Compact task-specific report

```text
Task status: NOT_STARTED | BLOCKED | CODE_DONE | ACCEPTANCE_PENDING
ACTUAL_GIT_HEAD / WORKTREE:
SOURCE_LOCK / DOC_PREFLIGHT_RESULT:
DOC_SYNC_STATUS / CODE_ALLOWED:
CHAT_CAPABILITY_CHECK / CHAT_DIRECT_ACTIONS_DONE / DELEGATION_REASON:
POLICIES_APPLIED:
REQUIRED_DOC_HASHES_VERIFIED:
UNPUBLISHED_DOC_DELTA / OPEN_GATES:
TESTS_RUN / EVIDENCE / ZIP_REQUIRED:
LIVE/MARGIN/BROKER_WRITES: false/false/false (FOX default)
EVIDENCE_ZIP: NOT_REQUIRED — <reason>   # mandatory last line when no ZIP
```

## Publication handoff reference

Whenever CHAT saves/updates a Library document, invoke `TRADING_AGENT_EVIDENCE_HANDOFF_POLICY_v1.8.md` P0–P7 publication workflow: prepare versioned Library source → separate Git candidate + hash lock → PR/CI → Owner-approved integration → Agent fetch/preflight. Never claim this flow runs as an unattended background automation. Keep the original v1.6 requirements binding for ZIP/evidence, authority, safety and no destructive Git commands.

## V1.8 publication and compatibility

- Historical v1.7 remains retained; this v1.8 requires its **own** Library publication/readback and manifest before `EFFECTIVE_TEMPLATE` status. No automatic replacement of already pinned accepted prompts.
- For FOX2, current application must bind newest released FOX2 Policy (V1.8.3 after publication) and Agent Routing Index (V1.2.3 after publication); project-specific source lock must never be guessed from this shared template's static text.
- For FOX/Silkworm/Mantis, CHAT-first is an attributable Owner routing directive, but no implementation work, migration, git source publication, code, merge or LIVE is authorized by this template alone.
