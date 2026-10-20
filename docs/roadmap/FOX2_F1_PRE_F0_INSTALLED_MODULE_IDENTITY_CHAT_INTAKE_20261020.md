# FOX2 — F1 installed two-module pre-F0 identity accepted / controlled adoption HOLD

**Date/time:** 2026-10-20T15:07:27.4232153Z (22:07:27 ICT). **Existing Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`. **Stage/Status:** BUILD/BLOCKED. **Mode:** CHAT-directed, read-only Owner-host snapshot intake and Git source review. **No Agent execution or installed change.**

## 1. Scope and provenance

Owner pasted `FOX2_F1_TWO_MODULE_GIT_BLOB_V1`, `mode=READ_ONLY_NO_AGENT_NO_SQLITE` with `last_phase=COMPLETE`, `errors=[]`, `package_identity_unchanged=true`, `pointer_stable=true`. Each module's repeated read was `stable=true`. These are **Owner-supplied point-in-time host observations**; CHAT has not independently verified running Python process image or cryptographically signed Windows evidence.

| Installed on-disk module | Owner-observed Git blob SHA1 | Independently Git-readback source match | Exact inference |
|---|---|---|---|
| `ledger.py` | `11e779f52b2518a9ac776cdc33192622c37e61df` | `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581` pre-F0 `agent_bridge/src/fox2_agent_bridge/ledger.py` | `MATCH_PRE_F0_MODULE_BYTES`; **does not match** accepted F0 blob `e97ad916b3d78f085a106bad74bc0ddd2aec82f4` |
| `desktop.py` | `32005141e11ac126ef8944334f3e8f95139c0b8c` | `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581` pre-F0 `agent_bridge/src/fox2_agent_bridge/desktop.py` | `MATCH_PRE_F0_MODULE_BYTES`; **does not match** accepted F0 blob `b835842eb72dfeba84c8a7c20eb7ec85076c4ae2` |

CHAT independently fetched the four source file blobs at both `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581` and accepted offline F0 source `611ec26c28484de740e963d86de6b00946f1492d`. The unchanged `installation.py` blob `9e7c1d07cce08536e5ca43a598632cff621c966c` and `launcher.py` blob `0c2d8c7c737239521c4e32a6511f447c5634796f` matched the previous host P1/P2 output and both source snapshots.

Previous Owner-host passive P1/P2 snapshot `2026-10-20T15:01:05.1244310Z` verified `P1=PASS_POINTER_RECEIPT_CONSISTENCY`, pointer/receipt stable, `252/252` payload member hashes match receipt manifest, two unchanged Python module byte matches, and two originally unresolved module mismatches. The latest V1 resolves only the identity of those **two on-disk Python module bytes**. It does not establish a complete before-F0 archive build, a trusted package signing/source chain, active Worker process module bytes, an exclusive one-writer lease, or legacy retirement.

For public-repository data minimization this file does not disclose the host's package SHA-256, source inventory SHA-256, local paths, config, credentials, process details or raw pointer/receipt JSON.

## 2. Corrected classification and non-promotion rules

**Accept:** `P1_HOST_REPORTED_PASS`, `MANIFEST_PAYLOAD_252_OF_252_PASS`, `FOUR_MODULE_BYTES_CLASSIFIED`, `TWO_INSTALLED_CRITICAL_MODULES_MATCH_PRE_F0_SOURCE`.

**Do not accept/promote:** `F0_INSTALLED`, `F1_INSTALLED_SOURCE_ATTESTED`, `P2_MATCH_F0`, `P3_INDEPENDENT_BUILD_PROVENANCE`, `WORKER_PAUSED`, `ONE_WRITER`, `LEGACY_RETIRED`, `POSITIVE_ADMISSION` or `CANARY`.

**Safety meaning:** reviewed F0 source `611ec26...` includes newer installed-root denials in `ledger.py::claim_dispatch` and `desktop.py::initialize_runtime`. Neither byte-identical F0 module is present at the two selected installed paths in this host snapshot. Their earlier equivalents do not independently establish current runtime enforcement, and no installed process/Agent should be activated merely to see whether old logic claims. The observed package can be *self-consistent internally* while lagging the accepted safety baseline. Do not attempt selective in-place replacement of two `.py` files inside a versioned package; that would break package provenance and create mixed-code conditions.

## 3. What CHAT can prepare, and remaining execution gates

The existing F1 Route A candidate remains selected **for offline design only**, see `7a5af1457dd094d79d870f3eee9bc2d68e494882:docs/roadmap/FOX2_F1_DURABLE_RETIREMENT_AUTHORITY_TRANSITION_DESIGN_CANDIDATE_20261020.md`. No new Agent task or dispatch is being created.

### A. Controlled safety-baseline adoption candidate — no install yet

1. Identify an **independently trusted, reproducible, immutable** F0-or-later fail-closed package archive (archive SHA, source file inventory, exact Git source, build toolchain, manifest, wheel content). No archive is attested in the present record. Rebuilding from Git is a new distinct action, not proof the installed archive is already compliant.
2. Host PreExec: establish current installed exact package/version identity, owner session/process lineage and quiescent Worker (including no Agent children, in-flight claims or published-but-unreviewed results), root-local and any legacy writer locks, safe paused/stopped lifecycle, rollback pointer and preserved both-root SQLite identities. **Do not invoke** `fox2_agent_bridge control status`, `launcher` or `setup` for a passive proof: code paths may initialize ledgers or spawn Worker/UI. A plain logon-task `Ready` state is not a Worker `PAUSED` assertion.
3. Separately verify all relevant legacy restart surfaces and an OS-/supervisor-enforced durable deny, effective after logoff/reboot/manual launch for admitted user and path scope. The previous 118 opaque non-Exec Scheduled Task actions and one disabled OTHER_FOX2 candidate remain bounded unknowns, not evidence of no possible legacy startup. No actual old writer invocation against live DB for testing.
4. Only after source-locked acceptance, Owner/route-specific PreExec and proven one-writer + quiescence: candidate **transactional versioned** adoption of F0 safety baseline (install verified package without tampering with old/current DB), readback exact installed Python bytes and pointer/receipt, then preserve DENY mode and PAUSED state. **Rollback must not turn old unsafe writer runnable** or lose consumed identities. No such install/adoption is authorized or executed by this receipt.
5. F0 baseline adoption is *not* F1 positive admission. F1 positive requires **new** trusted authority-transition code/acceptance plus durable legacy retirement and no-replay, under fresh task/rights/preexec. Owner's prior `gpt-6.1-sol` coding HOLD remains in force. Do not replay consumed CODEX Attempt06, COMPAT001, Canary009 or Dispatch001.

### B. Exact decision conditions

| Checkpoint | Result today | Next permitted work |
|---|---|---|
| Two exact critical installed module identities | `MATCH_PRE_F0_GIT_BYTES` — accepted scoped Owner evidence | STOP redundant source-identity rechecks |
| Current installed package self-consistency | `P1 PASS, payload 252/252 PASS` | Await P3 independently verifiable build artifact; package-level Git provenance not solved |
| F0 fail-closed installed runtime | `NOT_ATTESTED / OLD_MODULE_BYTES_OBSERVED` | Candidate controlled adoption only after permission and quiescence; no source edit in installed package |
| Legacy durable retirement and cross-root consumed-ID reconciliation | `NOT_VERIFIED` | Host-specific route design+authorized execution proof; preserve old data |
| F1 positive-claim source / installed gate | `NOT_IMPLEMENTED / HOLD` | Separate source-bound future F1 candidate acceptance and new task/preflight |
| Canary / Bridge Internal Ready | `HOLD / NOT_ATTESTED` | No activation before all release gates |

## 4. Governance, routing and STOP

Human operating authority: Registry `docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, Policy 2.0.0, Dictionary 1.3, installed effectivity NOT_ATTESTED. `POLICY_CHECK` scoped human permission for CHAT document/read-only reviews; `TASK_STATE_CHECK` existing Whole-WP, F0 offline accepted, F1 BUILD/BLOCKED, Attempt06 consumed/no replay; `SOURCE_RESOLUTION` immutable F0 SHA plus historical pre-F0 blob readback; `R0–R7` CHAT direct immutable non-main review, no new Agent/host activation, readback for Git writes; `ASSIGNMENT_CHECK=NOT_APPLICABLE`.

