# FOX2 — BRG-001 COPILOT MANUAL READ-ONLY HOST PREFLIGHT — REV2 (Candidate)

Prompt ID: FOX2-BRG-001-READONLY-COPILOT-20261013-REV2
Supersedes for manual use: FOX2_BRG001_COPILOT_READONLY_PROMPT_20261013.md (retain as historical prompt).
Status: MANUAL_EXECUTION_PROMPT_READY / NOT_AUTOMATED_DISPATCH / READ_ONLY / NO_DEV.
Tracker: https://github.com/dunglt2505/FOX2/issues/10
Task ID: FOX2-BRG-001; WP ID: BRG-001; Change ID: FOX2-BRG-QUOTA-RECOVERY-20261013.
Role: COPILOT, GitHub Copilot Pro on intended authorized Windows host ONLY if actually observed; otherwise BLOCKED_HOST or UNKNOWN.
Engine/model/thinking: ACTUAL_OBSERVED_OR_UNKNOWN. Do not assert a model or select a costly alternative. CHAT controls later routing and approvals.
Resource cost: read-only native host inspection, no deliberate paid request for quota probing; unknown quota recorded UNKNOWN, never guessed.
Stage: HOST_PREFLIGHT, no application/Bridge code.
Current CHAT scope decision: manual VS Code presentation to Owner, not Bridge transport approval or unattended Agent execution.

## Immutable source and authority table

1. Active FOX2 Policy V1.8.2 (RELEASED_EFFECTIVE), SHA-256 of released Library bytes `552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc`; Git blob `0783c024d19f96a0b87ab770dad80bab449fa21f` in released source-set `c9dc41b97ca8bc58f06cc2f3701832ba083422e3`.
2. Released FOX2 Bridge Technical Spec v0.3, Git path `docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.3.md` at source-set commit `c9dc41b97ca8bc58f06cc2f3701832ba083422e3`. Released design; Gate A still BLOCKED_CAPABILITY_UNAVAILABLE.
3. Technical-only quota recovery candidate `docs/agent_handoff/BRIDGE/BRIDGE_QUOTA_RECOVERY_DELTA_v0.1_CANDIDATE.md` at exact Git commit `25179960861e142bb973aa7a5538b067a17112cf`, blob `3cdf355df385a67c63e492d2a84efd3e099663ca`. Candidate is NOT authoritative over Policy/released Spec.
4. This prompt must be pinned to its exact full Git commit SHA by CHAT/Owner, and independently read back before any local action. Do NOT infer that source-set `c9dc...` contains later quota candidate or prompt.
5. P1 accepted evidence already exists, Issue #5 closed. M1-P2-01 contract lock `a374142d191c84a6a9e0bd8e4c21593797d31794`; do not re-run P1/P2 work. Historical Issue #9 used outdated Policy V1.8, not active task authority.

Source resolution must use exact full Git commit:path, not GitHub's default branch. If inaccessible, mismatched, or unsupported: SOURCE_RESOLUTION_UNKNOWN/BLOCKED and STOP; do not substitute an old local document.

## CHAT authority/routing snapshot to be checked, NOT rewritten by Copilot

POLICY_CHECK: V1.8.2 confirmed released from Library/Git evidence; each source must still be resolved by executor.
TASK_STATE_CHECK: BRG-001 remains PRE-DEV, not implemented; Issue #10 P0 OPEN.
R0: Existing released Spec/plan and quota candidate recognized; avoid duplicate tasks.
R1: Scope READ_ONLY host inspection, not DEV/recovery implementation.
R2: Source authority and C5B/C6F boundaries pinned; automated Bridge Gate A blocked; CODE_ALLOWED=NO.
R3: Windows host, installed product/model/mode/quota and permissions UNKNOWN pending Copilot observation. If not GitHub Copilot Pro on eligible host, standing C6F.2A report push does NOT apply.
R4: CHAT drafts/reviews; COPILOT is conditional local host observer; CODEX is possible future implementation candidate (unapproved); WORK independent audit after design; no privileged executor selected.
R5: Actual active writer, HEAD, worktrees and dirty WIP UNKNOWN until inspected. Do not create worktrees or edit files.
R6: THIS task is manual text report only. Standing C6F.2A is acknowledged but intentionally NOT exercised in this bounded precheck; do not conflate it with arbitrary app/code checkpoint Git push. Git source-read is conditional on real access.
R7: Task configuration = COPILOT / actual observed model-or-UNKNOWN / READ_ONLY / observation only. STOP before any file modification, Git push or Agent execution; return sanitized findings to Owner/CHAT. No Owner Bridge transport confirmation, no automated dispatch.

## Task-scoped permission matrix

