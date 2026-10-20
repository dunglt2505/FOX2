# FOX2 — F1 durable legacy retirement and positive-claim authority transition: bounded design candidate

**Date:** 2026-10-20. **Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`. **Current stage/status:** `BUILD / BLOCKED`; F0 offline source/test subgates accepted. **Publication class:** `DESIGN_CANDIDATE_ONLY / NOT_EXECUTABLE / NOT_INSTALLED / NOT_OWNER_RELEASE_APPROVAL / NO_AGENT_ASSIGNMENT`. This is an engineering continuation within the existing WP, not a new WP/Dispatch, independent TechSpec release, runtime approval or Owner-override expansion.

## 1. Source resolution, evidence and threat model

- CHAT human-operating Governance Registry on Owner release branch `work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019`: `docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`; Policy v2.0.0 and Dictionary v1.3 for new/re-scoped CHAT coordination; installed runtime enforcement `NOT_ATTESTED`. Bridge TechSpec v0.7 REV10 remains candidate, not automatically promoted by this document.
- Immutable accepted F0 code snapshot `611ec26c28484de740e963d86de6b00946f1492d`; `desktop.py` blob `b835842eb72dfeba84c8a7c20eb7ec85076c4ae2`; `ledger.py` blob `e97ad916b3d78f085a106bad74bc0ddd2aec82f4`; `installation.py` blob `9e7c1d07cce08536e5ca43a598632cff621c966c`; `launcher.py` blob `0c2d8c7c737239521c4e32a6511f447c5634796f`; `desktop_startup.ps1` blob `543f9b93e6257eb03e876da78d50d6e41a756faa`; `desktop_launcher.ps1` blob `1db524e98324893076322fc1b87a59972998a4c8`.
- F0 review `62e7629b8fedcb47ff0ddb59d6e1d02b9df4cb09`; scoped alternate delivery `4d3330f8f0cf1f3aeaaacc611ff406301858ebbc`. Historical CODEX Attempt06 is `CONSUMED / AGENT_RESULT_V2_NOT_DELIVERED / NO_REPLAY`, not retroactively repaired.
- Current Owner host snapshots, most recent `2026-10-20T14:25:15.1956869Z`: 211 tasks, 213 actions, 95 actions exposing Exec properties, 118 non-Exec opaque actions, zero snapshot errors; current SID Bridge task Ready and another unclassified FOX2 task Disabled; legacy SQLite DB PRESENT at 294912 bytes; old launcher files ABSENT at named paths; three current-referenced Bridge/Python processes. Owner-reported executable identities: `FOX2.Bridge.Desktop.exe` and `fox2-bridge.exe`, reported hashes, no authenticated package/source mapping or process/lease proof. V3 intake `360009d28fc1a07da6d1dfb9805c34b8ecce2089`.
- **Threat:** a legacy executable or alternate launcher (including service, manual command, copied binary, scheduler/COM handler, recovery path) may restart after the current writer exits and claim the same dispatch ID against a different SQLite DB. One-time snapshots, disabled individual tasks, root-local file locks and a copied DB are insufficient. The operational objective is prevention of **accidental/authorized legacy restart under the attested Windows-user/environment boundary**. Do not claim an admin/malicious actor with unrestricted OS/code modifications can be cryptographically excluded without an actual independently verified OS policy/trust boundary.

## 2. Source-level findings and non-negotiable invariants

1. `desktop.initialize_runtime()` passes `cross_root_authority_unknown=True` for every configured runtime root; it does a one-time legacy DB copy only if the canonical current DB is absent, with a temporary legacy lock. The accepted F0 solution is strictly fail-closed.
2. `SQLiteLedger.claim_dispatch()` unconditionally rejects installed-`BRIDGE_ROOT` database paths **before** opening the transaction. Even if a privileged operator changes `bridge_meta.claim_authority` to `SINGLE_ROOT`, positive claims under that root still reject. This is a safety property, **not** F1 implemented admission.
3. Non-installed direct ledger fixtures can still allow `SINGLE_ROOT` under local SQLite BEGIN IMMEDIATE and controls; this does **not** demonstrate dual-root authority. Do not remove protected six negative cross-root tests or soften denial.
4. `installation.install()` verifies a package hash, creates `versions/<package_sha256>/payload` and a per-version isolated runtime; `current.json` carries `package_sha256` plus `source_sha256`, and `receipt.json` stores the package manifest. The latter source digest is a packaged source-file inventory digest, **not automatically a Git commit SHA**. The two observed `.exe` hashes alone cannot establish an installed package contains Git source `611ec26...` or future F1 code.
5. The installed stable `launch.ps1` resolves `versions/<package_sha256>/payload/scripts/desktop_launcher.ps1`; `desktop_startup.ps1` registers an SID-qualified logon task. The launcher may call `control status` or `setup` (which may initialize/mutate installed state), so neither launcher nor CLI status is an approved passive evidence collector.
6. `ProcessLock` uses a per-path Windows byte-range lock; the current worker/app take current-root `data/bridge.lock`. It does not forcibly protect the old root, old binary after current exit or copied executables.
7. Existing `certify_rc1_installed.py` is a **mutating** test harness (stop/start/control/resume, startup changes, install/uninstall/reinstall); it is NOT an F1 read-only check or newly authorized execution path.

**Invariant for any future F1 source:** deny unknown/failed/stale trust; ensure *every* installed claim call including direct `SQLiteLedger.claim_dispatch`, App, Worker, Ops and E2E sees the same authority gate immediately before the durable claim; retain controls, one-writer, claim-before-spawn, no-replay and denial on malformed legacy state; never rewrite/delete old DB or consent markers to create false freshness.

## 3. Chosen engineering direction: Route A conditional (retire legacy writer first)

**Decision:** `A_SELECTED_FOR_OFFLINE_F1_DESIGN_ONLY`: durably prevent the legacy executor from acting under the authorized ordinary-user startup and manual execution paths **before** any positive new-root authority transition. Route B (both old and new versions honor a common atomic consumed-ID authority) remains `NOT_DEMONSTRATED / NOT_SELECTED`; no evidence the legacy binary implements such a protocol, and an optional shim around one current launcher cannot bind arbitrary old launchers.

### A0 — Trusted inventory/closure, still READ-ONLY

- Establish the exact retired binary family: canonical file identity/hash and accessible copied older executables, launcher aliases/reparse/mount locations, owner/installer/supervisor process lineage and tasks/services/startup/COM-handler references **as related to FOX2**, not generic blind audits.
- Classify the second Disabled FOX2 task's action semantics privately; determine whether the 118 non-Exec actions have any FOX2-related COM handler/signature/indirect launcher. Unclassified entries remain `UNKNOWN`, not verified absent.
- Identify observed current `current.json` package identity and installed version receipt, but expose only a redacted verdict externally; read metadata privately, do not execute the launcher. Tie package `sha256`, `source_sha256`, manifest `files`, exact wheel+runtime module hashes and Git file inventory to a reproducible authorized build. Distinguish installed package identity from Git commit identity.
- Exit: signed/otherwise independently attestable scoped host-owner evidence, complete material launcher/alias closure and verified current supervisor/lease state. If incomplete, **STOP positive admission**.

### A1 — Retirement transaction preparation (EXECUTABLE/INSTALLED; NOT AUTHORIZED BY THIS DESIGN)

- Prepare an exact allowed target list of legacy binaries/launch surfaces/identities with immutable hashes, ownership and rollback plan; establish quiescence of legacy and current worker and no in-flight Agent child, durable execution/claim records, OS writer lock ownership, and a separately authorized paused/stop protocol.
- Capture privacy-protected, non-destructive consumed-ID/history and marker reconciliation across **both** roots using independently admitted read-only source/host evidence. Unknown/corrupt rows/markers => `RECONCILE_HOLD`. Never copy a live mutable legacy DB into a positive current DB and presume coherence.
- Establish OS-enforced restart denial for exact old runnable executables/authorized launch routes, resilient to logout/reboot and ordinary-user manual invocation; do not equate a Disabled task or missing `launch.ps1` with this. A fail-closed supervisor/deny policy must not rely solely on an easily reversible marker/config in the new root.
- Prove denial after attempted controlled re-entry using a harmless/non-consuming fixture or dry-run checker; **do not actually restart an old writer against either live DB as a probe**. Preserve old data, old claims and rollbacks.

### A2 — Authority transition source design (offline; a new separately gated BUILD task)

- Introduce an explicit, versioned `UNKNOWN -> RETIREMENT_EVIDENCED -> TRANSITION_STAGED -> POSITIVE_AUTHORITY_ELIGIBLE` state machine, with monotonic epoch, immutable source/package bindings, audited host retirement proof identity, target root and denied-on-rollback state. **This is a proposed contract, not a current schema or permission token**.
- Only a *trusted, separately reviewed host admission transaction* may authorize the terminal transition; neither edited TOML, `current.json`, an unauthenticated local JSON boolean, a task label, nor manually setting SQLite `claim_authority=SINGLE_ROOT` can grant positive claims.
- The new installed claim gate must check that terminal authority on **all claim paths** with durable state synchronization/transaction ordering; fail closed on process crash/ABA epoch rollback, unverified source/package, unsupported SQLite schema, disappearing fence evidence, old executable/process/launcher reappearance, missing OS writer ownership, control `paused/stop_requested`, or duplicate consumed identity.
- **Important TOCTOU requirement:** a successful once-only host verification followed by an unlocked `claim_dispatch` is NOT enough. Durable old restart prevention and its continued validity must cover the whole admitted claim/execution lifetime; before positive claim the current worker must hold an appropriate exclusive admitted control/authority lease, and denied-on-loss operation must be independently proven. A self-declared filesystem file alone is insufficient.
- Rollback policy: fail closed and preserve `CLAIMED/RUNNING/FAILED/PUSHED_UNREVIEWED/NEEDS_RECONCILIATION` history. **Do not roll back to an executable legacy worker** or clear old tombstones; revert to deny/current-paused if authority proof is lost.
- Source candidate K1: `ledger.py` (`NECESSARY_DEPENDENCY` claim-time check and versioned evidence), `desktop.py` (`NECESSARY_DEPENDENCY` runtime binding), `test_runtime_ledger.py` and `test_desktop.py` (`REQUESTED`). Conditional impacts `app.py`, `ops_runner.py`, `e2e_runner.py`, `installation.py`, `launcher.py`, Windows scripts and fixture config require concrete consumer-level K1 and a newly authorized exact task allowlist; do **not** treat this candidate as a blanket authorization to edit them.

### A3 — Acceptance and installed adoption (NOT_RUN)

- Offline synthetic tests: 6 frozen original cross-root negatives byte-identical; old writer late claim/restart even after current process exit; old binary copy/alternate-root/bypass; present/current DB with unknown authority; corrupt/unknown legacy marker; no duplicate consumed IDs; source/package drift; no-spawn on any gate failure; crash before/after durable retirement proof, authority transition, claim commit, Agent-spawn boundary; simultaneous old/current attempted claims; worker paused/stop and direct ledger claim path; invalid epoch/rollback; positive only with a *test-only* enforced retired-old authority whose trust boundary is clearly simulated.
- Exact installed provenance tests: validated trusted package hash + receipt+manifest+wheel/runtime file hashes, source inventory mapped to reviewed Git SHA; safe path/reparse checks; paused/quiescent state, unique writer/process tree, version-specific rollback and re-login/reboot restart evidence; failure to establish any is HOLD, not unrun PASS.
- Operational dual-root replay and one-shot MANUAL_LOCAL require NEW task identity, source/host PreExec, exclusive writer and immutable scope. Prior Attempt06, Dispatch001 and Canary009 remain frozen/consumed/HOLD per their own contracts. No paid Agent/Canary for design proof.

## 4. Material gate checklist

| Gate | State now | Exit condition |
|---|---|---|
| F1-D1 Source architecture and claimed positive-invariant contract | `DESIGN_CANDIDATE_PREPARED` | Owner/CHAT scoped design validation + precise consumer impact, no source contradiction |
| F1-H1 Legacy executable and all material start routes identified | `PARTIAL` | Identity+hash/alias+launch/supervisor closure, including relevant COM handlers and second task classification |
| F1-H2 Quiescent one-writer and no in-flight Agent | `UNKNOWN` | Independently observed host process/lease/control and protected record state |
| F1-H3 Old executor durably denied from restarting | `NOT_RUN/NOT_VERIFIED` | Exact target OS/supervisor rule and non-consuming restart-denial validation, rollback & reboot evidence |
| F1-D2 New trusted positive authority transition code/tests | `NOT_IMPLEMENTED/NOT_RUN` | Exact source-bound independently tested trusted authority contract, preserved negative/no-replay cases |
| F1-I1 Installed package / Git source / pointer/manifest provenance | `PARTIAL/NOT_ATTESTED` | Package and installed wheel module bytes verify against released candidate source and build manifests |
| F1-I2 Installed one-shot admission/restart/no-replay | `NOT_RUN/HOLD` | Fresh PreExec, authenticated source/runtime+one-writer, authorized one-shot and post-restart consumed IDs |
| F1-RC1 Canary and Internal Ready | `HOLD/NOT_ATTESTED` | Independent final release gates and explicit bounded operational authority |

## 5. Route, publication and STOP

`POLICY_CHECK=SCOPED_OWNER_GOVERNANCE`, `TASK_STATE_CHECK=EXISTING_WP_F0_ACCEPTED_F1_BUILD_BLOCKED`, `SOURCE_RESOLUTION=GIT_BYTES_VERIFIED_HUMAN_OPERATING_SCOPE_ONLY`. `R0` existing Whole-WP; `R1` offline F1 source DESIGN; `R2` Owner scoped infrastructure engineering approval but not installed activation; `R3` no host PreExec required for CHAT-only design publication; `R4` CHAT direct, no Agent; `R5` single non-main Git writing route and no code modifications; `R6` commit + remote readback; `R7` candidate-only, immutable evidence and F1 STOP boundaries; `ASSIGNMENT_CHECK=NOT_APPLICABLE`.

**NEXT_SAFE_ACTION:** perform CHAT direct consumer-impact/source-to-install identity mapping; prepare exact F1-D2 offline candidate acceptance without starting a coding Agent while `gpt-6.1-sol / medium` coding remains Owner-HOLD. At the first material installed action, require route-specific source lock, host one-writer, fresh PreExec/permission, rollback and signed/verifiable acceptance. If required evidence cannot be acquired, F1 remains BLOCKED and F0 continues deny-by-default.

**STOP**: no installed retirement/edit, task toggle, process control, live SQLite reads/writes, manual F0 flag changes, package install, Agent start, replay, Canary, COMPAT001, main/merge/provider/broker/LIVE. No retrospective Agent Result v2 acceptance.

**Skill coverage:** source-resolver, governance-preflight, feature-certification, status-roadmap, agent-route-runtime, execution-recovery, result-review = REQUIRED/APPLIED; agent-prompt-builder N/A because no new executable Agent handoff.
