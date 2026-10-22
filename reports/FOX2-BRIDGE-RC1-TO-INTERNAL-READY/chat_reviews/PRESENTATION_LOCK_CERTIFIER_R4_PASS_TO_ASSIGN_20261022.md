# FOX2 — CHAT Preflight Intake — Presentation Lock Certifier Rework R4 PASS_TO_ASSIGN

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Whole feature stage: `TEST / IN_PROGRESS`
Residual task stage: `BUILD correction inside TEST`
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4`

## Verdict

**PASS_TO_ASSIGN — R4 CERTIFIER CORRECTION ONLY**

CHAT may publish exactly one fresh executable Dispatch:

`FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001`

This is a fresh attempt after R3 A01 `CONSUMED_NO_RESULT / NO_REPLAY`; it is not a replay or rebind.

This verdict does not certify the coding result and does not authorize A05 host lifecycle, G3, G4, Canary, main, PR, merge, provider, broker or LIVE.

## Route assessment

FOX2 Skills v0.3.7 task-level assessment remains:

- `COMPLEXITY=MEDIUM`
- ambiguity: `LOW_MEDIUM`
- `EXECUTION_RISK=MEDIUM`
- `SAFETY_OVERRIDE=NO`
- Actor: `CODEX`
- Model: `gpt-6.1-sol`
- Thinking: `medium`
- Permission profile: `FULL_ACCESS`, bounded by exact task paths

PreExec verifies this selected route; it does not classify complexity or upgrade Thinking.

## Immutable R4 task and prompt

Task:
- commit: `6b6cc697ca35b35ade1ccdf363782a1f912a8936`
- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r4/task.md`
- blob: `90e6c18192cb594f408c9fd99b23da772e37c87f`
- SHA-256: `54c2075c0cce6faa90c4f23292ebe43f90e28c356089f4cbbe1e245b9a257456`

Prompt:
- commit: `2df8bd66f325a7a5eaee854e59f24db1ccfabf46`
- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r4/prompt.md`
- blob: `16d40d6c22175dedd944c75e4fb8844f41ac489c`
- SHA-256: `bc10a5f348fbe8a5348db9159f93820841b8044bd5e4eb644093b892ea79b253`

Accepted Bridge product source remains:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

R4 starts from that source and has no product/test drift before Agent coding.

## R4 PreExec acceptance

PreExec publication:
`b9e1255b0e728b33c6e400465255214738fb2a6e`

Remote receipt commit:
`35aa18ccabcc6f7d4b889ed213c075fc314d45d0`

Receipt:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/presentation_lock_certifier_rework_r4.json`
- blob: `13163c5a14812b71253e094d7dc8341bc0bbacf8`
- SHA-256: `e183bfef170fc98d826fbe48fe4eb8cef58648d4b979b211c6ab02546e8aa6b8`

CHAT independent intake:
- publication → receipt: exactly one commit ahead;
- changed path: receipt only;
- Receipt Schema v1 blob: `25fe465f82a16edf29ebf773a220969192f546e8`;
- schema validation: PASS / 0 errors;
- receipt status: PASS;
- blockers: none;
- route: `CODEX / PINNED / gpt-6.1-sol / medium / FULL_ACCESS`;
- Python: 3.13;
- pytest: 8.3.5;
- jsonschema: 4.26.0;
- CODEX CLI: 0.162.1;
- current Medium capacity probe: PASS;
- one-writer: PASS;
- Git push permission: PASS;
- fresh R4 Dispatch absent at intake;
- Agent execution started: false;
- product/test drift before coding: none;
- package/Bridge host mutation: none.

## Recovery binding

R3 A01 final recovery:
`3c32743e9b9cdcb7eb799094ee7bdefdaeb9aa71`

Consumed Dispatch:
`FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-CODEX-001`

Final verdict:
`CONSUMED_NO_RESULT / NO_REPLAY`

The R3 Dispatch must never be replayed or rebound.

R4 is a fresh attempt identity.

## Reused PASS

No blanket recheck was performed.

Still reusable:
- accepted Bridge BUILD source;
- A04 package/provenance/install/safe-state/singleton PASS;
- reuse-first Master Plan;
- A04/A05 composite evidence plan;
- R3 route rationale;
- governance/source bytes that remain unchanged.

R4 PreExec rechecked only the mandatory new-attempt and time-dependent gates.

## Allowed code/test scope

Exactly:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Allowed result/evidence:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r4/**`

No third product/test file.
No WPF C# source.

## Required Agent validation

- focused lifecycle WPF contract tests;
- full `agent_bridge/tests`;
- `git diff --check`;
- exact changed-path allowlist;
- secret/privacy scan;
- K1 hunk classification with `UNEXPLAINED=0`;
- result report + evidence manifest + bounded R4 evidence;
- observed remote result SHA returned outside committed report.

## Explicitly forbidden

R4 MUST NOT:
- replay R3 A01;
- rebuild the A04 package;
- install/update/uninstall/reinstall Bridge;
- run the real Host Lifecycle;
- touch Worker/F1;
- open A05 execution;
- enable G3/G4/Canary;
- create PR or merge;
- touch main;
- provider/broker/LIVE.

## Assignment decision

CHAT may publish exactly one fresh R4 CODEX Dispatch with:

- actor: `CODEX`;
- model: `gpt-6.1-sol`;
- reasoning: `medium`;
- permission profile: `FULL_ACCESS` bounded to the task;
- execution: `MANUAL_LOCAL`;
- runtime base: `35aa18ccabcc6f7d4b889ed213c075fc314d45d0`;
- accepted source: `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- max_runs: `1`;
- retry lineage: consumed R3 Dispatch;
- code push only for exact two code/test paths;
- report/evidence push only for R4 result paths;
- no replay after consumption.

Agent completion is at most `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

A05/G3/G4/Canary remain locked.
