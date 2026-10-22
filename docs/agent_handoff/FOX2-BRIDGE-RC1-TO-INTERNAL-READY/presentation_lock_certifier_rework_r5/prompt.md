FOX2 — CODEX EXECUTION PROMPT — PRESENTATION LOCK CERTIFIER REWORK R5

Role: CODEX — bounded BUILD correction executor inside Bridge TEST
Model: gpt-6.1-sol
Thinking: medium
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022
Permission profile: FULL_ACCESS bounded to exact task
Max runs: 1
No model/effort substitution
No replay of R4 or earlier consumed Dispatches

TASK_ROUTE_ASSESSMENT
- COMPLEXITY=EASY
- ambiguity=LOW
- EXECUTION_RISK=MEDIUM
- SAFETY_OVERRIDE=NO
- dependency impact=MEDIUM
- evidence quality=HIGH
- ROUTE_RATIONALE=single known boolean-proof defect plus explicit missing negative fixtures; fail-closed certification semantics justify Medium reasoning.

IMMUTABLE TASK
Task ID: FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5
Task path:
docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r5/task.md
Task commit:
8fb7d23217067474488203aceef094b838e828ab
Task blob:
cbc546dcad97c9dcab02d6e82b68eef163d2b17d
Task SHA-256:
d7054edbb574661df9cbba08dcdf282cf175d2cd5496a5dc7b2c2af6cdaa7062

SOURCE / SALVAGE BINDING

Accepted product lineage remains:
085cc8302e824dbccf9cbef80422ed48894b9cb4

R5 execution salvage base:
d997756b5f4cfaa7e442dfc5d929093782b7a90f

That R4 result is NOT accepted product source.
CHAT review:
07ce66987345859f978c06fbb4abbdeeaa0ff04c
verdict:
CHAT_REWORK

R5 starting blobs:
- agent_bridge/scripts/certify_user_lifecycle.py
  cc469b9e29301db488605d621c8cbb37d9c442e0
- agent_bridge/tests/test_lifecycle_wpf_contract.py
  e2d6551ca119e72a8cb59f38f50bded09a276731

R4 Dispatch is consumed/no-replay:
FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001

OBJECTIVE

Fix only the R4 errno13 differential-proof semantic gap.

Current defect:
a live errno13/no-winerror can be accepted when a pre_live record merely exists, including pre_live classification ABSENT.

Required behavior:
1. SHARING_VIOLATION / winerror32 remains accepted.
2. Fresh or zero-WPF launch path:
   errno13/no-winerror is accepted only if pre_live classification is exactly OPENABLE.
3. pre_live ABSENT + live errno13/no-winerror fails closed.
4. Existing-live continuation:
   errno13 may remain provisional and is finalized only after graceful exit, zero WPF and same-lock post-exit OPENABLE.
5. Preserve same-file device/inode proof, lock bytes, bounded error evidence and lifecycle tail.

ALLOWED PRODUCT/TEST PATHS — EXACTLY TWO
- agent_bridge/scripts/certify_user_lifecycle.py
- agent_bridge/tests/test_lifecycle_wpf_contract.py

RESULT PATHS
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r5/**

REQUIRED TESTS

Add/retain:
- fresh + pre-live ABSENT + live winerror32 => PASS;
- fresh + pre-live ABSENT + live errno13/no-winerror => FAIL;
- continuation zero-WPF + pre-live ABSENT + live errno13/no-winerror => FAIL;
- pre-live OPENABLE + errno13 fresh/zero-WPF => PASS;
- existing-live continuation errno13 + post-exit OPENABLE => PASS;
- existing-live continuation errno13 + post-exit denied => FAIL;
- unrelated OSError and winerror5 => FAIL;
- lock bytes unchanged;
- no Worker/F1/tray fallback.

Run:
python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py
python -m pytest -q agent_bridge/tests
git diff --check

Also prove exact changed-path allowlist, privacy/secret scan, K1 UNEXPLAINED=0 and Result Contract v2 schema/hash checks.

PROVENANCE

R5 report/source binding MUST explicitly name the actual fresh R5 Dispatch and R5 PreExec receipt.
Do not state that execution relied only on a user prompt.

REUSE

Do not repeat package build/install or real Host Lifecycle.
Reuse unaffected A04 and R4 evidence, but rerun focused/full suites because code/test bytes change.

STOP

STOP if:
- R5 task/prompt/Dispatch binding differs;
- route differs from CODEX / gpt-6.1-sol / medium;
- salvage base differs from d997756b5f4cfaa7e442dfc5d929093782b7a90f;
- third product/test file required;
- WPF product change or package/host mutation required;
- tool installation/elevation required;
- A05/G3/G4/Canary/main/merge/provider/broker/LIVE would be touched.

Return observed remote result SHA outside committed report.
Result remains PUSHED_UNREVIEWED until CHAT result review.
