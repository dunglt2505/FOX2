# FOX2 — Bridge RC1 Pre-Canary Independent Audit: CHAT Evidence Intake and WORK Handoff
**Date:** 2026-10-18
**Status:** `CHAT_GIT_EVIDENCE_CHECK_PASS / WORK_INDEPENDENT_AUDIT_PENDING / NO_PRECANARY_READY`
**Project:** FOX2 ONLY
**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
**Nature:** Read-only, independently checked source/evidence handoff; this document is NOT WORK's audit report, not an independent certification, not a new executable Dispatch, and not Canary/release permission.

## 1. Authority and exact boundary

- Implementation outcome at `work/FOX2-BRIDGE-DESKTOP-BATCH-B` commit `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9` was produced by CODEX Dispatch `FOX2-DISPATCH-BRIDGE-RC1-CODEX-004`, max_runs=1, consumed. Source/worktree were bound to `dbaefdf686e06ffdf78b277288515deca9011710` / evidence-only PreExec `0789e5d8c3944fdc078090f50f18fb2a3abe6b64`.
- The authoritative Whole-WP task `docs/agent_handoff/FOX2-BRIDGE-DESKTOP-BATCH-B/task.md` section 11 expressly designates **WORK** for required independent pre-Canary release-readiness audit after implementation/installed PASS. This requirement governs the next step; CHAT cannot self-declare a WORK audit PASS merely by reviewing Git.
- RC1 WP-only trusted Registry `b27f1085ee13d8dce56fd2735e100ea1616e6e23:docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json`, manifests and approved Owner source-scope at `d8e2331674ef1921844f369bfa9e48b82a73c6a1`, immutable source `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`. No projectwide Governance promotion or main/merge/DEV/LIVE rights.
- Source lock remains Dictionary v1.2 / Policy v1.8.9 / Routing v1.3.0 / Git-first Protocol v12, not prospective Governance candidates.
- Current observed Git heads: Bridge `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`; control `dc79f8143eec471508bf37565bff38442ce0548a`; Canary 009 `501822a33ef08c7365154913bbc677544856eee5`; APP-B `fc8aba202e15bddfcc5156b2c1bb36ed222329eb`; all identical to recorded source snapshots when checked by CHAT.

## 2. Independently rechecked by CHAT (not by WORK)

**Acceptance matrix:** 40 entries: 38 PASS, `PRECANARY_INDEPENDENT_AUDIT=PENDING`, one non-gating `ICON_NON_GATING_NO_AUTHORIZED_ASSET`. `INSTALLED_RUNTIME_TECHNICAL_CERTIFICATION=PASS` is an implementation claim supported by its immutable Git evidence; no installed-host rerun occurred in CHAT.

**Git cryptographic checks:** CHAT independently computed SHA-256 from authenticated Git file bytes using a separately implemented SHA-256 with known-answer self-test. Exactly 6/6 sampled critical files matched the declared `evidence_manifest.json` digests:
1. `reports/BRIDGE-DESKTOP-BATCH-B/report.md`: `df8f358e04fb86288c3299b2d9eeb81dcbcc7fba4dfd77e38fd5ab645f492b66`
2. `reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_final_closure_004/acceptance_gates.json`: `6c77535b77b191156a1b3c2ea4ee8f80a0c831598eb129a63c4c3f7223995035`
3. `reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_final_closure_004/artifact_ui_certification.json`: `1467b561b419fcbda01b2c29d39fb5359793a29531e5edcf52225c339e0a4862`
4. `reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_final_closure_004/atomic_index_events.json`: `b82237e0069454bc01360511f6e716db99589620b41bab6df39bc5f5f283cbc3`
5. `reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_final_closure_004/final_runtime_readback.json`: `42f817da961b610c4aa0549b69e651ebe7eea98f927f7ac358dc5098962d5155`
6. `reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_final_closure_004/installed_ui_fresh_save.jpg`: `1cf3c101c46ceb0ff55c6a3ebbef531b4ccaacaa7dd91e9ca2265d2d7fbad8b8`

