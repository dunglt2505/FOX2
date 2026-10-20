# FOX2 — CHAT intake: F1-I1 passive package-provenance pointer I/O failure

**Date:** 2026-10-20. **Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` · **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` · **Status:** `BUILD/BLOCKED` · **Mode:** `OWNER_HOST_REPORTED_READ_ONLY_RESULT / CHAT_DIRECT_REVIEW`.

## Exact returned evidence (not fabricated retest)

Owner pasted PowerShell 7 console JSON with `schema=FOX2_F1_PACKAGE_PROVENANCE_PASSIVE_V1`; `observed_utc=2026-10-20T14:49:58.5187425Z`; `mode=READ_ONLY_NO_AGENT_NO_SQLITE`; declared `source_reference=611ec26c28484de740e963d86de6b00946f1492d`.

- `error_codes=["POINTER_IOException"]`, **phase = POINTER**, exception type `IOException` (no full exception HResult, message, stack trace, step-level information).
- `package_sha256=null`, `source_inventory_sha256=null`, `pointer_stable=false`, `receipt_stable=false`.
- `payload_members_checked=0`, `payload_members_matched=0`, `payload_member_failures=0`; `module_results=[]`.
- `p1_pointer_receipt=HOLD_OR_NOT_VERIFIED`, `p2_payload_source=HOLD_OR_NOT_VERIFIED`, `p3_independent_build=NOT_ATTESTED`.
- `worker_one_writer=UNKNOWN`, `legacy_retirement=NOT_VERIFIED`, `installed_positive_admission=HOLD`.

The first exception happened before P1/P2 reached the package/receipt or file-hash comparisons. **This proves an attempted passive read encountered an I/O error; it does not prove package corruption, source mismatch, missing files, or false content.** The previous Owner-host snapshot `2026-10-20T14:13:09Z` observed a pointer present and obtained a hash; this is a historical observation, not proof of the pointer's present readability or unchanged bytes.

`POINTER_IOException` could originate in `Assert-PlainPath` / `Get-Item`, `Get-FileHash`, `Get-Content` or path resolution, and the script did not label individual statements. It is not currently evidence of any specific sharing violation, ACL, link problem, filesystem corruption, or concurrent package upgrade. No retry or state modification was authorized/performed by CHAT.

## Scoped gate disposition

| Gate | Truthful state |
|---|---|
| Passive host test execution | `ATTEMPTED / POINTER_IO_BLOCKED` |
| F1-I1 P1 pointer↔receipt | `NOT_VERIFIED` (failed before receipt) |
| F1-I1 P2 payload hashes + 4 module Git blobs | `NOT_RUN` (0 members/modules inspected) |
| F1-I1 P3 independent build/source/process trust | `NOT_ATTESTED` |
| F1 legacy retirement | `NOT_VERIFIED` |
| Worker exclusive control | `UNKNOWN` |
| F1 installed positive admission / Canary | `HOLD / NOT_RUN` |

Governance is scoped to CHAT documentation and authorized evidence intake; projectwide Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, Owner Policy 2.0.0, Dictionary 1.3, installed enforcement `NOT_ATTESTED`. Immutable source/test F0 `611ec26...`, F1 design candidate `7a5af1457dd094d79d870f3eee9bc2d68e494882`; previous F1-I1 gate `2785584be4dcaef560f20b3a607c445d442de55f:docs/roadmap/FOX2_F1_INSTALLED_PACKAGE_PROVENANCE_READONLY_GATE_20261020.md`. No CODEX Attempt06 replay or delivered Agent Result v2 is implied.

## NEXT_SAFE_ACTION — one precise pointer diagnostic, not another full inventory

If OWNER continues host checks, run a **single bounded read-only PowerShell 7 pointer diagnostic**, fully printed inline in CHAT, which: (a) reports exactly which step (file/path metadata, handle open, read, JSON parse) fails; (b) emits safe exception **HResult** without the raw OS message/path; (c) uses a *read-only* FileStream with `FileShare.ReadWrite | FileShare.Delete` and at most 4KiB read to distinguish normal sharing restrictions from an actual unopenable pointer; (d) reports only validated SHA-256 identifiers and status, no raw JSON; (e) compares to historical pointer hash only as reference, not a source authority; and (f) fails closed if a separate installed process holds incompatible exclusive sharing, file changes, or invalid structure. It must not use the installed launcher or Bridge CLI, pause/resume Worker, query SQLite, override ACL/sharing, or cause package changes.

Only after pointer success can P1/P2 package/manifest comparisons legitimately be resumed. A deliberate I/O failure remains `HOLD / BLOCKER=HOST_IO`, not a reason to clear deny, install or retry an Agent. Do not make repeated broad host audits for this narrow blocker.

`POLICY_CHECK=SCOPED_OWNER_HUMAN`, `TASK_STATE_CHECK=EXISTING_WP_BUILD_BLOCKED_ATTEMPT06_CONSUMED`, `SOURCE_RESOLUTION=GIT_F0_611EC26`, `R0-R7=CHAT_DIRECT_READ_ONLY_RESULT_INTAKE_AND_NONMAIN_GIT_RECEIPT`, `ASSIGNMENT_CHECK=NOT_APPLICABLE`, `PREEXEC_HOST_AGENT=NOT_APPLICABLE`. Skills: source-resolver, governance-preflight, feature-certification, status-roadmap, execution-recovery, agent-route-runtime APPLIED; prompt-builder NOT_APPLICABLE because no new Agent assignment.

**STOP:** no operational retirement of legacy, process/task controls, installed scripts/packages/DB modifications, Agent dispatch, Canary/COMPAT001, main/merge/provider/broker/LIVE.
