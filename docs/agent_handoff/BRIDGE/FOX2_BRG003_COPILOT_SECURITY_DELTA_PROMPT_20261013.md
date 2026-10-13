# FOX2 — BRG-003 Delta Safety Clearance — COPILOT READ-ONLY (2026-10-13)

**Task:** BRG-003-SECURITY-DELTA-01 / report-only follow-up; not a DEV, Git import or branch/push grant.
**Stage:** BRG-003 PRECOMMIT, bounded final security attestation.
**Applicable authority:** FOX2 Policy V1.8.2 RELEASED_EFFECTIVE; Agent Prompt Routing Index V1.2.2 EFFECTIVE_DERIVATIVE; Bridge Technical Spec v0.4 RELEASED_EFFECTIVE. Prior BRG-003 REV3 remains historical parent prompt. At handoff, apply current Library Source Freshness precheck / use CHAT-attested release status if Copilot has no Library; STOP on known newer effective release. 
**Source identity:** comparison manifest `8c217d122f171de5bfef9b2c7cca6c823cd32eaa:docs/agent_handoff/BRIDGE/FOX2_BRG003_20FILE_HASH_RECONCILIATION_20261013.json`, blob `3ef8852964214c99161ed9ff4e463cb677af51cd`.
**CHAT finding:** original Copilot BRG-002 full SHA-256 table from Owner-pasted `Pasted text(20261013-042845).txt` independently compared to Copilot BRG-003 report `Pasted text(20261013-062752).txt`: all **20/20 names / sizes / full hashes match**. Original baseline is now preserved in Git manifest; **DO NOT REPEAT** whole-tree inventory or full 20-file baseline comparison. This is cross-report evidence, not direct disk attestation.
**Role/Engine/Thinking:** COPILOT / actual observed model and Optimize setting or UNKNOWN; cheapest eligible READ-ONLY session, do not trigger paid CLI/quota probes. CHAT owns routing and verdict.
**Allowed action:** Read only specific source text and metadata on Windows, report sanitized findings in Copilot Chat. No file write, git fetch, branch/worktree creation, git commit/push, staging, pytest, SQLite open, deletion or process termination.

## Tasks — only remaining deltas

1. Independently open the manifest at the exact Git commit+path and report its blob SHA and 20/20 count. On the local host, take **one fresh full SHA-256 of each of the 20 allowed source paths only if needed to detect change since the BRG-003 report**; otherwise use file metadata delta first. If any file changed, record the changed path/new digest (no content), STOP; do not quietly accept a new snapshot. No full-tree reread.
2. **Synthetic credential fixture review:** Inspect literal definitions and usage without executing tests for `tests/test_dispatch_poller.py` lines ~353, ~434; `tests/test_lock_logging_health.py` lines ~97/~109, and any dependencies needed to understand them. Determine whether the token-shaped `ghp_` string and URL-with-userinfo are demonstrably synthetic examples (constructed hardcoded fixtures with no credential lookup/reference) or `UNKNOWN/POSSIBLE_SECRET`. Return file:line, classification, proof by description (NOT token value, email address or URL). If genuine/uncertain, STOP import.
3. **Personal paths:** Inspect `src/fox2_agent_bridge/config.py` lines ~27/30/33 and `tests/test_config_paths.py` line ~23. Report paths masked as `<USER>`; classify runtime impact if replaced by environment-based dynamic home/tool discovery. Propose *exact changed path list and acceptance test* for a later authorized sanitization commit (no code changes now).
4. **REVIEW_REQUIRED decision:** For first source baseline, **DEFER all three** `config/bridge.example.toml`, `reports/BRG-010.md`, `reports/BRG-020.md` from initial Git import; keep all three originals unchanged at Windows source path. Later task may add sanitized config and reports after distinct content review. Do not stage them. Confirm this decision in report.
5. **Writer/permissions:** Observe Git branch `work/FOX2-BRG-003-SOURCE-BASELINE-copilot` availability, intended isolated `C:\Projects\FOX2-worktrees\FOX2-BRG-003` and current Codex process state read-only. A clean repo or empty worktree is not exclusive writer proof. Do NOT kill any process or inspect private memory; return `WRITER_UNKNOWN` unless an explicit applicable one-writer lane can be proven. Do not run `gh auth status` or create credentials unless scoped separately.
6. **Import risk contract proposal** (NOT executed): target only `agent_bridge/**`, source original frozen locally; initial Git snapshot must contain **sanitized copies** of the 20 INCLUDE files (after separate whole-WP DEV grant to alter only copies) plus `agent_bridge/.gitignore` denylist. No raw paths, suspected token strings or private runtime/config/report content in **any** commit history. Maintain private raw pre-edit source evidence locally without Git promotion; after sanitization recompute Git source hashes and relate them to original 20 SHA manifest. All first-import operations require a later explicit one-time scoped WP authorization and verified writer/Git permission. Subsequent commits inside the same grant scope do NOT require per-commit Owner approval.

## Report required

`FOX2 BRG-003 SECURITY DELTA VERDICT`:
- task/version pins and freshness basis (independent vs CHAT-attested);
- exact 20/20 historical hash comparison **REUSED** from CHAT, observed delta changes if any;
- token fixture status: SYNTHETIC_CONFIRMED | UNCERTAIN_POSSIBLE_SECRET, evidence by code context without literal secrets;
- path impact and safe parameterization strategy, no personal path disclosure;
- 3 REVIEW_REQUIRED excluded from first import; runtime DB/sidecars preserved/excluded;
- actual worktree/writer and Git capability, UNKNOWN where not verified;
- proposed **one-time whole BRG-003 sanitized-source import** grant with exact allowed paths, chosen branch/base SHA and STOP criteria (proposal only);
- verdict `READY_FOR_SCOPED_SANITIZED_IMPORT_GRANT` or `BLOCKED_SECURITY / BLOCKED_WRITER / INCOMPLETE_EVIDENCE`.

STOP if source version changed, content SHA mismatches, any actual/unknown secret, uncontrolled writer, or any write/import/branch/worktree operation. No CODE_ALLOWED/GIT_CODE_PUSH/merge/LIVE granted.
