# FOX2 — R3 CODEX A01 Consumed Attempt Recovery

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-CODEX-001`

## Immutable execution identity

- runtime base: `7fcdfd19e0d9177b4d85e39fd249b5e65ccc0d49`
- Dispatch commit: `097c57a779d1fca58d08aed80e2af4a0646b7ea8`
- Dispatch blob: `9cfba0acd7e6e1cbc5d74d7539ef9d414e940cac`
- Dispatch SHA-256: `df288de7b09d3ba0d8996615513c059a2a8780f96550090ba2648ba9cdea08c3`
- PASS_TO_ASSIGN: `7efa989c070da15d2000ca105b04632f092701a5`
- valid PreExec v4 receipt: `7fcdfd19e0d9177b4d85e39fd249b5e65ccc0d49`
- route: `CODEX / gpt-6.1-sol / medium / FULL_ACCESS bounded`
- max_runs: `1`

## Observed Owner-host terminal block

The owner launcher printed:

- `FOX2_DISPATCH_CONSUMED=TRUE`
- `FOX2_NO_REPLAY=TRUE`
- entered `=== FOX2 R3 POST-CONSUME FAILURE ===`

The catch/reporting block then failed while trying to call:

`Safe $_.Exception.Message`

with:

`The term 'Safe' is not recognized...`

This is a launcher post-consume reporting defect. It does not prove whether CODEX produced local edits/commits before the reporting failure.

## Independent remote reconciliation

CHAT remote-read the authorized R3 branch after the failure.

Observed remote head:

`7fcdfd19e0d9177b4d85e39fd249b5e65ccc0d49`

Compared with runtime base:

- status: `IDENTICAL`
- ahead: `0`
- behind: `0`
- changed paths: `0`

Therefore there is **no remote R3 result commit**.

The existing `report.md` and `evidence_manifest.json` at that head predate this attempt and are not evidence of a new R3 result.

## Verdict

`NEEDS_RECONCILIATION / DISPATCH_CONSUMED / NO_REMOTE_RESULT`

The Dispatch is permanently consumed and MUST NOT be replayed.

Current local result state:
`UNKNOWN`

Possible states still to distinguish:
1. CODEX made no changes;
2. CODEX left valid uncommitted R3 code/result bytes;
3. CODEX created one or more local commits but push failed;
4. CODEX/result delivery partially failed;
5. a task-scoped CODEX writer is still live.

## Reusable PASS

Preserve without rerun:
- A04 package/provenance/install-update/safe-state/singleton PASS evidence;
- R3 task/prompt bindings;
- R3 PreExec v4 PASS;
- R3 route assessment and Medium capability PASS;
- R3 Dispatch publication/readback/schema PASS.

Do not repeat package build/install or historical A04 PASS gates.

## One discriminating host probe

Next safe action is one **read-only local reconciliation probe** that inspects:

- durable attempt claim;
- current task-scoped CODEX processes;
- local R3 HEAD and ancestry;
- local commits ahead of runtime base;
- staged/unstaged/untracked paths;
- local diff path allowlist;
- most recent `FOX2-R3-CODEX-LAST-*.txt` if present;
- whether report/manifest/evidence were produced locally.

The probe MUST NOT:
- invoke CODEX;
- reset/clean/checkout;
- commit/push;
- modify files;
- replay the Dispatch;
- package/build/install/host-mutate;
- enable A05/G3/G4/Canary.

## Recovery rule after probe

- If a clean, allowed local descendant/result exists: validate and push the **existing bytes only** under recovery; no Agent replay.
- If allowed uncommitted bytes exist: inspect and preserve them; do not discard. CHAT decides whether bounded publication of existing bytes is safe.
- If no result bytes exist and no writer remains: classify `CONSUMED_NO_RESULT`; any further coding requires a **fresh new Dispatch/task attempt**, never replay of this one.
- If writer remains active or state conflicts: `NO_REPLAY_STOP` until reconciled.
