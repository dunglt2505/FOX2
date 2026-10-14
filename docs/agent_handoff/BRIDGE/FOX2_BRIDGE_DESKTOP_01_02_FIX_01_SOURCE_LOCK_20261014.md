# FOX2 — BRIDGE-DESKTOP-01+02 FIX-01 Corrective Source Lock

**Date:** 2026-10-14  
**Corrective WP:** `BRIDGE-DESKTOP-01-02-FIX-01`  
**Parent WP:** `BRIDGE-DESKTOP-01-02`  
**Status:** `FIX_SCOPE_LOCKED / OWNER_PREP_AUTHORIZED / EXECUTION_DEFERRED_UNTIL_TOKEN_AVAILABLE`

## 1. Purpose

This corrective WP repairs only the CHAT review findings on delivery commit:

`3497356d5fc74785ab3377c1a49ea5330c0dab13`

The Desktop-01+02 implementation itself is retained. This is not a redesign, refactor, or Desktop-03 expansion.

## 2. Immutable parent authority

Parent implementation authority remains:

- Combined source/design lock commit: `1ca353efc2ffc2f6d7eaacccac11d48897ba09ac`
- Source/design lock blob: `6683781beb03a9c7deea9260c2d6553798e298ad`
- BRD-09 v0.1 Candidate and Bridge Technical Spec v0.7 Candidate remain Owner-bound exactly as previously authorized.
- Replacement handoff REV2 remains historical execution authority for dispatch 002.
- Parent implementation recovery commit under review: `3497356d5fc74785ab3377c1a49ea5330c0dab13`.

No governance or BRD/Technical source change is authorized by FIX-01.

## 3. CHAT review findings to correct

FIX-01 is limited to these findings:

### F01 — non-zero Agent exit after launch is misclassified

Current runner can terminalize a dispatch as `FAILED` when an Agent process has already started and returned a non-zero exit code.

Required correction:

- once the Agent has started / RUNNING evidence exists, a non-zero Agent exit is execution-uncertain unless a narrower fail-closed case proves no workspace mutation;
- the conservative state for the quota-stop / non-zero-after-start case is `NEEDS_RECONCILIATION`;
- no automatic replay;
- consumed dispatch identity remains consumed;
- add deterministic regression coverage for an Agent that produces/modifies WIP and then exits non-zero.

Do not weaken genuine pre-spawn failures such as tool missing, auth unavailable before launch, unsupported required capability, or other proven `AgentNotStarted` cases.

### F02 — whitespace / diff-check defects

Correct all `git diff --check` failures present in the parent delivery, including:

- extra blank line at EOF in `agent_bridge/README.md`;
- trailing whitespace/CR artifact in `reports/BRIDGE-DESKTOP-01-02/evidence/pytest.txt`.

Final staged and unstaged diff checks must PASS.

### F03 — required evidence artifacts missing

The parent delivery does not contain final:

- `reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json`
- `reports/BRIDGE-DESKTOP-01-02/evidence/verification.json`

Regenerate them from a successful deterministic validator run after all code/test fixes.

### F04 — report state stale after recovery publication

Update `reports/BRIDGE-DESKTOP-01-02/report.md` so it no longer states that the delivery is uncommitted/unpublished.

It must accurately record:

- parent recovery publication SHA `3497356d5fc74785ab3377c1a49ea5330c0dab13`;
- FIX-01 corrective lineage;
- exact final test result;
- exact validator/diff-check status;
- real-world canaries that remain NOT_RUN;
- no claim of PR/merge/main/deploy/provider/broker/LIVE.

The final remote FIX-01 SHA is Bridge-owned publication evidence and may be appended/recorded by Bridge/runtime evidence after Agent exits; CODEX must not invent it.

## 4. Explicit non-goals

FIX-01 MUST NOT:

- redesign worker/tray/startup architecture;
- expand Desktop-03 packaging/setup/update/uninstall;
- add generic/community extraction;
- change BRD-09 or Tech Spec v0.7 Candidate;
- change governance;
- touch application backend/frontend/data/provider/broker/LIVE paths;
- merge or push main;
- perform real paid Agent canaries merely for this corrective patch;
- replay dispatch 001 or 002.

## 5. Exact write scope

Allowed:

- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-01-02/**`

Everything else is read-only.

CHAT-authored FIX-01 lock/handoff/prompt files are immutable source and are not Agent write targets.

## 6. Required tests

At minimum:

1. existing full Bridge suite;
2. new regression proving:
   - Agent launch occurs;
   - Agent returns non-zero after RUNNING;
   - dispatch/execution becomes `NEEDS_RECONCILIATION`;
   - same dispatch cannot be claimed again;
   - no alternate Agent is substituted;
3. existing pre-spawn failure semantics remain terminal/actionable where non-execution is proven;
4. `git diff --check` PASS;
5. delivery validator PASS;
6. required evidence manifest and verification JSON exist and parse;
7. changed paths remain exact allowlist;
8. report secret scan PASS.

No test may require paid Codex/Copilot execution.

## 7. Acceptance contract

FIX-01 is acceptable only when all are true:

```text
FULL_TESTS=PASS
NONZERO_AFTER_AGENT_START=NEEDS_RECONCILIATION
DISPATCH_REPLAY_AFTER_NONZERO=BLOCKED
NO_AGENT_SUBSTITUTION=PASS
PRESPAWN_FAILURE_SEMANTICS=PASS
GIT_DIFF_CHECK=PASS
DELIVERY_VALIDATOR=PASS
EVIDENCE_MANIFEST=PRESENT_VALID
VERIFICATION_JSON=PRESENT_VALID
REPORT_STATE=CONSISTENT
OUT_OF_SCOPE_CHANGES=0
REMOTE_SHA_READBACK=PASS
FINAL_STATE=PUSHED_UNREVIEWED
```

## 8. Branch / stop boundary

Task branch:

`work/FOX2-BRIDGE-DESKTOP-01-02-FIX-01-codex`

Preferred worktree:

`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-02-FIX-01-CODEX`

Execution is intentionally deferred until the Owner confirms Codex token/quota is available.

Stop boundary after execution:

`PUSHED_UNREVIEWED`

No PR, merge, main, deploy, provider, broker or LIVE.
