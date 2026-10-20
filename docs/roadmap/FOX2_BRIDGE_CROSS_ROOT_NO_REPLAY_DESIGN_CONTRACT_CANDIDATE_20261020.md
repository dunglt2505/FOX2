# FOX2 Bridge RC1 — Cross-root No-Replay Design Contract

**Stage:** DESIGN candidate; **status:** CANDIDATE_NOT_EFFECTIVE, NOT_IMPLEMENTED, NOT_RELEASED. **Whole-WP:** FOX2-BRIDGE-RC1-TO-INTERNAL-READY; existing feature FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION remains BUILD/BLOCKED. No new Whole-WP, Dispatch, Governance or Policy authority.

## Authority and immutable source evidence

- Accepted CHAT review: 3b4ebbed504911836f327b53e9f8da20a5dd0be6:docs/roadmap/FOX2_BRIDGE_MANUAL_LOCAL_ATTEMPT02_CHAT_RESULT_REVIEW_20261020.md. CODEX Attempt02 result dd3e46616c1f5dd2643eead3901ceaa1693cc6d6: six new no-replay tests FAIL, 162 selected existing tests PASS. No production code changed. Attempt02 consumed, no replay.
- Owner's standing exact conditional infrastructure engineering grant: c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json; no wildcard/no main/no merge/no Canary/no LIVE. Human scoped Policy 2.0.0 CODE-FIRST / machine Bridge RC1 frozen at f3d6468fedb553ba6c6192ba5811cb1b26a11ab9: different proof axes.
- Red tests are from dd3e46616c1f5dd2643eead3901ceaa1693cc6d6:agent_bridge/tests/test_e2e_runner.py, blob 7b2a2c48e6bf4225d849dc7a7a32126652b0c3be. The six red cases concern (3) consumed states in split ledgers, (2) legacy manual marker valid/corrupt, (1) late claim after migration snapshot.

## Current code facts

- desktop.py::initialize_runtime lines 30–64, blob 32005141e11ac126ef8944334f3e8f95139c0b8c: migrates legacy SQLite once ONLY if current DB is absent, locks legacy bridge.lock temporarily, reads manual_consumption.json ONLY in current root.
- ledger.py::claim_dispatch lines 388–430, blob 11e779f52b2518a9ac776cdc33192622c37e61df: BEGIN IMMEDIATE + duplicate identity denial is atomic only for ONE SQLite DB. honor_controls=True enforces local PAUSED/stop_requested, which must remain mandatory.
- process_lock.py, blob 37aaef1fdf0854d0dfbe90dda5919d5396a00a8c: lock is per file/root, not automatically a cross-root identity fence. The existing legacy executable may not understand new current-root markers.

## Normative acceptance invariants

I1. A claimed, consumed, FAILED, PUSHED_UNREVIEWED, NEEDS_RECONCILIATION or UNKNOWN identity in either root or valid/unknown marker cannot be admitted a second time. Missing/corrupt/ambiguous evidence is DENY, not fresh.
I2. An allowed claim must be protected by ONE durable identity authority with atomic checks covering both roots; a snapshot or separate SELECT-then-INSERT is insufficient.
I3. Deal with late legacy claims and legacy supervisor RESTART AFTER current supervisor exits. Merely holding the legacy lock for current process lifetime prevents cooperating overlap only during that lifetime; without durable legacy retirement/fencing or truly shared protocol, UNKNOWN coexistence means DENY new claims.
I4. PAUSED, stop_requested, one-writer, source/model/Owner hashes and normal BRIDGE-auto rejection of MANUAL_LOCAL remain independent denial gates. No honor_controls=False, unpause, installed ledger edits or duplicate manual ledger.
I5. Store monotonic and restart-safe UNKNOWN/BLOCKED/VERIFIED fence evidence (source roots, epoch/authority and decision reason), not a temporary in-memory flag. A generic resume cannot clear a cross-root ambiguity. Do not delete legacy DB/marker/lock.
I6. All App/Desktop/E2E/Ops claim paths must observe the same shared fence, including direct SQLiteLedger.claim_dispatch calls, not only a startup precheck. Exact Windows root/alias, file and launched executable identities are operational evidence needed for runtime adoption.
I7. Crash before/after legacy evidence read, atomic claim, Agent spawn and result delivery cannot clear a consumed identity. Fail-closed error must be actionable and test observable. Explicit source drift and unknown schema STOP.

## Selected approach for the next implementation attempt

**Preferred fail-closed two-phase transition, not a parallel MANUAL_LOCAL engine:**

