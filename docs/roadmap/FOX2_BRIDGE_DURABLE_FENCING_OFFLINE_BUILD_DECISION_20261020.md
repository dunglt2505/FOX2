# FOX2 — CHAT durable-fencing decision after FOXLE-PC host launcher attribution

**Recorded:** 2026-10-20 · **Whole-WP:** FOX2-BRIDGE-RC1-TO-INTERNAL-READY · **Feature:** FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION · **Stage:** BUILD / BLOCKED.  
**Decision type:** **ENGINEERING DESIGN LOCK FOR OFFLINE FAIL-CLOSED BUILD ONLY** (`DESIGN_DECIDED_FOR_OFFLINE_DEVELOPMENT / CANDIDATE_NOT_INSTALLED / NOT_EFFECTIVE / NOT_TESTED`). Not an Agent task, Dispatch, Provider permission or release. No declaration of durable legacy retirement.

## 1. Latest specific host evidence, provenance

Owner pasted read-only PowerShell JSON `FOX2_HOST_FINAL_LAUNCHER_ATTRIBUTION_V1` captured `2026-10-20T07:22:08.1889295Z` on FOXLE-PC. CHAT has **not** independently seen private Windows process table or filesystem bytes; report is user-host observation with `errors=[]`.

- PID 17036: `NOT_OBSERVED_AT_SNAPSHOT` (parent previously used by three current Bridge processes). Parent disappearance does not stop descendants or establish their control state.
- PID 18720: `ChatGPT.exe`, parent 10884, OTHER root and OTHER command reference. CODEX child PIDs 20300/25096: `codex.exe`, OTHER roots, OTHER command signatures; don't infer FOX2 writer absence or present one-writer PASS solely from these classifications.
- PIDs 16056 and 10940: `python.exe`, respective CURRENT/CURRENT and OTHER/CURRENT reference; PID 10476: `FOX2.Bridge.Desktop.exe`, CURRENT/CURRENT. Current Bridge processes were observed, **actual PAUSED/stop/ledger/claim state not independently attested**.
- Current SID Bridge scheduled task `Ready/enabled` at logon targets `CURRENT_REFERENCE` via `pwsh.exe`. Another time-trigger `OTHER_FOX2_CANDIDATE` is `Disabled`, action `FOX2_OTHER_REFERENCE`, not proven a legacy Bridge launcher. No action taken to start/disable/alter these.
- Legacy root `C:\Projects\FOX2-AgentBridge` still exists (prior host observation). Checked legacy `launch.ps1`, `scripts/desktop_launcher.ps1`, `scripts/desktop_startup.ps1`: `NOT_OBSERVED`. Legacy `data/bridge.db`: `PRESENT`, size 294,912 bytes, not a reparse point; **no DB bytes/rows consumed**, no proof of claim history from file size. Legacy `data/manual_consumption.json`: `NOT_OBSERVED`; absence of this one marker is not global absence of consumed identities.
- Earlier direct host observation: user Startup shortcuts 0 inspected, common 4 inspected without FOX2 match; current and 32-bit Run/RunOnce surfaces negative or absent; matching services 0. Every finding is a **bounded snapshot**, not proof of unlaunchability or retirement.

Sources:
- Last CHAT source-locked review `eb760d67bc6c98b444d56090646f34fbdb47c3fb:docs/roadmap/FOX2_BRIDGE_HOST_LIFECYCLE_ATTRIBUTION_REVIEW_20261020.md`.
- Frozen implementation source `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581:agent_bridge/src/fox2_agent_bridge/{desktop.py,ledger.py,process_lock.py}`; static code already shows initial copy only when current DB absent, temporary legacy lock, single-DB claim atomicity, no old-binary universal protocol.
- Attempt03 failed fixture evidence `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/test_summary.json`, CHAT independent review `c659100b785ee75fdbe12b851ee30ec1d3aaf352`. Six negative cross-root checks still FAIL; separate two-process current-exit/legacy-restart fixture duplicated a synthetic claim. Fixture is a *source-level gap*, not proof a legacy host executable ran.
- Engineering contract candidate `bd5cd44e31ceb7384b558c8fb08ccefd98dfb9e6:docs/roadmap/FOX2_BRIDGE_CROSS_ROOT_NO_REPLAY_DESIGN_CONTRACT_CANDIDATE_20261020.md`.
- Owner scoped authority `c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json`, **Owner intent recorded by CHAT (not independently signed)**. Conditional K1 path binding is specified in earlier approved engineering design. No Owner reapproval for the same scope; implementation still subject to source, host, PreExec, one-writer and Result Review gates.

## 2. CHAT safety decision — separate offline safeguard BUILD from installed positive admission

**DECISION F0: DENY BY DEFAULT** at every current-root dispatch claim until a **durable, independently provable cross-root authority/legacy retirement** exists. A transient process lock, a current-root-only marker, existence/nonexistence of `launch.ps1`, absence of a running legacy PID or copying SQLite once is **not** enough.

The execution invariant is **system-wide no new claim under unresolved authority**, not merely current process startup consistency. In particular:
1. Current process must never make a positive claim while the legacy writer may reappear and cannot observe current-root consumed identities.
2. If legacy consumed state, marker or DB content is corrupt, unreadable, inaccessible, schema-incompatible, changing concurrently, or host authority unknown, the only allowed claim outcome is `DENY/NEEDS_RECONCILIATION`, **without spawning Agent**. Reading SQLite rows is only permitted inside isolated synthetic fixture tests or a separately authorized read-only evidence route, not this Chat host intake.
3. `PAUSED/stop_requested/honor_controls=True`, durable claim-before-spawn and already-consumed identity checks remain independent guards. No rebranding `FAIL` as `PASS` or treating `NOT_RUN` as completed.
4. A **legitimate positive claim** requires separate operational evidence that old writer cannot restart or a single transactional identity authority verifiably honored by *both* old and current binaries. Merely asserting `legacy_retired=true` in an editable current-root config cannot satisfy this requirement.
5. Do not change the frozen legacy executable or task/registry/install state as a side-effect of offline source BUILD. No production Bridge claim/adoption happens through offline tests.

