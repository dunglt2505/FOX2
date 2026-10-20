# FOX2 F1 — Installed package identity: targeted passive read-only gate

**2026-10-20** · Existing Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`, opened feature `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` · `BUILD/BLOCKED` · **Gate:** `F1-I1`, bounded host attestation preparation · **State:** `PROTOCOL_PREPARED / HOST_CHECK_NOT_RUN / NOT_RELEASED`.

## What is source-verified versus not attested

Governance current for scoped CHAT work: Owner-released projectwide Governance Registry Git blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`; Policy v2.0.0, Dictionary v1.3; installed/runtime enforcement NOT_ATTESTED. F0 bounded accepted Git code `611ec26c28484de740e963d86de6b00946f1492d`, **not yet proven installed**. F1 candidate design at `7a5af1457dd094d79d870f3eee9bc2d68e494882` on the current CHAT non-main branch, not executable or effective. Original CODEX Attempt06 remains CONSUMED and AGENT_RESULT_V2_NOT_DELIVERED, no replay.

Actual code read: `installation.py` blob `9e7c1d07cce08536e5ca43a598632cff621c966c`; `scripts/build_user_package.py` blob `bae3b6c1ee89c9005f46f3afe3ac19a377123ffa`; `launcher.py` blob `0c2d8c7c737239521c4e32a6511f447c5634796f`. The installer stores `current.json {package_sha256,source_sha256}`, `versions/<package_sha256>/receipt.json {package_sha256,manifest}`, immutable-by-convention `payload/<manifest.files entry>` and `runtime/Lib/site-packages/fox2_agent_bridge/*.py`. A versioned directory, package manifest and pointer may all be mutually consistent while missing independent build provenance.

## Three separate proof levels

| Proof | Passive validation | What PASS establishes, and does not |
|---|---|---|
| P1 **Pointer/receipt** | `current.package_sha256` matches exact version folder and receipt package SHA; `current.source_sha256` matches receipt manifest source hash; reject absent/invalid/malformed/reparse | Internally coherent installed pointer only; does **not** prove source commit or signed package |
| P2 **Installed member bytes** | Verify each whitelisted manifest member hash against actual `payload` bytes, with safe relative names and reparse containment; compare `runtime/.../ledger.py` and `desktop.py` raw Git blob identities to exact F0 source blobs | Byte-level payload consistency and whether specific installed modules match F0 code; **not** whole runtime source/execution binding |
| P3 **Independent source/build and active process binding** | Independent trusted package artifact SHA + source build manifest→Git commit/file inventory plus live process executable/runtime mapping, immutable host proofs | `F1_INSTALLED_SOURCE_ATTESTED` only after full verification; P1+P2 cannot alone satisfy P3 |

**Specific Git module blob anchors** for P2 (SHA-1 Git blob identity computed over `ASCII("blob <length>\\0") + raw file bytes`, not merely file SHA-1): `ledger.py=e97ad916b3d78f085a106bad74bc0ddd2aec82f4`; `desktop.py=b835842eb72dfeba84c8a7c20eb7ec85076c4ae2`; `installation.py=9e7c1d07cce08536e5ca43a598632cff621c966c`; `launcher.py=0c2d8c7c737239521c4e32a6511f447c5634796f`. A mismatch is `SOURCE_DRIFT_OR_BUILD_NORMALIZATION_NOT_RESOLVED`, not release PASS. Match of two files alone does not certify every code path.

**Caution:** hash of `current.json` from Owner's 14:13 snapshot `60B3E2…` and the two observed EXE digests are historical machine evidence, not an immutable installed source lock. The `manifest.source_sha256` is a **source file inventory aggregate** from build code, not the Git commit SHA. Never compare them as if they were the same identifier.

## Exact bounded host route and privacy

One self-contained PowerShell 7 READ-ONLY procedure supplied fully **inline in CHAT** may inspect only `%LOCALAPPDATA%/FOX2/AgentBridge/current.json`, the derived `versions/<sha>/receipt.json`, whitelisted package member bytes and exact four installed Python module files. No raw JSON printed, no TOML, private credentials, secret-bearing logs or SQLite file rows, no process launch, no imports, no `control status`, no worker/control changes, no task edit, no uninstall/reinstall. A static output with statuses, count, per-module Git blob match verdicts, SHA identifiers, and errors is kept private in CHAT first. Only CHAT-reviewed sanitized summary may be published to this PUBLIC repository.

Verify `current.json` file hash before and after bounded read; if drift, `STOP_P1_P2`. Reject reparse/junction anywhere along derived path and path traversal in any manifest entry. Host signal `P1/P2_PASS` does not waive F1 legacy retirement, one-writer, source release or runtime claims. Missing receipt/package/digest, symlink, unexpected member, `SHA1` collision concern, unsupported schema or read errors => HOLD.

## Acceptance and actor

**Already completed:** source-side manifest semantics verified; exact F0 module Git blob identities bound, no Windows modifications. **NOT_RUN:** Owner host P1/P2, P3 trust chain, trusted OS-level legacy execution denial, worker one-writer and live task/dispatch records. **F1-I1:** `PARTIAL / NOT_ATTESTED`; **F1-positive-installed:** `HOLD`.

`POLICY_CHECK=SCOPED_OWNER_HUMAN_GOVERNANCE`, `TASK_STATE_CHECK=F0_ACCEPTED_F1_HOLD_ATTEMPT06_NO_REPLAY`, `SOURCE_RESOLUTION=F0_611EC26_AND_EXACT_BLOB_ANCHORS`; `R0` existing WP; `R1` host read-only evidence candidate; `R2` existing Owner infrastructure and CHAT intake scope; `R3` no executable PreExec for PASSIVE metadata reads, new runtime/Agent action requires fresh preflight; `R4` CHAT designs, Owner Windows host only if explicitly run; `R5` Git report-only non-main; `R6` remote readback; `R7` P1/P2 only; `ASSIGNMENT_CHECK=NOT_APPLICABLE`. No fresh agent/model selection.

**NEXT_SAFE_ACTION:** Acquire targeted Owner-host P1/P2 result (not another full general survey), assess package/source drift, then independently resolve P3/build provenance with verified artifact if present. Even with P1/P2 success, no positive claim, no legacy retirement, no Canary. Existing Owner coding HOLD remains; no micro-WP, git main/merge, broker/provider/LIVE, Agent retry, worker start or SQLite modifications.
