# FOX2 — CODEX HOST LEGACY LIFECYCLE INVENTORY (READ-ONLY)
## Candidate Agent prompt — source-bound, NOT ISSUED to execute

**Role:** CODEX — host-only read-only inventory collector; CHAT retains SDLC ownership and independent Result Review.
**Engine / Model:** OpenAI CODEX CLI / `gpt-6.1-sol` (PINNED).
**Thinking:** `medium` (pinned for this candidate; do not silently switch).
**Scope:** FOX2 Bridge RC1 only, existing Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`, existing WP `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`; **read-only Windows host observation, NOT a coding attempt**.
**Permissions:** READ_ONLY against FOXLE-PC system state, files and Git source. Local temporary private sanitized JSON/ZIP and exact two non-main Git report files only after privacy verification. No elevated prompt, no state changes.
**Execution:** single bounded host inspection session, no nested Agent, no Attempt01–03 replay; **this file is a CANDIDATE** until the separate CHAT final assignment/admission and route-specific host checks.
**Expected delivery:** `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`, `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json` under a dedicated Git result branch, plus actual observed remote result SHA in final Agent message **outside** committed files. Sensitive host inventory remains local/private and is NOT pushed to Git.

### 1. AUTHORITY + EXACT SOURCE BINDING

Read the entire immutable task first:
`docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/HOST_LEGACY_LIFECYCLE_READONLY_20261020/task.md` at commit `45a50c6cdca27faaf3e24f71abd7b032214178ec`, Git blob `b093b7b01c6e97cd221781fb5d4e91c61baac78f`, raw SHA-256 `8af4e53145b64765b1a1225ab7606b9785284f7ffafaec1b4e07850bc85283fd`.

Bound host-inventory candidate contract: `8f072f99c22a8201a3c6f04ba5dafa62ea55d2fc:docs/roadmap/FOX2_BRIDGE_LEGACY_HOST_LIFECYCLE_INVENTORY_CONTRACT_20261020.md`, blob `204da7e0b29acc44ff2d3e31baeb9daddcd4b5a0`. Results accepted only within those source-defined read-only requirements.

Source evidence and status: CODEX Attempt03 Git result `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581` is a truthful `BLOCKED` report-only result. CHAT review `c659100b785ee75fdbe12b851ee30ec1d3aaf352` accepted only that evidence, not BUILD. Feature Registry `4f14585f60a1044b2fc895331bfe4dd3077d6408:docs/roadmap/FOX2_FEATURE_STATUS.json` has `BUILD/BLOCKED`. Governance Registry `d34da1e3b4918a902646621b487ca8ad3e05b0e0`, Dictionary v1.3, Routing v1.4.0, Git-first Protocol v12 determine prospective human task routing; **they do not attest Windows installed enforcement**. Current/source Git bytes and policy authority must remain distinct.

**Before running, the host launcher MUST supply separate actual CHAT assignment/admission** binding this exact prompt's own immutable publication commit/blob/SHA-256, the immutable task, allowed result branch/paths and verified current host route. Published task/prompt alone ≠ clearance. No final admission, wrong source, unverified host capability/writer or no rights => **STOP before host probing**. Never invent PASS because earlier CODEX attempts worked.

### 2. ROUTE-SPECIFIC HOST PREFLIGHT, NO SYNTHETIC CODING PREEXEC

Within verified PowerShell 7 on FOXLE-PC, before inventory: check correct user/current process permissions, pinned CODEX CLI/model/effort and auth, Git repository origin, exact current branch/source lock, fresh one-writer for the dedicated result worktree, no consumed matching inventory task, safe Git result delivery and quota/capability statuses. `NOT_EXPOSED` quota or runtime telemetry must be reported as such; explicit mismatch/errors STOP. This is **READ_ONLY_AUDIT**, not an installed Bridge execution; do NOT rerun old Bridge PreExec or fabricate a coding PreExec PASS. A host-specific fresh admission check is required when material. Do not change PowerShell policy, OS protection, registry or Agent model to make a check pass.

### 3. READ-ONLY HOST INSPECTION

Use read-only Windows APIs / PowerShell queries on the actual FOXLE-PC:

- Current and legacy candidate roots (including `C:\Projects\FOX2-AgentBridge` and `%LOCALAPPDATA%\FOX2\AgentBridge`): existence, directory/reparse state, safe launcher metadata and presence/size of `data\bridge.db` and `data\manual_consumption.json`. **Do not open/read SQLite or marker contents, or record config secrets.** Do not follow reparse aliases outside expected root.
- Current installed pointer/launcher: existence and integrity category for `current.json`, `launch.ps1`, `desktop_launcher.ps1`; if needed validate pointer format without including its content in external reports. Record installed package/launcher version identity only in the private local evidence; no version-to-current-Git assumption.
- Processes: inspect bounded FOX2/Bridge executable/command signature and OS parent/PID relationships without copying raw command lines, environment variables, usernames, full filesystem paths or credentials into deliverables.
- Logon task `FOX2Bridge-<current SID>` and all FOX2-looking Scheduled Tasks (task state, trigger class, principal scope, action executable basename/signature only); inspect **per-user and machine** Run/RunOnce metadata, user/common Startup shortcut **targets** (not just filenames), and relevant Windows services. Classify uninspected entries and permission denied as `UNKNOWN`. Never execute targets.
- Legacy current-root interaction: identify whether an older executable, enabled scheduled task, autorun, service, shortcut or unknown third-party launcher might restart after current process exit. An absent process **now** does NOT prove retirement.

Collect each probe as `OBSERVED_PRESENT / NOT_OBSERVED_WITHIN_SCOPE / UNKNOWN / ACCESS_DENIED` plus which scope and time were actually inspected. Do not turn a missing task or unavailable privilege into definitive nonexistence.

### 4. HARD SAFETY, PRIVACY AND STOP

ABSOLUTELY FORBIDDEN: stop/restart/reconfigure Worker, start launcher or installed Bridge, edit/claim SQLite dispatch, modify `manual_consumption.json`, change Task Scheduler/Run/RunOnce/Startup/services, install/uninstall, activate Canary009/COMPAT001, execute provider/broker/LIVE, rewrite source, delete/clear old markers, merge/main/force-push/replay Attempts01–03, or trigger paid nested Agents.

Privacy: do not write raw host evidence to public Git. No raw SID/user/computer name, argv, registry data, private config, token, SQLite bytes, exact process paths or private executable file hashes in the public report. Keep any sanitized private inventory ZIP **outside repository**; do not upload it automatically. The only allowed public Git artifact is a minimum necessary allowlisted summary with generic root classes and states and explicit caveats, after local privacy/secret scan. If unable to prove privacy of the two public report files, **HOLD PUBLICATION** and deliver actual private file bytes by a verified private channel; otherwise mark `DELIVERY_BLOCKED`. Do not claim evidence independently reviewed by CHAT until real intake.

### 5. RESULT CONTRACT AND OBJECTIVE ACCEPTANCE

Commit ONLY the two named result files to the **dedicated non-main branch selected in final CHAT admission**, preferably `work/FOX2-BRIDGE-LEGACY-LIFECYCLE-READONLY-RESULT-20261020`; do not create code changes. Report Schema v2 uses the existing WP's `reports/<WP>/report.md` and `evidence_manifest.json`. No code or test file mutation. Include source locks, actor/route requested vs observed, timestamps, successful and UNKNOWN surfaces, counts/categories of possible active launchers, explicit `legacy_retirement_verified=NO`, hypothesis for restart/no-replay risk, limitations, privacy scan outcome, Git diff and allowed-path proof, and follow-up decision options without taking action.

Provide: (a) exact observed remote commit SHA **outside manifest**, (b) content hash/byte readback of both reports, (c) accurate PASS/FAIL/NOT_RUN statuses and host enumeration errors, (d) no-agent-replay/host-mutation attestation to the extent observable. Use a new one-shot task identity; if the host result state becomes ambiguous, STOP and ask CHAT to reconcile, never rerun.

**CHAT** will use `fox2-result-review` to check Git delivery, manifest, privacy and evidence limitations, and decide `ACCEPT_REPORT_ONLY / REWORK / HOLD`. Without comprehensive host evidence, CHAT retains `BUILD/BLOCKED` and selects fail-closed design instead of claiming a durable retirement.

### 6. FINAL EXIT

- If unverified legacy launch/retirement, result may be `OBSERVED_RISK / UNKNOWN`: this is a valid truthful inventory, NOT permission for Manual Local.
- STOP and return exact evidence/defect when unauthorized or unobservable; no pretend PASS, false host capability, or unapproved path expansion.
- `NEXT_OWNER=CHAT` for interpretation, source/update/acceptance. `CANARY009=HOLD`, Worker PAUSED status not newly re-attested, `INTERNAL_READY=NOT_ATTESTED`. **No autonomous background task.**

**PROMPT STATUS:** `GIT_CANDIDATE_NOT_FINAL_AGENT_DISPATCH` until CHAT verifies this immutable prompt publication and separately issues the task's current host-bound final admission.
