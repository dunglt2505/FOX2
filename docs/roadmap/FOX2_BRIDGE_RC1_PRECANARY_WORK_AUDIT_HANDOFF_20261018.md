# FOX2 — Bridge RC1 Pre-Canary Independent Audit: CHAT Evidence Intake and WORK Handoff

> **CURRENT CHAT STATUS — Owner instruction (2026-10-18):** The latest factual status is
> [FOX2_BRIDGE_RC1_CHAT_CONSOLIDATED_STATUS_20261018.md](FOX2_BRIDGE_RC1_CHAT_CONSOLIDATED_STATUS_20261018.md)
> (published with verified Git readback). Owner controls reviewer appointment and has stopped repeated administrative admission/host-certificate investigations. This does **not** certify independent audit PASS. B2=CLOSED_PASS; PRECANARY_INDEPENDENT_AUDIT=BLOCKED; Canary009/APP-B=HOLD.
> Historical status lines and previous handoff recovery recommendations below remain provenance, not new instructions to repeat the blocked admission loop.
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

---

## 6. CHAT intake of subsequently published bounded reviewer result — 2026-10-18

**Status:** `PRECANARY_INDEPENDENT_AUDIT=BLOCKED` (accepted as truthful blocked admission; not product failure; not release readiness).
**Reviewer Git commit:** `d48aea2e22449ee4435cd81cb89101b653e7dbc8`
**Reviewer result branch:** `work/FOX2-BRIDGE-RC1-PRECANARY-AUDIT-20261018-readonly` (HEAD exact match at intake).
**Published records (3 new paths only):**
- `reports/BRIDGE-RC1-PRECANARY-AUDIT-20261018/audit_receipt.json` — Git blob `03cd2342c97441986ed95fa11ece5ceef7dc763e`
- `reports/BRIDGE-RC1-PRECANARY-AUDIT-20261018/audit_checks.json` — Git blob `618cc3f38b08dcc6d76a493aaa96d3f7cc13d5e0`
- `reports/BRIDGE-RC1-PRECANARY-AUDIT-20261018/report.md` — Git blob `ff6841b96ce9f75803f1edf2084cc81009026284`

### Evidence accepted and inherited

- 34/34 bounded independent Git/package evidence checks PASS, not product retests.
- 26/26 Dispatch-004 declared digests and 67/67 historical digests verified, 10/10 source-family digests and 252/252 ZIP archive member hashes verified; 399 JUnit cases with 0 failures/errors/skips and previously accepted 30 Desktop PASS. All are evidence-based and not fresh installed-host tests.
- No material code or package defect found by this review. Exactly three report files added after Bridge product commit; Bridge source/Canary/APP branches unchanged at intake. No replay or protected execution performed.
- `PRECANARY_INDEPENDENT_AUDIT` remains BLOCKED; `FOX2_BRIDGE_RC1_PRECANARY_READY` NOT_GRANTED; Canary 009 and APP-B remain HOLD.

### Remaining exact blockers and limits

1. **B1 REVIEWER_ADMISSION_UNVERIFIED (blocking):** the reviewer receipt identifies `CODEX_WORK_MODE_LINUX`, role `BOUNDED_EVIDENCE_REVIEWER_NOT_ADMITTED_WORK`, not admitted independent WORK. Its Git principal, permission and read access cannot substitute for verified independent WORK reviewer identity/admission. Do not label this work WORK PASS.
2. **B2 SHARED_RESOLVER_NOT_EXECUTED (procedural):** the reviewer could not read/execute `shared/git_resolver.py` from its cloud skill mount. CHAT has since verified in the authenticated **FOX2 Skills Plugin v0.2.3** backend release `pluginrel_6ad44b76c59c8191a78e1f40300e17c6` that exact `shared/git_resolver.py` and `shared/host_guidance.md` exist and are readable via Plugin Creator `get_plugin_files`; this is a **review-host exposure/execution** gap, not absence of source in the plugin. Merely retrieving it in CHAT does not discharge the execution gate. The resolver requires Python 3.11+ and authenticated live GitHub token for actual remote reads; the caller separately validates the Owner trust policy.
3. **L1 CURRENT_HOST_NOT_REATTESTED:** Windows installed payload/pointer, manually consumed Dispatch store and current ledger were not directly accessible in the reviewer Linux session. Admitted WORK auditor must decide if one bounded read-only host evidence attestation is material; do not automatically repeat Windows reinstall, 399/30 tests or the fresh UI save.
4. Reviewer model/thinking, numeric quota and independent signature are NOT_EXPOSED; reported live analysis capacity alone is not independent admission.

