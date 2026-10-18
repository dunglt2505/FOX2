# FOX2 — Bridge-first priority decision & CHAT intake (2026-10-18)

**Status:** `OWNER_PRIORITY_BRIDGE_FIRST / CHAT_RESULT_INTAKE_COMPLETED / PRECANARY_INDEPENDENT_AUDIT_PENDING`
**Project:** FOX2 only
**Owner decision:** Complete Bridge RC1 before promoting new project-wide Governance to EFFECTIVE.
**Document scope:** Non-main documentary roadmap and CHAT evidence intake; NOT an EFFECTIVE Policy, change to Bridge immutable source lock, DEV grant, audit certificate, Canary authorization, or LIVE release.
**Publication branch:** `work/FOX2-GOVERNANCE-OWNER-RELEASE-20261018`
**Reviewed Bridge result commit:** `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`
**Bound Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`

## 1. Verified source and task state (R0/R1)

- Live Git observed HEAD on `work/FOX2-BRIDGE-DESKTOP-BATCH-B`: `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`, not drifted at intake.
- Historical executable Dispatch 004: `FOX2-DISPATCH-BRIDGE-RC1-CODEX-004`, control commit `dc79f8143eec471508bf37565bff38442ce0548a`, max_runs=1, manually consumed. DO NOT REPLAY 001–004 or create new repair Dispatch without new evidence of a real technical failure.
- The installed source binding for this Whole-WP is WP-only Registry `b27f1085ee13d8dce56fd2735e100ea1616e6e23` at `docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json` -> Owner approval/manifests `d8e2331674ef1921844f369bfa9e48b82a73c6a1` -> immutable RC1 source `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`.
- Bridge final report: `reports/BRIDGE-DESKTOP-BATCH-B/report.md`; manifest: `reports/BRIDGE-DESKTOP-BATCH-B/evidence_manifest.json`; gate matrix: `reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_final_closure_004/acceptance_gates.json`.
- Gate matrix contains 40 entries: 38 `PASS`; `PRECANARY_INDEPENDENT_AUDIT=PENDING`; `ICON_DISPOSITION=ICON_NON_GATING_NO_AUTHORIZED_ASSET`. Therefore technical PASS does not imply pre-Canary release approval.
- Installed technical certification is reported PASS based on unchanged 252 installed payload file hashes and a fresh installed WPF UI Artifact Vault proof (27 passed readback checks). Prior unchanged product evidence includes 399 Python tests PASS and 30 desktop checks PASS. Those prior suites were not rerun in Dispatch 004.
- No code/package changes by Dispatch 004; package SHA-256 `a0516aed3d69564c657dc557b7b09cfaab549d6ab04ce4132e9399b50ce5b4ac`; data and result path changes remain under `reports/BRIDGE-DESKTOP-BATCH-B/**`.
- CHAT verified the Git result, named status, and acceptance evidence. **This is CHAT intake for audit handoff, not an independently certified audit or installed-host re-execution.**
- Current status is `IMPLEMENTATION_PUSHED_UNREVIEWED` in the historical Agent manifest; CHAT intake now records review of the published Git evidence, without mutating the Agent's immutable result or turning a pending audit into PASS.

## 2. Correct execution priority — no new Whole-WP

1. **Now — CHAT intake:** accept the Dispatch-004 report as technically complete *for the purpose of requesting independent pre-Canary readiness audit*; preserve all raw evidence and remote SHA. Do not run a new implementation cycle.
2. **Next — independent pre-Canary audit:** eligible independent reviewer assesses the exact frozen source/trust-chain, package/payload, fresh installed-UI proof, test carry-forward materiality, integrity, no replay, permissions, allowed paths, outstanding acceptance requirements and Canary readiness. Record independently verifiable PASS/FAIL and evidence. Do not default to WORK for unrelated routine document review; this task is an explicit independent audit gate in the bound Bridge task.
3. **Only after audit PASS — CHAT:** verify and publish `FOX2_BRIDGE_RC1_PRECANARY_READY` under an authorized source-bound receipt; verify Canary 009 remains unconsumed and PreExec/worktree/agent quota/ownership before execution. Avoid reusing stale preflight evidence when material host state changed.
4. **Only after true pre-Canary READY — execution agent:** immutable Canary `FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001` at `work/FOX2-BRIDGE-FINAL-CANARY-009` source `501822a33ef08c7365154913bbc677544856eee5`, exactly once. No claim, edit, replacement or replay before authority and gates.
5. **After Canary — CHAT final intake:** validate real once-only execution, usage, restart/no-replay, installation correctness, remote readback and final acceptance; only then issue `INTERNAL_FOX2_BRIDGE_READY`.
6. **After Bridge ready:** resume APP-B only under its own gating; separately certify Governance project-wide Registry and Dictionary v1.3/Policy v1.9.0/Routing v1.4.0/Protocols. Use prior 10/10 Git–Library parity and 47/47 isolated candidate checks without unnecessary rework. Do not auto-rebind any in-flight Bridge/Canary/APP source.

## 3. Governance state and protected branches

- Governance candidate publication branch HEAD at intake: `e0e0d76fdc572a0e63bbe94a02925936df004cf4`.
- New Governance versions are documented and in pre-promotion; project-wide EFFECTIVE is **HOLD**, not a dependency for the already source-bound Bridge Whole-WP.
- `work/FOX2-BRIDGE-FINAL-CANARY-009` was observed unchanged at `501822a33ef08c7365154913bbc677544856eee5`. Git HEAD stability is not proof of installed-ledger consumption state; use the actual ledger before a future claim.
- `work/FOX2-M1-A-APP-BATCH-B` was observed unchanged at `fc8aba202e15bddfcc5156b2c1bb36ed222329eb`; APP-B stays PAUSED.
- No main/merge/DEV/LIVE, provider/broker, release or production permission is granted by this roadmap intake.

## 4. Routing precheck R0–R7 and next handoff

| Check | Evidence-backed decision |
|---|---|
| POLICY_CHECK | Current WP-only source Registry + Owner approval inspected; new Governance remains CANDIDATE. |
| R0 | Dispatch-004 and 38 technical gate PASS results already recorded; do not replay. |
| R1 | Current phase = **independent pre-Canary audit**, not implementation or installer repair. |
| R2 | Source registry and Owner WP trust binding present; `PRECANARY_INDEPENDENT_AUDIT=PENDING`. No Canary/LIVE grant. |
| R3 | CHAT Git/Library access is verified. New independent reviewer host access, quota and permissions = UNKNOWN; do not claim execution admitted. |
| R4 | CHAT performs evidence review and routing. WORK is a candidate for required independent audit; COPILOT/CODEX only if a new authorized material technical action is required, not by default. |
| R5 | Git release documentation branch owned by CHAT; audited Bridge worktree and new reviewer single-writer state must be checked on host (UNKNOWN here). |
| R6 | The result report, manifest, gate matrix, immutable trust binding and no-replay evidence are identified for audit. Remote readback of this planning record must occur after publication. |
| R7 | Immediate route = CHAT publish this non-main roadmap/intake decision; next **audit candidate** = WORK GPT-6 Astra Medium (High only if audit complexity warrants), pending real access/quota/independence and separate valid preflight. Do not dispatch or claim audit was performed. |

**STOP:** Do not certify independent audit yourself; do not claim `PRECANARY_READY`, run Canary 009, resume APP-B or promote Governance project-wide EFFECTIVE without their respective documented gates.

## 5. One next milestone

**Next material work is exactly one independent pre-Canary acceptance audit on the existing whole-WP evidence, not new implementation work.** Return audit PASS/FAIL and immutable evidence to CHAT; CHAT then decides Canary admission. Governance candidate promotion remains deferred until Bridge internal-ready and its own authority/compatibility gates.
