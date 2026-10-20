# Attempt 02 result: BLOCKED at shared legacy admission dependency

Implementation WP: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019.
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY.
Attempt: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-OFFLINE-ATTEMPT-02.
Source/result parent: 65c50f7831722300a5418d0e9bc21f9f95988147.
Result branch: work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-02.

Status: BLOCKED. No manual entrypoint or production change is delivered. This submission contains six intentionally failing regression cases and four result artifacts. CHAT must independently review; no BUILD, acceptance, release or runtime adoption is claimed.

## Admission and source evidence

The clean worktree, exact branch, local HEAD and origin branch initially matched the pinned parent. The published task and prompt commit/blob/SHA-256 matched the executable prompt and injected FINAL_CHAT_ADMISSION. Independent Git read of chat_final_admission.json at d3d999de17f1c3833f03acaf327a2a549e798f85 returned blob 12579bb05809793f36a4942ad6e33f3cf16e3ba9, SHA-256 61e4fda77df6d9e4ca3e1084d8fe3eec5287415da322d9340f5e155388d13ee7; its bound identities and conditional assignment match intake. Recovery01 receipt has the pinned blob, PASS, nine material PASS capabilities and no blockers. Policy 2.0.0, Dictionary 1.3, Routing 1.4.0 and Protocol 12 were read at the Registry-selected commits; their declared blob/hash identities were checked. The Dictionary-selected Result v2 schema matches local schema bytes. Full source identities and raw captured test output are in test_summary.json.

Authority is the supplied Owner-scoped task and separate CHAT admission, with the immutable Owner grant read for exact scope; Git hashes alone are not an independent signature. Human governance authority does not establish installed runtime adoption. The prior BLOCKED receipts and Attempt01 history remain unchanged.

HOST VERIFIED evidence is accepted for the launch checks and retained named mutex as instructed. No second CLI, nested Agent, delegation, marker creation/deletion or re-launch occurred here. Requested model/effort: gpt-6.1-sol / medium; observed model/effort: NOT_EXPOSED; quota: NOT_EXPOSED. No contradictory telemetry was observed. Agent timestamps in the manifest bound the captured test/report evidence window, not an independently observed CLI start/end time.

## Exact excluded dependency and K1 reason

D1: agent_bridge/src/fox2_agent_bridge/desktop.py::initialize_runtime (lines 30-64) is the shared App and Desktop startup consumer. At line 34 it copies the legacy ledger only when the current DB is absent. When both DBs exist, a consumed legacy identity is absent from the current DB and claim_dispatch accepts it. Reproduced for FAILED, PUSHED_UNREVIEWED and NEEDS_RECONCILIATION.

D2: the same shared initializer reads manual_consumption.json only under the current root (line 47). A legacy-root valid consumed marker, or an unreadable marker with no legacy DB, does not prevent a current claim. These are fixtures under the patched legacy root, not the host attempt markers.

D3: the legacy ProcessLock at line 39 is held only for the migration snapshot. A deterministic race schedule holds the current root singleton, performs initial snapshot, acquires the now-free legacy root singleton and claims there, then successfully claims the same identity in the current DB. Both claims use honor_controls=True. The test demonstrates cooperating root locks, not hostile process behavior or a timing-dependent stress test.

agent_bridge/src/fox2_agent_bridge/ledger.py::claim_dispatch (lines 388 onward) correctly uses BEGIN IMMEDIATE and rejects any existing identity in its own DB, with PAUSED/stop checks when honor_controls=True. Its atomicity is confined to that DB. It does not establish a cross-root durable authority. This report does not allege broken same-DB SQLite atomicity or justify disabling controls.

Required shared behavior: establish one authoritative consumed-identity namespace or conservatively refuse unresolved coexistence before any claim; account for existing DBs and valid/unknown legacy markers; prevent a late legacy writer from invalidating migration evidence. This belongs in the shared startup/claim contract used by App, DesktopWorker and E2E/Ops, with restart-safe no-replay evidence. A one-off precheck or a second parallel manual marker/claim mechanism in the permitted entrypoint would leave other consumers and future legacy claims outside that contract. Do not duplicate the ledger/migration engine in e2e_runner.py or manipulate installed SQLite as a workaround.

Proven excluded source owner: desktop.py::initialize_runtime. Minimum scope for CHAT design/binding review: desktop.py and its corresponding test_desktop.py coverage, retaining the permitted test_e2e_runner.py reproductions. ledger.py is an impacted claim consumer/API and may require a separately justified exact binding if the chosen durable design needs it; this result does not assert that changing ledger.py or process_lock.py is unconditionally necessary. No excluded file was changed. Do not treat this report as approval of any proposed shared design.

## Actual tests and interpretation

From agent_bridge, with PYTHONPATH pointing to this worktree's agent_bridge/src and PYTHONDONTWRITEBYTECODE=1:

- python -m pytest -q -p no:cacheprovider tests/test_e2e_runner.py tests/test_project_dictionary.py: exit 1; 6 failed, 117 passed in 6.58s. All six failures are the new no-replay requirements above, not a passing negative test or XFAIL.
- python -m pytest -q -p no:cacheprovider tests/test_desktop.py tests/test_ops_runner.py: exit 0; 45 passed in 3.85s.

The 162 pre-existing selected tests passed freshly. They cover existing legacy v0.6/current schema normalization, automatic rejection of MANUAL_LOCAL, adapter fixtures, post-start failure/no replay, recovery stages and Desktop/Ops behavior. They do not establish the new manual feature. New manual positive admission, full authority/source/prompt drift and manual crash/delivery matrices: NOT_RUN because implementation stopped. Dedicated old PreExec v1 contract suite: NOT_RUN. No historical PASS substituted. No real Agent was launched by tests; adapters and transports are synthetic. No protected Dispatch001/Canary009, installed Bridge, Worker/scheduler or host attempt marker was accessed or modified.

## Delivery and next owner

Changed paths: agent_bridge/tests/test_e2e_runner.py plus report.md, evidence_manifest.json, test_summary.json and diff_trace.json under this WP report directory. Production source and test_project_dictionary.py are unchanged. The tests deliberately keep the affected suite red so the unresolved requirement remains visible.

K1 hunk trace is in diff_trace.json. Captured logs use disposable fixture identities only. Result-schema validation, evidence hashes, exact changed-path allowlist, secret-pattern scan and git diff --check are checked before delivery. The committed manifest records LOCAL_ONLY as its truthful pre-push state; the actual remote result SHA and verified pushed state are supplied separately after push, avoiding a self-reference or an invented successful delivery.

NEXT_OWNER: CHAT for independent Git Result Review and exact shared dependency scope binding under the existing Owner grant. Preserve the consumed Attempt02 state and reconcile; no blind Agent retry. This invocation will not implement excluded changes. No main/merge, install, runtime adoption, provider/broker, Canary, COMPAT001 or LIVE authority is exercised.