### CHAT routing intake (R0–R7)

- R0: This result is new evidence, not a new implementation request; preserve Dispatch 001–004 no-replay and all historical PASS.
- R1: Phase is **WORK independent pre-Canary certification admission**, not implementation repair or Canary.
- R2: RC1 WP-only approved source authority remains pinned, but audit release gate is BLOCKED; no new DEV/merge/LIVE/Canary rights.
- R3: CHAT can verify Git & Plugin Creator source; actual independent WORK reviewer identity, access to resolver execution, Windows host and quota remain **UNKNOWN/BLOCKED** until verified in its own host.
- R4: CHAT performs this factual intake; CODEX implemented and CODEX_WORK_MODE_LINUX did not satisfy WORK independence; COPILOT is not established as independent eligible reviewer; use actual admitted WORK as normative gate owner only after fresh preflight.
- R5: This delta is confined to CHAT-owned non-main roadmap path; no Bridge, Canary, APP worktree or protected branch is modified.
- R6: New reviewer result immutable Git commit and blob refs above; this CHAT update requires its own remote byte readback.
- R7: Status `BLOCKED`; next meaningful action is one **admitted WORK** review that reuses 34/34 verified checks, runs trusted resolver, assesses any minimal host attestation, then issues truly independent PASS/FAIL/BLOCKED receipt. STOP before `PRECANARY_READY`.

**Do not create another CODEX implementation Dispatch or retry the bounded CODEX reviewer as WORK.** First secure legitimate independent reviewer admission and actual resolver access; if impossible, report the exact platform/host capability limitation to Owner for a governed decision, without relaxing the acceptance gate.

---
## 2026-10-18 — CHAT intake: final reviewer-admission determination

Input Git Result: `541bf35e3bdb95b701bd1cdc22b0bdbe87333110`; report `reports/BRIDGE-RC1-PRECANARY-AUDIT-20261018/final_admission_determination.md`. Verified single new report file, exact audit-branch commit, and unchanged Bridge/Canary/APP heads.

Disposition: `CHAT_INTAKE=PASS`; `B2_SHARED_RESOLVER=CLOSED_PASS`; `WORK_REVIEWER_ADMISSION=BLOCKED`; `PRECANARY_INDEPENDENT_AUDIT=BLOCKED`; `PRECANARY_READY=NOT_GRANTED`.

The frozen RC1 task section 11 requires an independent WORK pre-Canary review. That task does **not expressly specify** a host-issued identity certificate, cryptographic signature, or a particular model-telemetry field as the sole admissible way to evidence reviewer eligibility. More specific host-issued provenance wording was introduced by the later CHAT handoff. It must not silently replace the owning acceptance specification or be silently waived. Distinguish the substantive mandatory **independence of reviewer** from any unverified **particular attestation mechanism**.

The new report states its execution was a continuation of the earlier reviewer session and cannot establish a fresh admitted WORK role; no audit PASS is issued. Existing 34/34 evidence checks, 10/10 source families, 252/252 package hashes, 399 JUnit tests and historical 30 desktop PASS are preserved.

Next allowed decision: CHAT and the governance-owning authority should determine an actual independently evidenced reviewer admission route supported by the product/host, or approve a prospective explicit audit-admission evidence contract. Such contract must preserve independent review, read-only scoped evidence and final acceptance, not retroactively assert this review as admitted. If no eligible WORK reviewer can be established, retain BLOCKED. Do not repeat the same prompt/recovery session.

Canary 009 and APP-B remain HOLD; no replay, code change, source rebind, merge or release authority follows from this note.