- GIT_SOURCE_READ: CONDITIONAL (read-only and actual access).
- LOCAL_READ_ONLY_COMMANDS: CONDITIONAL (only commands demonstrably non-mutating; file names, remotes and logs may contain sensitive content; redact).
- GIT_REPORT_WRITE / GIT_REPORT_PUSH: NOT EXERCISED BY THIS PROMPT. C6F.2A remains a conditional, narrower standing authorization for eligible Copilot Pro reporter workflows, not revoked and not evidence of host entitlement.
- CODE_ALLOWED / GIT_CODE_PUSH / GIT_CHECKPOINT_CODE_PUSH / BRIDGE_AGENT_LAUNCH / PR_CREATE / MERGE_ALLOWED / PROVIDER_PRODUCTION / BROKER_WRITE / LIVE: NO.
- No source, policy or user task text alone is grant evidence; no implicit permissions from installed credentials.

## Execute observations in order

0. If operating in VS Code, report detected host, Copilot product, real model/mode if visible and timestamp. If remote/cloud environment rather than authorized Windows host, STOP with BLOCKED_HOST. Do not query or expose tokens/auth.
1. Read and verify immutable Policy, released Bridge Spec and candidate delta by the exact refs above. Report independently observed commit/path/blob or UNKNOWN. Apply source precedence; candidate cannot override released documents.
2. Locate FOX2 checkout without modifying it. Report sanitized origin/branch/HEAD; WIP tracked/untracked/ignored; worktree owners; merge/rebase/cherry-pick states; possible concurrent git/agent writers, all via safe read-only inspection.
3. Use only non-mutating inspection commands as available: `git status --porcelain=v1 --untracked-files=all`, `git status --short --ignored`, `git rev-parse HEAD`, `git branch --show-current`, `git worktree list --porcelain`, `git remote -v` with redaction, `git diff --name-only`; `where.exe git`, `where.exe codex`, `where.exe copilot`; `--version` only when safely supported. If any command could trigger network/auth/Agent consumption or writing, skip and report NOT_RUN/UNKNOWN.
4. Inspect tool availability and versions: Windows, Python/pip/Git, Node only as context, Copilot CLI/extension, Codex CLI; distinguish VS Code Copilot extension from Copilot CLI, and account plan from actual model quota. No CLI login, auth refresh, prompt execution, write probe, or intentional quota depletion.
5. Record only quota already observable without extra paid request: per product/model reset/remaining/rate limit if explicitly shown; timestamp and provenance. UNKNOWN if not shown. Do not treat generic HTTP 429 as confirmed quota exhaustion.
6. Inspect whether an independent Bridge Git identity is theoretically feasible without showing secrets; actual credential presence, scope, remote push authority and protected/ref enforcement remain UNKNOWN unless safe verified external evidence already exists. No write/push test.
7. Identify safe future isolated Bridge worktree roots, writer ownership and local durable checkpoint location as NON-BINDING proposal. Do not create directories or touch WIP.
8. Perform conceptual recovery scenarios: quota before first file, mid-write, after test, before push, independently valid/invalid Git, process still running, source drift, successor quota missing; label all BRG-QF tests NOT_RUN with pilot/offline feasibility.
9. Compare next step options CHAT / COPILOT / CODEX / WORK by evidence and cost. Do NOT select a DEV agent or self-authorize a successor.
10. STOP and return the report in current Copilot Chat (text only) to Owner for independent CHAT readback. No automated task dispatch or further file operations.

## Report format (required; do not create a file)

# FOX2-BRG-001 HOST READINESS — REV2
- Task ID / WP ID / Change ID / Prompt revision / timestamp:
- Host and actual COPILOT product, engine/model/thinking, quota source/status (or UNKNOWN):
- Verified exact Policy Git commit:path, blob and released status:
- Verified exact Bridge Spec Git commit:path and blob:
- Candidate delta exact commit:path/blob, clearly NOT_RELEASED:
- OS/toolchain/CLI availability with safe evidence and NOT_RUN distinctions:
- Git branch/HEAD/origin sanitized, tracked/untracked/ignored WIP and worktree collision:
- Authentication/quota visibility: OBSERVED/UNKNOWN, NEVER_TOKEN_DUMPED:
- Independent Git checkpoint feasibility: DESIGN / PROVEN / UNKNOWN, with report-vs-code-grant distinction:
- Gate A trust enforcement: BLOCKED_CAPABILITY_UNAVAILABLE until new effective evidence:
- BRG-QF-01..20 test statuses: NOT_RUN; future pilot classification:
- Permission matrix, each PASS/BLOCKED/UNKNOWN/NOT_EXERCISED with evidence:
- R0–R7 observation deltas / any actual conflicting source:
- Risks, missing facts and STOP events:
- Outcome: READY_FOR_CHAT_REVIEW / BLOCKED_SOURCE / BLOCKED_HOST / INCOMPLETE_EVIDENCE:
- Exact safe next step; no DEV, push, PR, merge or LIVE claim.

Security: redact credentials, URLs containing tokens, env vars, raw account data, private feeds and sensitive filenames. Do not claim work complete from an issue comment or a local unpushed file. Distinguish Git-reported state from effective permissions.

STOP when source mismatch, unexpected credential exposure, missing authorized host, writer collision, unsafe command, untrusted control plane, quota prompt triggering execution, or attempted unauthorized modification. Report observed blocker; do not improvise.
