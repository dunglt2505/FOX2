# FOX2 — R5 PASS_TO_ASSIGN

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5`

## Verdict

`PASS_TO_ASSIGN` for exactly one fresh R5 CODEX attempt.

Route: `CODEX / gpt-6.1-sol / medium / FULL_ACCESS`.
Task assessment: `COMPLEXITY=EASY`, `EXECUTION_RISK=MEDIUM`, `SAFETY_OVERRIDE=NO`.

Accepted product lineage remains `085cc8302e824dbccf9cbef80422ed48894b9cb4`.
R5 salvage base is unaccepted R4 result `d997756b5f4cfaa7e442dfc5d929093782b7a90f`.
R4 CHAT_REWORK: `07ce66987345859f978c06fbb4abbdeeaa0ff04c`.
R4 Dispatch is consumed/no-replay.

R5 task:
- commit `8fb7d23217067474488203aceef094b838e828ab`
- blob `cbc546dcad97c9dcab02d6e82b68eef163d2b17d`
- SHA-256 `d7054edbb574661df9cbba08dcdf282cf175d2cd5496a5dc7b2c2af6cdaa7062`

R5 prompt:
- commit `b33d0610649cbfb466bb5febd1e295f91f35e53d`
- blob `10b95e130289752701c790beb41b2d0cde9af017`
- SHA-256 `ffeaccd6a60eb4b56da907bf1092bb3889b38a80a8cd957ca5d8a90860e79fba`

PreExec publication: `7d18412b0ac1226cd0d93a42c06e372077519a7f`.
PreExec receipt commit: `59ba8b50136ac5bcee7cf2d2edbf65e360812b78`.
Receipt blob: `ffe3e6f1fd06daae83df0cd854c27613ed943352`.
Receipt SHA-256: `4426c651dd4e0719f96061491450143317b1e04012e2016b249cc74137d33b04`.
Receipt Schema v1 validation: PASS, zero errors.
Publication→receipt: one commit, receipt file only.
Agent execution started: false.
Fresh R5 Dispatch at intake: absent.
Host lifecycle mutation: false.

Allowed code/test paths:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Allowed result paths:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r5/**`

Required correction: fail closed for pre-live ABSENT + live errno13/no-winerror in fresh and zero-WPF continuation; preserve winerror32 and valid existing-live continuation differential proof.

Runtime base for fresh R5 Dispatch: `59ba8b50136ac5bcee7cf2d2edbf65e360812b78`.
Max runs: 1.

A05/G3/G4/Canary/main/merge/provider/broker/LIVE remain unauthorized.