### Bounded offline implementation, once a NEW task/PreExec/one-writer is truly admitted

- Implement a **shared claim-time admission fence** in the allowed `ledger.py` interface, with strict fail-closed status/error, compatible with existing SQLite atomic transaction semantics. Ensure direct `SQLiteLedger.claim_dispatch`, shared Desktop/App/E2E and Ops consumers cannot bypass it when current installed-root mode applies. Default offline fixtures outside installed roots should remain valid for established old tests; don't silently activate positive installed admission based on a simulated retirement token.
- In `desktop.py::initialize_runtime`, preserve/inspect both-root consumed state, malformed legacy/current markers, already-present current DB, migration idempotence; never overwrite a consumed state; unresolved roots and racing/late legacy claims preserve DENY. Do not assume a current initial snapshot settles future legacy writes.
- When legacy retirement is **UNKNOWN**, explicitly fail the positive Manual Local acceptance. A test can check that the six negative regression cases now deny claims for a real reason; it must not mark positive installed runtime as READY. Synthetic positive testing may be performed only for a separately modeled jointly fenced authority with a hard separation from installed host settings.
- Requirement for crash/restart: fail-closed survives current process exit/restart, including legacy reappearance; do not assert cross-root global correctness if the old binary can still directly write to its private SQLite DB. Explicitly name the remaining **legacy-side limitation** instead of creating a dummy shared lock that old code ignores.
- Preserve six existing red regression test identities and assertions. Where semantics make a fixture positive claim disallowed, adjust **new bounded tests only** to prove DENY; do not remove/XFAIL/weaken protected red tests.
- Scope K1 carried from earlier design: six primary code/test paths plus the four proven conditional dependencies `desktop.py`, `ledger.py`, `test_desktop.py`, `test_runtime_ledger.py`. No expansion to `process_lock.py`, `ops_runner.py`, `config.py`, Windows startup/installer, dictionaries or Policy without a new exact consumer K1 and authorization.
- Tests: six cross-root negatives, failed/pushed/reconciliation legacy identities, malformed marker, current DB preexisting, late legacy claim after snapshot, current/legacy process restart, crash before/after claim, PAUSED/stop guard, no BRIDGE auto MANUAL_LOCAL, existing focused/desktop/ledger/ops/PreExec regressions and explicit positive `NOT_RUN/BLOCKED` if host retirement not provable. No actual paid Agent, installed worker, protected Dispatch, broker/provider, Canary.

### Distinct later gate F1: operational legacy fencing and admission

Do **not** start F1 now. F1 requires separately verified eligible legacy executable/launcher/root set and exact authority to disable/replace old entrypoints **with rollback and consumed-ID preservation**, or verified atomic shared DB/claim protocol understood by both versions, installed artifact SHA and repeatable restart/no-replay tests. Legacy `bridge.db` remains present and **must not be deleted or rewritten** as an administrative shortcut. Even if all F0 offline tests PASS, `MANUAL_LOCAL_POSITIVE_ADMISSION=HOLD`; Canary009/COMPAT001 stay HOLD.

## 3. SDLC, routing and continuation

**Stage:** BUILD · **Status:** BLOCKED (current result) · **Evidence:** Attempt03 six negative FAIL + host snapshot + this design decision. **Exit gate for F0 BUILD acceptance:** authorized implementation actually exists, synthetic negative tests PASS without weakening, backwards compatibility and code/reports reviewed independently; this decision alone proves NONE of those.

**Agent routing:** CHAT performs source resolution, design, test acceptance and Git intake directly. For coding, `CODEX/gpt-6.1-sol/medium` may be selected under existing Owner scope, **but no executable Attempt04 is issued here**. A new immutable task+prompt per `fox2-agent-prompt-builder`, correct Git result branch, fresh route-specific host PreExec/actual CLI capabilities, one-writer bound, current worktree and permission checks are needed. Two observed CODEX processes belong to a ChatGPT parent with no FOX2 command-line signature; this alone is NOT an exclusive-writer proof; host gate must inspect *relevant* writers, not assume every unrelated CODEX process blocks all tasks. Quota `UNKNOWN` until independently observed. No blind replay of coding Attempts01–03 or consumed host-audit task.

**STOP:** old writer lifecycle or shared authority unsupported for positive admission; any new test requires out-of-scope edits; installed Bridge Worker unknown/active/PAUSED status not independently attested; unexpected source/branch/path drift; unverified current one-writer; permission/quota unsupported. A host failure does not erase safe source-design work.

**NEXT_SAFE_ACTION:** progress authorized F0 **offline fail-closed implementation** as one Whole-WP task, starting with exact non-replayed task/source selection and new task-specific PreExec; keep F1 separately gated. Do not require another round of generic process/launcher inventory merely to draft offline F0. **GOAL_MET:** host attribution/decision yes; implementation no; release no.

**Skill routing:** `fox2-source-resolver=REQUIRED/APPLIED`, `fox2-execution-recovery=REQUIRED/APPLIED`, `fox2-result-review=APPLIED`, `fox2-governance-preflight=APPLIED`, `fox2-status-roadmap=APPLIED`, `fox2-feature-certification=APPLIED`, `fox2-agent-route-runtime=APPLIED`, `fox2-agent-prompt-builder=REQUIRED_ONLY_FOR_NEW_AGENT_ASSIGNMENT`.
