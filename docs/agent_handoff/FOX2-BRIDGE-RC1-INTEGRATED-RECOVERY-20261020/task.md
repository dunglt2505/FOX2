# FOX2 — One integrated Bridge RC1 recovery / offline BUILD+TEST task

## Identification
- Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` (existing, **not** a new micro-WP).
- Attempt: `FOX2-BRIDGE-RC1-INTEGRATED-RECOVERY-20261020-ATTEMPT-001` (NEW, no previous execution; do not reuse Attempt06, Dispatch001, COMPAT001 or Canary009).
- Type: **source-bound offline engineering, tests and verifiable F1-capable packaged candidate**. Does **not** authorize installed Windows adoption, stopping existing Worker, legacy OS policy changes, SQLite live reads/writes, positive claim activation, canary/main/LIVE.
- Branch: `work/FOX2-BRIDGE-RC1-INTEGRATED-RECOVERY-20261020` created from immutable code+docs head `c3af81429b389bb3301effc96c68fbf88744aeff`. Branch is the sole allowed code writer for this attempt; no branch rebind.
- Engineering source base: `c3af81429b389bb3301effc96c68fbf88744aeff`; accepted offline F0 code source `611ec26c28484de740e963d86de6b00946f1492d`, exact `ledger.py` blob `e97ad916b3d78f085a106bad74bc0ddd2aec82f4`, `desktop.py` blob `b835842eb72dfeba84c8a7c20eb7ec85076c4ae2`.
- Governance: Owner-released human Registry `docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, Policy v2.0.0/Dictionary v1.3 human scope, machine installed enforcement NOT_ATTESTED. Technical candidate v0.7 REV10 remains CANDIDATE, never silently EFFECTIVE. Immutable RC1 release plan and existing 8 F1 admission gates govern their original contexts.
- Direct Owner authorization: latest 2026-10-20 instruction `Owner ra lệnh thực hiện ngay, dứt điểm Bridge`. CHAT treats this as a **new scoped mandate to progress offline engineering** and to prepare a valid Agent route, **not** waiver of PreExec, no-replay, host safety, historical outcomes or installed release gates. Previous pinned CODEX choice `gpt-6.1-sol / medium` is preserved.

## Integrated outcome (ONE cohesive code/test attempt)
1. Source truth: review existing dual-root/old writer/current worker, F0 tests, immutable Dispatch/Agent semantics; do not rewrite working Git-first Core, WPF UI or versioned package architecture.
2. Design and implement a secure, versioned **claim authority interface** that remains fail-closed by default and on malformed/unknown/stale host retirement proof; no edit to ordinary SQLite metadata or current.json may grant positive claims. Code must specify external trust anchor and verify authenticity, source/package identity, epoch anti-rollback, fresh owner/lease, and continued old-writer retirement coverage for the full claim/execution lifetime. If OS enforceability is impossible within allowed scope, **do not implement a fake positive unlock**; preserve F0 denial and produce an exact bounded BLOCKER in result, with offline simulations.
3. Bring direct `SQLiteLedger.claim_dispatch`, runtime initialization, App/Worker, Ops/E2E claim-before-spawn and control paused/stop onto one check; protect alternate config root, path aliases/symlinks, distinct SQLite roots, legacy restart after a snapshot, crash and race conditions; keep all six protected F0 negative tests.
4. Preserve both-root consumed dispatch IDs and manual markers as historical/uncertain on migration; no deletion, replay, false unconsumption, clearing `DENY_CROSS_ROOT_UNKNOWN`, or unsafe rollback to old runnable binary. Design the guarded retirement transaction and dry-run/negative evidence mechanism; don't touch real host.
5. Add synthetic authority/fence/concurrency tests for denial, positive only in a truly *simulated independent enforced* retirement environment, replay/no-spawn, race, restart/crash, invalid signatures/epochs, source mismatch, control pause, direct ledger bypass, source/installed artifact mismatch and time-of-check/time-of-use loss.
6. Preserve installer architecture with one package build that defaults DENY, source file inventory→immutable Git source, manifest/wheel/runtime module hashes; produce deterministic candidate archive if Windows tooling available, otherwise truthful `NOT_RUN_HOST_CAPABILITY` and no package assertion. Do not modify installed Python files or certify old RC1 archive.
7. Run focused + full feasible automated tests and static checks, report exact counts/failures/skips, diffs, K1 impact, and immutable source/package SHA. No original Agent replay. Nothing mutates `main`.

