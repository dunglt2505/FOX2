# FOX2 — COPILOT PROMPT — BRG-001 Windows Host + Quota/Git Recovery Readiness (READ_ONLY)

Prompt ID: FOX2-BRG-001-READONLY-COPILOT-20261013-001
Task: BRG-001; priority P0; stage PRE-DEV / HOST_PREFLIGHT.
Operating role: COPILOT = observatory host inspector only; CHAT = owner of routing/review.
Mode: READ_ONLY / NO DEV / NO AGENT EXECUTION / NO GIT WRITE.
Engine/Model/Thinking: record ACTUALLY OBSERVED Copilot product, exact model/mode and remaining quota if exposed; otherwise UNKNOWN. Never assume or change paid model. Optimize for minimum cost consistent with factual verification.
Dispatch status: MANUAL PROMPT FOR OWNER TO START IN VS CODE ONLY; not an authenticated automatic Bridge dispatch.
Policy: FOX2 Policy V1.8.2 RELEASED_EFFECTIVE; raw SHA256 552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc.
Released baseline commit: c9dc41b97ca8bc58f06cc2f3701832ba083422e3.
Technical current release: docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.3.md.
Candidate delta: docs/agent_handoff/BRIDGE/BRIDGE_QUOTA_RECOVERY_DELTA_v0.1_CANDIDATE.md at exact commit 25179960861e142bb973aa7a5538b067a17112cf (NOT RELEASED; design inspection only).
P0 tracking: https://github.com/dunglt2505/FOX2/issues/10.
Known old P2-01 host preflight Issue #9 is stale Policy V1.8; DO NOT copy its source binding or rerun P1.

## Critical boundaries
Do NOT edit, create, delete or save any project file, including tests, metadata, branches, Git config or .gitignore. Do NOT install/update/uninstall packages, extensions, CLI or drivers. Do NOT run a live agent task, spend extra agent requests just to probe quota, access auth tokens, print credentials, write remote report, commit/push, checkout, reset, clean, stash, rebase, cherry-pick, create worktree, create PR or merge. Do NOT change main, global git settings or owner WIP. Do NOT touch DNSE Production, broker, account, private market feed or secrets. Do NOT run destructive commands. If the available Copilot/terminal cannot execute an observation safely, report UNKNOWN/BLOCKED with reason and provide suggested future test, without improvising permissions.

## Execute in order

R0. Observe repository state and existing evidence with non-mutating commands only. Do not redo P1 (accepted), prior BRG docs or P2-01 contract lock.
R1. Confirm BRG-001 is PRE-DEV host capability assessment, not implementation.
R2. Read exact policy/spec/delta from verified Git or already available local exact-source mirror; report URL/hash and inability to match source as BLOCKED_SOURCE if mismatched.
R3. Inventory actual Windows host and available tools WITHOUT invoking interactive Agent workloads:
- OS, current user environment (do NOT include private identifying information in report), working folder, available Python/pip/git/node (versions only if safely obtainable).
- `where.exe git`, `git --version`, `git remote -v` (redact credential-bearing remotes), `git status --porcelain=v1 --untracked-files=all`, `git status --ignored --short` (redact sensitive filenames if needed), `git branch --show-current`, `git rev-parse HEAD`, `git worktree list --porcelain`, `git diff --name-only`, `git ls-files -m -o --exclude-standard`, `git rev-parse --show-toplevel` if inside repository, each only when safe; READ ONLY, no mutation.
- Detect in-progress merge/rebase/cherry-pick and existing writer locks/processes using OS non-mutating inspection where possible.
- `where.exe codex`, `where.exe copilot` and safe `--version`/`--help` only when verified non-mutating. Do not run CLI login/status endpoints that trigger interactive auth or consume quota unless obviously safe; if unclear UNKNOWN.
- Capture observable quota indicators from already visible product UI/help/status only, with timestamp and vendor semantics; differentiate remaining requests vs subscriptions vs model quota; if not exposed UNKNOWN. Do not print token or credential data.
- Check whether Bridge can potentially have independent Git credential context without reading raw secrets. Git credential presence not equal scoped permission. Never perform a write/push test in READ_ONLY.
- Identify existing Bridge runtime installation/service/configuration if visible; do not assume it exists merely because documents exist.
R4. Compare eligible agents (COPILOT/CODEX/CHAT/WORK) by actual installed access, task suitability, exposure, quota observability and cost; do not choose a DEV agent.
R5. Determine whether BRG source/worktree can be isolated from owner FOX2 worktree and whether one-writer/exclusive ownership is actually observable; provide proposal only, no creation.
R6. Assess recoverability after quota exhaustion with **non-operational** scenarios: (a) quota before write, (b) mid-file, (c) tests complete/no push, (d) Git credentials independent, (e) remote inaccessible, (f) successor candidate quota absent. Clearly state which behaviors are purely designed and require an authorized pilot.
R7. STOP; return findings and no action changing files.

## Required report in final Copilot chat response (do not write it to disk without separate permission)

# FOX2-BRG-001 HOST READINESS REPORT
- Task / observation time / Windows host fingerprint sanitized:
- Policy V1.8.2 SOURCE_VERIFIED: YES/NO/UNKNOWN + exact anchor:
- Bridge spec v0.3 SOURCE_VERIFIED: YES/NO/UNKNOWN:
- Quota delta candidate SOURCE_VERIFIED: YES/NO/UNKNOWN:
- Repository origin (sanitized) / branch / HEAD / WIP tracked-untracked-ignored / worktrees / active writer:
- Python, Git, Node, Codex CLI, Copilot CLI: INSTALLED/ABSENT/UNKNOWN + verified version:
- Copilot observed config/model/mode/quota and Codex observed config/quota: evidence or UNKNOWN:
- Agent CLI quota errors distinguishable in current installed version: VERIFIED/UNKNOWN (no simulated consumption):
- Safe Bridge Git independent push: DESIGN_POSSIBLE / BLOCKED / UNKNOWN; credentials scope and GitHub write permissions UNKNOWN until safely confirmed:
- Current Bridge Gate A trust enforcement: VERIFIED/BLOCKED/UNKNOWN; no assumptions from unprotected branches:
- Proposed isolated worktree and checkpoint report paths: NON-AUTHORIZED PROPOSAL:
- Recovery risks and unknowns:
- BRG-QF-01..20 feasibility: OFFLINE_TESTABLE / HOST_PILOT_NEEDED / UNKNOWN, do not mark tests PASS:
- Recommended next exact bounded step:
- Gate table: BRG001_PREFLIGHT, GIT_REPORT_WRITE, GIT_CODE_CHECKPOINT_WRITE, AUTOMATED_GATE_A, CODE_ALLOWED, PR, MERGE, LIVE:
- Final verdict: READY_FOR_REVIEW / BLOCKED / INCOMPLETE_EVIDENCE:
- Evidence digest: commands and sanitized findings; explicitly label commands NOT_RUN.

If a command is unsupported, do not invent output. Return the report directly to the user for CHAT readback. Since this is a manual READ_ONLY prompt, no Git result delivery or autonomous follow-up is authorized.

STOP CONDITIONS: Policy/source mismatch, unsafe workspace, active writer collision, CLI trying to trigger paid Agent requests, credential exposure, any mutating command, absent authority, unclear quota semantics, or unexpected request for Git push.