1. Reconcile evidence from both ledgers AND both manual marker locations under consistent locks; do not overwrite historic consumed states. If current DB exists, legacy records still need consideration.
2. Bind a durable current-root admission fence to the SHARED claim path. Unknown/unproven legacy retirement or active/coexisting legacy writer => DENY claims (and retain PAUSED/stop guard). Code can perform isolated synthetic tests but cannot claim the installed legacy launcher is retired.
3. If the design uses both current and legacy OS locks, enforce consistent acquisition and release across BridgeApp and DesktopWorker; protect full admission lifetime as necessary. **Even lifetime double-lock is insufficient when a legacy executable can restart later**, so require separately observed durable retirement/fencing before positive installed admission, or demonstrate a backward-compatible single identity authority shared by BOTH executables.
4. Compare strict fail-closed mode against a joint-authority mode, state compatibility and rollback risks, and choose only a variant for which all negative acceptance tests can prove atomic no-replay. Do not fabricate a positive installed-runtime state from fixtures.

## Exact K1 scope binding for a NEW attempt

Original six authorized code/test paths:
- agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py
- agent_bridge/src/fox2_agent_bridge/e2e_runner.py
- agent_bridge/src/fox2_agent_bridge/app.py
- agent_bridge/src/fox2_agent_bridge/__main__.py
- agent_bridge/tests/test_project_dictionary.py
- agent_bridge/tests/test_e2e_runner.py

Four conditional paths now materially justified within the same Owner grant:
- agent_bridge/src/fox2_agent_bridge/desktop.py — NECESSARY_DEPENDENCY, shared initialize_runtime is crossed by all six failures.
- agent_bridge/tests/test_desktop.py — NECESSARY_DEPENDENCY, startup/legacy lock/control/marker regression coverage.
- agent_bridge/src/fox2_agent_bridge/ledger.py — NECESSARY_DEPENDENCY_FOR_CLAIM_TIME_FENCE, claim_dispatch currently accepts identities unknown to its own DB, direct callsites bypass initializer-only precheck. Restrict edits to specific compatible claim-time fence contract; give hunk-by-hunk K1.
- agent_bridge/tests/test_runtime_ledger.py — NECESSARY_DEPENDENCY, atomic refusal/concurrency/restart and SQLite transaction regression.

**Not bound for changes:** process_lock.py, ops_runner.py, config.py, project_dictionary.py, startup/install scripts, schema/generators or other code. Inspect them read-only where needed. Test_preexec.py can run as read-only regression. Any newly needed edit requires CHAT's separate exact consumer/K1 scope binding, not Agent expansion.

New attempt result contract: only reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/{report.md,evidence_manifest.json,test_summary.json,diff_trace.json} plus the ten exact code/test paths. A new isolated branch must NOT inherit Attempt02's historical report namespace.

## Gate-mapped acceptance

A. Preserve all six negative regression assertions; make them PASS through real shared code protection, never XFAIL/skip/delete/weaken. Include existing-current+legacy-DB, valid/corrupt legacy marker, late claim racing after snapshot.
B. Add synthetic positive MANUAL_LOCAL test ONLY with provable fenced authority; unknown/legacy-unfenced/paused/stop all deny. Test pinned Owner/source/prompt/model and old BRIDGE automatic selection rejection.
C. Test dual-root locks, lease lifetime and restart/resurrection, claim-before-spawn, crash windows and report-push ambiguity; don't launch a real Agent or installed Worker.
D. Fresh focused/negative and Desktop/Ops/RuntimeLedger/PreExec v1 regression with real exit codes; no historical PASS substitution. Assert exact allowed paths, diff-check, secrets, report manifest v2 and remote result SHA.
E. Independent CHAT diff/tests/source/result review required before BUILD accept; host legacy launcher retirement/quiescence and Canary are separate, not granted by offline green tests.

**Decision:** DESIGN CONTRACT PUBLISHED AS CANDIDATE ONLY; not an executable CODEX assignment. Preserve Attempt01 and Attempt02 markers/receipts/results. Never merge/main, resume Worker, trigger COMPAT001/Canary009, install, provider/broker or LIVE.

**NEXT_SAFE_ACTION:** isolate Attempt03 candidate source from PreExec clean base 65c50f7831722300a5418d0e9bc21f9f95988147, carrying only verified six red tests without old reports; publish a source-bound new task candidate; perform fresh native-specific host PreExec and then Prompt Builder exact immutable task+prompt+CHAT admission before invoking one new CODEX run.
