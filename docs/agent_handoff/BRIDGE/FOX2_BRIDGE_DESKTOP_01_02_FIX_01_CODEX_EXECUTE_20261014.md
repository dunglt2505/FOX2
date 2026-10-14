# FOX2 — CODEX EXECUTION HANDOFF — BRIDGE-DESKTOP-01-02-FIX-01

**Date:** 2026-10-14  
**Corrective WP:** `BRIDGE-DESKTOP-01-02-FIX-01`  
**Status:** `PREPARED / DEV_SCOPE_AUTHORIZED / EXECUTION_DEFERRED_UNTIL_OWNER_TOKEN_READY`  
**Stop boundary:** `PUSHED_UNREVIEWED`

## 0. Role · Engine · Thinking · Scope

- **Role:** CODEX corrective implementation Agent through FOX2 Bridge
- **Engine/Model:** GPT-6.1 Sol if available; exact dispatch model fields govern at execution
- **Thinking:** High
- **Scope:** corrective patch only; no architecture expansion
- **Execution timing:** DO NOT execute until Owner explicitly confirms Codex token/quota is available

## 1. Exact base and source

Repository:
`dunglt2505/FOX2`

Parent rejected delivery:
`3497356d5fc74785ab3377c1a49ea5330c0dab13`

Corrective task branch:
`work/FOX2-BRIDGE-DESKTOP-01-02-FIX-01-codex`

Normative FIX-01 lock:
- commit: `2e3dbcad475805da7a80a57ac57e11441f6a36b2`
- path: `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_FIX_01_SOURCE_LOCK_20261014.md`

Read that file completely before editing.

Parent combined source lock remains immutable:
- commit `1ca353efc2ffc2f6d7eaacccac11d48897ba09ac`
- blob `6683781beb03a9c7deea9260c2d6553798e298ad`

## 2. Exact write scope

Allowed:
- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-01-02/**`

Forbidden:
- `docs/**` including this handoff/lock/prompt;
- application backend/frontend;
- BRD/Technical source;
- governance;
- `.github/**`;
- provider/broker/LIVE;
- unrelated reports.

## 3. Required corrective implementation

### A. Recovery semantics

Fix the runner so an Agent that has already launched and then exits non-zero is not automatically classified as a clean terminal `FAILED`.

For the quota-stop / post-launch non-zero case:
- preserve consumed identity;
- classify conservatively as `NEEDS_RECONCILIATION`;
- do not auto replay;
- do not substitute another Agent;
- retain enough checkpoint/result evidence for later reconciliation.

Preserve terminal/actionable behavior for proven pre-spawn failures.

Add deterministic tests that specifically prove this distinction.

### B. Diff hygiene

Fix all current `git diff --check` failures in authorized paths.

Known defects include:
- extra blank line at EOF in `agent_bridge/README.md`;
- trailing whitespace/CR artifact in `reports/BRIDGE-DESKTOP-01-02/evidence/pytest.txt`.

Do not hide failures by weakening validation.

### C. Evidence completion

Run full tests and then run the delivery validator successfully so it creates:

- `reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json`
- `reports/BRIDGE-DESKTOP-01-02/evidence/verification.json`

If the validator currently hardcodes assumptions that are valid only before recovery publication, update it minimally so it validates the FIX-01 lineage correctly without weakening:
- source lock identity;
- allowlist;
- diff check;
- test evidence;
- secret scan;
- report/evidence requirements.

### D. Report consistency

Update `reports/BRIDGE-DESKTOP-01-02/report.md` to describe the actual history:
- parent implementation recovery-published at `3497356d5fc74785ab3377c1a49ea5330c0dab13`;
- FIX-01 corrects CHAT review findings;
- tests/validator/diff-check exact outcomes;
- real Windows/manual/paid canaries remain NOT_RUN where applicable;
- Desktop-03 and later generic/community scope remain NOT_RUN/out-of-scope.

Do not fabricate the final remote FIX-01 SHA before Bridge publishes it.

## 4. Mandatory tests / gates

Run:

```powershell
$env:PYTHONPATH = Join-Path $PWD 'agent_bridge/src'
python -m pytest agent_bridge/tests -q -p no:cacheprovider --junitxml reports/BRIDGE-DESKTOP-01-02/evidence/pytest.xml
python agent_bridge/scripts/validate_desktop_delivery.py
git diff --check
```

Also ensure:
- regression test for post-launch non-zero -> NEEDS_RECONCILIATION;
- replay remains blocked for same dispatch;
- no Agent substitution;
- pre-spawn failure behavior remains correct;
- required evidence JSON files parse;
- no out-of-scope changes;
- secret scan PASS.

## 5. Git ownership

CODEX edits/tests only.

CODEX MUST NOT:
- git add;
- git commit;
- git push;
- create PR;
- merge;
- touch main.

Bridge owns commit/push after successful Agent exit and verification.

## 6. Result contract

Required final files:
- `reports/BRIDGE-DESKTOP-01-02/report.md`
- `reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json`
- `reports/BRIDGE-DESKTOP-01-02/evidence/verification.json`
- `reports/BRIDGE-DESKTOP-01-02/evidence/pytest.xml`

Required final marker:

`FOX2_BRIDGE_DESKTOP_01_02_FIX_01_DELIVERY_READY`

Stop at:
`PUSHED_UNREVIEWED`

No PR/merge/main/deploy/provider/broker/LIVE.