**Semantic cross-check:** CHAT independently tested 13 invariants, all 13 PASS: source/artifact SHA binding, index preservation, exactly one new Vault entry, valid new record, saved after attempt and UI launch, stable UI PID and path, same package SHA, native rename sequence to `index.json`, consumed Dispatch 004 record, Canary 009 zero recorded per-user claims, APP-B paused, no protected actions, Worker stopped/paused safely. Parsed and viewed the immutable screenshot, observing new fresh `LOCAL_SAVED` row. The image, receipts and timestamps are consistent; image alone is not substitute for genuine host execution proof.

**Open reviewer work:** CHAT did NOT validate every evidence file's SHA-256 (6 critical of 27 verified), independently execute installed Windows Worker/GUI, independently read current installed ledger, or cryptographically attest the installed package. The 399 Python, 30 Desktop and 252 installed payload hash checks were retained claims of the implementing Codex evidence, not re-executed by CHAT. WORK must independently assess their applicability, evidence completeness and final audit acceptance.

## 3. Required one-pass independent audit (WORK, subject to real admission)

**Role:** WORK — independent pre-Canary release-readiness auditor (not implementing code).
**Suggested model/thinking:** GPT-6 Astra / Medium when eligible; High only if material trust/integrity complexity warrants and actual quota allows.
**R0:** Reuse Dispatch 004 and prior approved evidence, never replay 001–004.
**R1:** Audit / certification readiness, NOT implementation, no Canary claim.
**R2:** Verify actual effective RC1 Registry, WP-only scope, release permission and required gate; audit is not an authority grant.
**R3:** Verify WORK access to live Git, raw evidence including JPG/package as appropriate, actual independent reviewer identity/capacity/quota. UNKNOWN until the WORK host checks it.
**R4:** CHAT performed evidence intake; CODEX implemented and cannot self-certify; COPILOT has no verified independent audit admission (historical auth failure). WORK is the normative required independent reviewer for this gate.
**R5:** Read-only Git by default; no competing writer, worktree or branch mutation. If evidence publication required, verify destination/ownership and use separate approved location.
**R6:** Verify immutable Git hashes, test carry-forward integrity, 252 installed payload claims, host UI/Vault freshness and atomic index, secret/changed-path checks, no-replay ledger, Canary 009 untouched, APP-B paused. Distinguish observed from merely claimed evidence. Deliver auditable PASS/FAIL/BLOCKED receipt with exact source lock and reason.
**R7:** If reviewer/tool/quota/independence or material evidence cannot be confirmed, label `BLOCKED/UNKNOWN`, do not fabricate PASS or issue `PRECANARY_READY`.

**Acceptance focus:**
- Source Registry and ten EFFECTIVE family manifestations within **WP-only** scope
- Dispatch 004 single consumption and source/PreExec integrity
- 38 technical PASS gates and non-gating icon disposition
- 399/30 carried-forward regression evidence; code/package unchanged
- Fresh actual WPF UI save, matching SHA-256, index-before/after and atomic rename, state LOCAL_SAVED not Git-synced or released
- Installed package SHA `a0516aed3d69564c657dc557b7b09cfaab549d6ab04ce4132e9399b50ce5b4ac` and 252 claimed installed payload checks
- Secret/allowlist/diff quality proof
- Canary 009 current head/ledger and no-replay; APP-B pause
- Evidence contradictions and material remaining defects, if any

**Required output:** One consolidated audit verdict `PRECANARY_INDEPENDENT_AUDIT=PASS|FAIL|BLOCKED`, scope/source/commits/digests, actual verified evidence, limitations, required actions, audit signature/identity recorded by authorized mechanism, Git/remote readback where permitted. Do not present a WORK audit as already executed until it truly runs.

## 4. Gate and next step

**Now:** `WORK_INDEPENDENT_AUDIT=PENDING`, `FOX2_BRIDGE_RC1_PRECANARY_READY=NOT_GRANTED`.

Only after externally executed WORK audit PASS can CHAT independently verify the audit receipt and, if all other gates and source integrity remain PASS, issue a scoped pre-Canary READY decision. Canary 009 must still be checked for no prior claim and freshly preflighted under its existing immutable Dispatch, then executed **exactly once** by the eligible authorized executor. Afterwards verify restart/no-replay and issue `INTERNAL_FOX2_BRIDGE_READY` only after final CHAT intake.

**Prohibited:** Do not run or replay Canary now. Do not create Canary 010, resume APP-B, modify in-flight bindings, promote new Governance EFFECTIVE, merge/main, provider/broker, or LIVE.
