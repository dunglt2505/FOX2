# FOX2 — Presentation Lock Certifier R3 PreExec v3 Fetch Recovery

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3`

## Observed Owner-host failure

R3 PreExec v3 publication:
`c06a8ab9d1ca84a1bef41da354de5c3ea876a620`

The launcher successfully verified:
- PowerShell 7;
- dedicated R3 worktree;
- exact branch/publication;
- accepted source ancestry;
- zero `agent_bridge` product drift;
- immutable task/prompt/v3 hashes;
- historical v2 receipt hash;
- selected route remains CODEX / `gpt-6.1-sol` / `medium`;
- v3 PowerShell parse PASS.

The exact v3 PreExec then stopped fail-closed during its read-only source refresh with:

`FETCH_FAILED: work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019`

## Remote reconciliation

CHAT independently remote-read current Git state after the failure:

- R3 branch head remains exactly:
  `c06a8ab9d1ca84a1bef41da354de5c3ea876a620`
- governance branch still exists and resolves to:
  `d34da1e3b4918a902646621b487ca8ad3e05b0e0`
- Dispatch control branch remains:
  `533712e930a5cf937fa9401add0a89baa4994615`
- R3 v3 receipt: ABSENT
- executable R3 Dispatch: ABSENT
- Agent execution: NOT_STARTED
- code edit: FALSE
- package/host lifecycle mutation: FALSE
- G3/G4/Canary: HOLD

Therefore no executable attempt or host mutation was consumed.

## FIRST_FAILURE

**Read-only Git fetch plumbing failed while refreshing the governance branch into its remote-tracking ref.**

This does not prove governance/source invalidity. The same governance branch remains remotely readable by CHAT.

## Bounded recovery

Do not create a new coding task or change the selected route.

Do not run v3 again blindly.

Publish PreExec v4 under the same immutable R3 task/prompt with these corrections:

1. keep CODEX / `gpt-6.1-sol` / `medium`;
2. preserve v1 BLOCKED and v2 schema-invalid and v3 fetch-failed history;
3. for status/control/governance reads, use branch-local `FETCH_HEAD` discovery rather than updating `refs/remotes/origin/<branch>`;
4. bounded retry is permitted only for read-only network fetch, with no product/host mutation;
5. verify exact current governance blobs from the fetched governance head;
6. verify required status/recovery commits are ancestors of the fetched status head;
7. verify fresh Dispatch absence against the fetched control head;
8. recheck current test Python, one-writer, CODEX auth/capacity and push permission;
9. generate the receipt with schema-supported `candidate_route.model_policy="PINNED"`;
10. validate the complete receipt against current `FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json` with the discovered existing Python/jsonschema **before Git add/commit/push**;
11. install/upgrade nothing.

## Verdict

`RECOVERED / PREEXEC_V3_READ_ONLY_FETCH_FAILED / NO_SIDE_EFFECT`

Historical v1/v2/v3 remain factual.

Next safe action:
`RUN_FRESH_R3_PREEXEC_V4_ONLY`.
