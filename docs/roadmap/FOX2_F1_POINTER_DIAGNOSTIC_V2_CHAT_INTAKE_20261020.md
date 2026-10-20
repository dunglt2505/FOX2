# FOX2 — CHAT intake: F1 current-pointer diagnostic V2

**Date:** 2026-10-20 · **Existing Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` · **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` · **Stage:** `BUILD / BLOCKED`.

## Owner-host evidence returned

Owner pasted JSON output of `FOX2_F1_POINTER_DIAGNOSTIC_V2` observed at `2026-10-20T14:55:19.7906286Z` using a read-only PowerShell diagnostic. This evidence is **OWNER_REPORTED_POINT_IN_TIME**, not direct CHAT host access, an independently signed runtime attestation, or an Agent result.

| Observed field | Value and bounded conclusion |
|---|---|
| `result` | `POINTER_READ_SUCCEEDED` |
| `last_phase` | `COMPLETE`; metadata, ancestor reparse check, file open, bounded read, hash, JSON parse and two identity format checks completed |
| `exception_type` / `hresult` | Both null; no exception in **this** run |
| `pointer_bytes` | 178 |
| `matches_previous_snapshot` | `true` — the SHA-256 matches Owner's earlier `2026-10-20T14:13:09Z` pointer snapshot; raw digest omitted from this PUBLIC receipt |
| `package_identity_valid` / `source_identity_valid` | Both `true`; **format only**, neither identity was compared with receipt or independent build source |
| `p1_pointer_receipt` | `NOT_VERIFIED`; no receipt accessed |
| `p2_payload_source` | `NOT_RUN`; no payload/modules accessed |
| `legacy_retirement` / `installed_admission` | `NOT_VERIFIED` / `HOLD` |

**Result review:** `ACCEPT_SCOPED_POINTER_READ_AND_HISTORICAL_DIGEST_MATCH`, `PREVIOUS_POINTER_IO_EXCEPTION_NOT_REPRODUCED`, `ROOT_CAUSE_UNKNOWN`. The previous `POINTER_IOException` at `2026-10-20T14:49:58Z` remains a real historical error, not erased or explained by the subsequent successful read. The result does not certify package consistency, active runtime integrity, permission status, legacy retirement, one-writer, or F1 positive claims.

## Source, state and next bounded action

Governance Registry on approved human governance release branch: blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, scoped Policy v2.0.0, Dictionary v1.3, installed enforcement `NOT_ATTESTED`. Source `611ec26c28484de740e963d86de6b00946f1492d` remains only the independently reviewed F0 offline source; no installed SHA attested. Related source-locked passive gate: `2785584be4dcaef560f20b3a607c445d442de55f:docs/roadmap/FOX2_F1_INSTALLED_PACKAGE_PROVENANCE_READONLY_GATE_20261020.md`. Previous I/O failed intake: `e863afbff96209f55ceaebc0c025fef5bb3d6df8:docs/roadmap/FOX2_F1_PACKAGE_PROVENANCE_POINTER_IO_CHAT_INTAKE_20261020.md`.

`NEXT_SAFE_ACTION`: do **not** rerun the entire historical host inventory or diagnostic; run a single targeted read-only P1/P2 **receipt, payload, and four F0 module-bytes** audit, keeping the pointer step minimal and using share-permissive read-only handles; compare before/after pointer and receipt hashes for stability. Report counts/status only, no raw installed JSON/config/secret paths. If any read is blocked, record exact phase and HOLD; no stop/unlock/modify of installed Worker is authorized. P1/P2 matching cannot supply P3 independent build provenance, worker state, durable legacy retirement or positive admission.

`POLICY_CHECK=SCOPED_OWNER` · `TASK_STATE_CHECK=F1_BUILD_BLOCKED_ATTEMPT06_CONSUMED_NO_REPLAY` · `SOURCE_RESOLUTION=OWNER_GIT_F0_SOURCE_BYTE_LOCK_ONLY` · `ROUTING_R0_R7=CHAT_DIRECT_OWNER_PASSIVE_HOST_READBACK_NONMAIN_REPORT` · `ASSIGNMENT_CHECK=NOT_APPLICABLE`, no Agent task. Applicable Skills: source-resolver, result-review, feature-certification, status-roadmap, governance-preflight, execution-recovery APPLIED.

**STOP:** no Windows executable/task manipulation, no Bridge status/launcher/setup/pause/resume/start, no SQLite reads/writes, Agent Dispatch, Canary/COMPAT001, main/merge/provider/broker/LIVE.