## Exact allowed WRITE paths
`agent_bridge/src/fox2_agent_bridge/ledger.py`
`agent_bridge/src/fox2_agent_bridge/desktop.py`
`agent_bridge/src/fox2_agent_bridge/app.py`
`agent_bridge/src/fox2_agent_bridge/paths.py`
`agent_bridge/src/fox2_agent_bridge/process_lock.py`
`agent_bridge/src/fox2_agent_bridge/installation.py`
`agent_bridge/src/fox2_agent_bridge/launcher.py`
`agent_bridge/src/fox2_agent_bridge/config.py`
`agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
`agent_bridge/src/fox2_agent_bridge/ops_runner.py`
`agent_bridge/src/fox2_agent_bridge/__main__.py`
`agent_bridge/scripts/build_user_package.py`
`agent_bridge/scripts/desktop_startup.ps1`
`agent_bridge/scripts/desktop_launcher.ps1`
`agent_bridge/scripts/install_user.ps1`
`agent_bridge/tests/test_runtime_ledger.py`
`agent_bridge/tests/test_desktop.py`
`agent_bridge/tests/test_installation.py`
`agent_bridge/tests/test_rc1_package.py`
`agent_bridge/tests/test_e2e_runner.py`
`agent_bridge/tests/test_lock_logging_health.py`
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/*` (**sanitized text only; no binary secrets/raw host logs**).
No code outside allowlist without CHAT impact approval, new immutable task amendment and host gate. Generated caches/test files must not be committed.

## Execution / acceptance gates
- Before running CODEX: true `codex` CLI and pinned model capability, explicit offline worktree / branch / source / clean status, repo permission, one-writer and no-replay check, material Windows host PreExec (Git, Python, PowerShell and required test/build tools); no generic historical Bridge bootstrap receipt reused as EXEC PASS.
- Branch checkout source must match **the final published task/prompt commit**, verified immutable task+prompt Git blobs and SHA-256; `CODEX gpt-6.1-sol`, reasoning `medium`, bounded local coding workspace, Git push **only** the dedicated non-main result branch. No Git write to other branches.
- Offline test gate: original six F0 negatives and direct bypass denial, new concurrency/rollback/host-fence tests, all existing appropriate regression. Missing test is `NOT_RUN`, not PASS.
- Packaging: package manifest, archive hash and installed-source evidence is distinct from successful code tests; no attribution of live Worker state from installed on-disk files.
- Result Contract: actual `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md` + `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json` plus implementation/tests in allowed paths; K1 labels `REQUESTED/NECESSARY_DEPENDENCY/JUSTIFIED_GENERATED/UNEXPLAINED/NOT_VERIFIED`, test command/results, limitations, permissions, STOP and next safe action. Agent must push exact Git code/report to this branch and communicate **observed remote result SHA outside files**. If Git push unavailable, leave real files in allowed worktree and report exact path + hash; CHAT must publish under separately verified rights. Git push != CHAT acceptance.
- Post-result CHAT independently remote-readbacks status, source, diff, tests and report; verdict `ACCEPT / REWORK / HOLD`. Only after accepted offline package and fresh Owner/host PreExec does a **separate explicit installed adoption** transaction become eligible.
- STOP if source/permission/tool/host/writer ambiguity; do NOT silently swap CODEX model or compute flags, fake test PASS, invoke Agent on a live dispatch, mutate existing SQLite roots, enable worker, Canary or LIVE.

## Release remainder (not part of executable code assignment)
F1 host G1–G8: durable retirement verified after logoff/reboot without touching live claim paths, both-root consumed identity reconciliation, one-writer/no-in-flight, exact package-to-Git build provenance, fail-closed staged install + rollback, explicit positive claim activation with fresh admission, one-shot no-replay, fresh RC1 UI Artifact Vault acceptance, independent final audit and separate Canary009 permission. This task's successful offline code may clear BUILD tests but **never** automatically clear installed/TEST/DEPLOY gates.
