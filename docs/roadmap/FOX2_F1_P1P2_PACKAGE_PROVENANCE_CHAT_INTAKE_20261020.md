# FOX2 — CHAT acceptance of passive P1/P2 installed package check (2026-10-20)

**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`; feature `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`; `BUILD / BLOCKED`. **Input provenance:** Owner pasted PowerShell 7 output `FOX2_F1_PACKAGE_P1P2_READONLY_V2`, captured `2026-10-20T15:01:05.1244310Z` (22:01:05 ICT), mode `READ_ONLY_NO_AGENT_NO_SQLITE`. CHAT can assess the user-provided output but has not independently accessed the Windows host, runtime module image or package archive. Because the repository is PUBLIC, this receipt intentionally does not publish package IDs, raw private path information, process identities or raw installed JSON.

## Observed result and independent Git comparison

- `last_phase=STABILITY_CHECK`, `errors=[]`, `pointer_receipt_stable=true`. `p1=PASS_POINTER_RECEIPT_CONSISTENCY` — accept internal pointer↔receipt consistency **only**. Package identity and inventory source SHA are well-formed values provided by the host, not independently trusted Git version binding.
- `payload_members_checked=252`, `payload_members_matched=252`, `payload_members_failed=0`; accept **payload↔manifest member consistency** for these observed entries, not complete installed wheel/runtime attestation or package/archive signature.
- `module_results` against frozen F0 commit `611ec26c28484de740e963d86de6b00946f1492d`: `installation.py=MATCH_F0_GIT_BYTES`, `launcher.py=MATCH_F0_GIT_BYTES`; `ledger.py=DIFFERENT_FROM_F0_GIT_BYTES`, `desktop.py=DIFFERENT_FROM_F0_GIT_BYTES`. Therefore `p2=HOLD_PAYLOAD_OR_MODULE_DIFFERENCE`, strictly **not PASS**. No exceptions; no file corruption inferred.
- `p3_independent_build=NOT_ATTESTED`, `worker_one_writer=UNKNOWN`, `legacy_retirement=NOT_VERIFIED`, `installed_admission=HOLD`.

CHAT independently remote-fetched historical Git blob identities. The two changed module families had the following exact **source byte** identities:

| File | Before F0 — commit `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581` and `65c50f7831722300a5418d0e9bc21f9f95988147` | F0 reviewed commit `611ec26c28484de740e963d86de6b00946f1492d` |
|---|---|---|
| `ledger.py` | Git blob `11e779f52b2518a9ac776cdc33192622c37e61df` | `e97ad916b3d78f085a106bad74bc0ddd2aec82f4` |
| `desktop.py` | Git blob `32005141e11ac126ef8944334f3e8f95139c0b8c` | `b835842eb72dfeba84c8a7c20eb7ec85076c4ae2` |
| `installation.py` | `9e7c1d07cce08536e5ca43a598632cff621c966c` | same |
| `launcher.py` | `0c2d8c7c737239521c4e32a6511f447c5634796f` | same |

`compare_commits(a3ad10d...,611ec26...)` verifies `ledger.py` and `desktop.py` are modified in that range; installing an earlier package is a **plausible, unproven** explanation for the installed byte mismatch. This is **NOT** a demonstrated malicious tamper, software installation failure, or an attested `a3ad10d` source build. Even if future two-module hashes match old source bytes, independent archive/source provenance P3 and active-process code identity remain unverified.

## Safety finding

F0 reviewed `desktop.py` calls `ledger.initialize(cross_root_authority_unknown=True)` and reviewed `ledger.py` denies direct claim under installed `BRIDGE_ROOT`. Both exact **claim-relevant** modules are different on the Owner-observed installed filesystem. The accepted F0 fail-closed source must therefore **not** be described as installed/runtime-enforced. Because Worker state is UNKNOWN, do not trigger `control status`, launcher, `setup`, start, resume, Agent/Dispatch or Canary to test whether live installed code can claim; deny any new Agent execution through Bridge until separately admitted.

## Scoped acceptance and next action

`ACCEPT_P1_POINTER_RECEIPT_INTERNAL_CONSISTENCY` · `ACCEPT_P2_MANIFEST_PAYLOAD_252_OF_252` · `ACCEPT_2_OF_4_F0_MODULE_BYTE_MATCH` · `HOLD_P2_F0_MODULE_PROVENANCE_2_MISMATCH` · `P3_NOT_ATTESTED` · `F1_INSTALLED_ADMISSION_HOLD`.

**NEXT_SAFE_ACTION:** one targeted read-only owner-host **two-module Git blob identity** observation for `ledger.py` and `desktop.py` in the exact version referenced by `current.json`, with stable pointer and path-reparse checks. Compare the two actual installed module Git blob SHA-1 identities to both immutable before-F0 and F0 anchors. Output only per-file comparison class and evidence flags; do not print local paths, raw JSON, credentials, SQLite contents, or execute Python. If neither matches, preserve `INSTALLED_SOURCE_UNKNOWN` and no automatic overwrite/reinstall. If both match old, classify `PRE_F0_MODULE_BYTES_OBSERVED`, **not** `APPROVED_OLD_PACKAGE` or `F0_RUNTIME_PRESENT`. Then require separate authenticated build/package/P3 and host retirement/one-writer gates before considering source-bound remediation.

Source/gov lock: Governance Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, Policy 2.0.0/Dictionary 1.3 CHAT operating scope, installed effectivity NOT_ATTESTED. F0 `611ec26...` offline scoped accepted only. F1 design `7a5af1457dd094d79d870f3eee9bc2d68e494882` candidate. CODEX Attempt06 consumed; no replay. `POLICY_CHECK/SOURCE_RESOLUTION/TASK_STATE/R0-R7`: CHAT-direct read-only review and single non-main evidence receipt, Git-only, no executable Agent. Prompt Builder N/A; Result Review applied as scoped result intake, not Agent Result v2 certification. Source Resolver, Feature Certification, Status Roadmap, Governance Preflight, Execution Recovery applied. **STOP:** no installed mutation, task/process startup/retirement, DB, Agent, main/merge, Canary/COMPAT001, provider/broker/LIVE.