`NEXT_SAFE_ACTION`: proactively inspect repo for trusted package build artifact/release evidence; if unavailable, mark P3 `REAL_BLOCKER` and draft narrow source-bound host build/adoption prerequisites without invoking a paid Agent or Windows runtime. Do not request further redundant Windows inventories or repeat two module reads.

**STOP:** no in-place Python replacement, installed mutation, worker status/start/resume/exit/task toggling, local SQLite access, Agent/Dispatch, new CODEX run, merge/main, COMPAT001/Canary, broker/provider/LIVE.

Skill application: source-resolver, result-review (scoped Owner output, not Agent Result v2), feature-certification, status-roadmap, governance-preflight, execution-recovery, agent-route-runtime APPLIED; agent-prompt-builder NOT_APPLICABLE, no new assignment.

## 5. Newly resolved historical package lineage (Git archive report, not release attestation)

CHAT directly read the historic RC1 archive and result **metadata** at reviewed Git source snapshot `611ec26c28484de740e963d86de6b00946f1492d` (archive bytes were NOT downloaded or independently SHA256-hashed):

- Immutable archived binary Git entry `reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_recovery_003/FOX2-Bridge-RC1.zip` exists, Git blob SHA-1 `15450a648b70db79a94bf4a24fa69c879d0c4a49`, `64,479,644` bytes.
- Associated `FOX2-Bridge-RC1.json` Git blob `13ba36d017ce22a4292b4958741c0b83e5b2ddec` **declares** exact archive SHA-256 `a0516aed3d69564c657dc557b7b09cfaab549d6ab04ce4132e9399b50ce5b4ac` and `manifest.source_sha256=9990e91c9bb2f9d176dd5b2501294e0cfae9bd0eed6e32d92881754466d982a8`. Both declared digests match the Owner-observed installed pointer and receipt.
- Historical `installed_certification.json`, blob `75cf4718ad3b2f0be2adb3f6cf4051e9f741bd05`, references the **same pair** as installed `final_package` and `per_user_update`; its overall `status=PARTIAL_NOT_CERTIFIED`, not RELEASE_PASS, notwithstanding partial lifecycle checks. `final_runtime_readback.json` blob `dabad4a006232a048bc24d241d849867b07ed805` likewise identifies the same pair and says `certification=PARTIAL_NOT_CERTIFIED`. This is historical and does not certify 2026-10-20 runtime.
- Historical `quality_checks.json` blob `62c4a2b3c191ea06e104fe25dc479d9224c1a128` reports repeat deterministic archive SHA-256 `a0516aed...` and lists a `source_commit=c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`; **however**, CHAT directly fetched that older commit and it has `ledger.py` and `desktop.py` with the pre-F0 blobs, but `installation.py` blob `f88c84cdcc795ef35ebd8060994fcff83579210b` (unlike installed `9e7c1d07...`) and `launcher.py` is absent there. Therefore `c916de...` is not proven to represent every source byte in the archived package; a claimed freeze/quality report must not be used as immutable whole-package source proof without manifest-to-commit reconciliation.

**Updated scoped conclusion:** `HISTORICAL_ARCHIVED_PACKAGE_DIGEST_CLAIM_MATCHES_HOST_IDENTITIES` and `GIT_ARCHIVE_ENTRY_EXISTS`; `ARCHIVE_SHA256_INDEPENDENT_REHASH=NOT_RUN`, `WHOLE_BUILD_SOURCE_MAPPING=NOT_VERIFIED`, `P3=PARTIAL_HISTORICAL_LINEAGE_ONLY`, `F1_INSTALLED_RUNTIME=HOLD`.

**Efficient next step:** reuse this exact historical archive/receipt rather than request fresh blind artifact discovery. Before any adoption, independently rehash the archive bytes, validate its manifest and source inventory against an immutable code source set, and verify host one-writer/legacy retirement with route-specific preexec. If archive source remains pre-F0, it is **not** an acceptable F0 safety-baseline upgrade; identify or build a separately trusted newer archive with proper governance and source lock. Do not run or install this archived old package as remediation.

