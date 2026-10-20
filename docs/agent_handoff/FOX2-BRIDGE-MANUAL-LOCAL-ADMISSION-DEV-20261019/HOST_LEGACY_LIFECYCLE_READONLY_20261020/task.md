# FOX2 Bridge — Host Legacy Lifecycle Inventory (new READ_ONLY host-evidence task candidate)

**Status:** `TASK_CANDIDATE / NOT_DISPATCHED / NO_AGENT_EXECUTION`. **Date:** 2026-10-20. **Existing Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`; **existing implementation WP:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`; **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` (`BUILD/BLOCKED`). This is a diagnostic task inside the SAME WP, not a new coding attempt or micro-WP.

## Owner objective / exact outcome

Determine actual FOXLE-PC legacy/current Bridge launcher, supervisor and startup surfaces without touching installed runtime state. Establish whether potential late or restarted legacy writer remains possible; distinguish `LEGACY_ENTRYPOINT_OBSERVED`, `NONE_OBSERVED_IN_BOUNDED_SCOPE` and `UNKNOWN`. **Never assert** `DURABLE_LEGACY_RETIREMENT_VERIFIED` from a one-time inventory. The immediate goal is evidence for CHAT to choose a safe cross-root no-replay design, not execution of manual admission.

## Source resolution, status and constraints

- **Owner-approved human task priority** is subject to exact scoped source decision; reference projectwide human governance Registry `d34da1e3b4918a902646621b487ca8ad3e05b0e0` and its Dictionary v1.3, Routing v1.4.0, Git-first Protocol v12. Machine installed Bridge adoption and runtime enforcement are separately `NOT_ATTESTED`. This source claim alone is not a live host authorization.
- **Accepted Attempt03 report-only BLOCKED:** `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581`; CHAT Result Review `c659100b785ee75fdbe12b851ee30ec1d3aaf352:docs/roadmap/FOX2_BRIDGE_MANUAL_LOCAL_ATTEMPT03_CHAT_RESULT_REVIEW_20261020.md`. All Attempts 01–03 consumed, **NO REPLAY**. Six no-replay assertions still FAIL; installed legacy actual presence UNKNOWN.
- **Authoritative candidate inventory contract:** `8f072f99c22a8201a3c6f04ba5dafa62ea55d2fc:docs/roadmap/FOX2_BRIDGE_LEGACY_HOST_LIFECYCLE_INVENTORY_CONTRACT_20261020.md`, Git blob `204da7e0b29acc44ff2d3e31baeb9daddcd4b5a0`.
- **Feature status (readback):** `4f14585f60a1044b2fc895331bfe4dd3077d6408:docs/roadmap/FOX2_FEATURE_STATUS.json`, feature `BUILD/BLOCKED`. **Result Schema v2:** `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`, Dictionary-selected, with `reports/<WP>/report.md` and `evidence_manifest.json` when a formal Agent handoff actually occurs.
- **Machine source for code inspection only:** `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581` on consumed Attempt03 result branch. Frozen versions/paths do NOT prove installed binaries or active launchers.
- **Candidate Agent route:** `CODEX | gpt-6.1-sol PINNED | medium | host PowerShell 7 read-only inventory | report-only Git result`; host capability, quota, fresh writer proof, permitted task scope and clean separate worktree are **PENDING**. Previously successful CODEX invocation is historic evidence, not a certificate for this task.
- `POLICY_CHECK`: human scoped governance source read; `TASK_STATE_CHECK`: existing WP, Attempts01–03 consumed; `SOURCE_RESOLUTION`: immutable context above; `R0-R7`: candidate routing only, **R3 capability and R5 writer still UNKNOWN**, `ASSIGNMENT_CHECK=HOLD_HOST_PROOF`. This task is not executable on publication; a separate CHAT final admission/host source binding is required if issued.

## READ_ONLY host inventory boundary

Using native **PowerShell 7 on FOXLE-PC**, inspect only: actual current/legacy root existence and reparse metadata, installed launcher file presence and allowed SHA256 of nonsecret launcher binaries/scripts, installed package pointer format/hash (not its contents), metadata-only `bridge.db` and `manual_consumption.json` existence/size, running FOX2-related processes (names and bounded root-category; never raw args), Windows current-user Scheduled Tasks (SID-qualified `FOX2Bridge-` task among candidates, but do NOT export actual SID), Task Scheduler state/triggers/action executable basename and matching signature, per-user/machine Run/RunOnce values by count/match only (no values), user/common Startup shortcuts by safe categories, and potentially relevant services. Record probe-specific `UNKNOWN/ACCESS_DENIED`, not absence. Include time, elevated status category, limitations and unenumerated startup surfaces. Never read credentials, raw ledger contents, config TOML or SQLite records, registry values, private command lines or sensitive environment variables. Do not follow linked paths outside intended roots.

No process stop/restart, Task Scheduler change, registry write, worker control, install/uninstall, Windows autorun enable/disable, Python Bridge initialization, schema migration, SQLite connection, broker/provider, Canary, protected Dispatch claim, or source-code modification. No CODEX coding nested agent. An inventory may write **sanitized temporary artifacts outside repo** and **two reviewed report-only Git files** on a dedicated non-main result branch after privacy inspection. Raw host inventory is private/local and MUST NOT go to the public repository.

## Assignment and result routing

A **new formal Agent handoff** (not this candidate) must use `fox2-agent-prompt-builder`: independently verify immutable task/prompt commit/blob/SHA256; repo and result branch; host PowerShell and pinned CLI; fresh one-writer and no competing host work; permissions and quota status; source-specific host PreExec only if materially required by chosen route. A READ_ONLY audit does **not** borrow Bridge coding PreExec or claim runtime readiness. No false `PASS` for unknown host capabilities.

Candidate result branch name: `work/FOX2-BRIDGE-LEGACY-LIFECYCLE-READONLY-RESULT-20261020`, to be reserved and verified before assignment. After exact result branch authority, delivery paths ONLY:
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json`

Git reports must be **privacy-safe high-level assertions ONLY**, allowlisted fields and statuses, with no raw hostname/user/SID/paths/raw commands/register values/tokens/hash fingerprints of private host files. Hold raw sanitized inventory ZIP locally for CHAT's private review; disclose only if a private, verified delivery channel is available. Never push raw ZIP to public Git. If privacy cannot be verified, STOP before push and mark `DELIVERY_BLOCKED`. Do not claim raw host evidence independently reviewed merely because a redacted result is Git-published. The observed remote result SHA is delivered outside committed report/manifest. CHAT must apply `fox2-result-review`, validate provenance/privacy and issue `ACCEPT / REWORK / HOLD`.

## STOP and next transition

STOP on missing or conflicting task/source binding, rights/host capability, writer status, data access ambiguity, inability to sanitize or verify a public report, any unintended host mutation, unexpected changed Git path, or already-consumed attempt. Preserve existing marker/receipts and Worker PAUSED. No main/merge, release, Canary009/COMPAT001, live provider/broker or installed runtime adoption.

**Current next safe action:** CHAT completes immutable task and prompt candidate publication/readback, selects route and verifies actual host capability/one-writer and result delivery. **No Agent execution or Owner-manual fallback has yet been authorized by this artifact.**
