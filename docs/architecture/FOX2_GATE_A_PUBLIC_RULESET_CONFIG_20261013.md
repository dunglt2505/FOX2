# FOX2 — Gate A Public Ruleset & CHAT Publisher Route Configuration
Date: 2026-10-13
Status: ADMIN_CONFIG_REQUIRED / TEST_PLAN_READY
Repository: dunglt2505/FOX2
Visibility: PUBLIC (verified by CHAT)
Control branch: work/FOX2-LOCAL-DISPATCH-chat

## 1. Current verified facts
- Repository visibility readback: PUBLIC.
- Repository rulesets endpoint is now accessible and returns an empty set: no ruleset is configured yet.
- Control branch exists.
- Current GitHub connector installation is installation ID `169139119`, installed on account `dunglt2505`, repository selection `all`, and can access both `Fox` and `FOX2`.
- Commits written through CHAT currently appear with GitHub author/committer `dunglt2505`, are unsigned, and raw commit readback does not expose a `performed_via_github_app` identity. Therefore commit metadata alone is NOT sufficient publisher proof.

## 2. Gate-A publisher strategy for public bootstrap
Use the exact GitHub App that backs the current CHAT GitHub connector as the **authorized service publisher route for the FOX2 dispatch control ref**, and prove that route operationally through ruleset enforcement.

This is acceptable for Gate-A testing only if ALL of the following are demonstrated:
1. the active ruleset targets only the dispatch control branch;
2. ordinary user/admin updates do not bypass the restriction;
3. only the exact GitHub App integration used by the CHAT connector is configured as operational bypass;
4. CHAT can publish a canary through that connector after the ruleset is active;
5. a direct ordinary-user mutation attempt is rejected;
6. ruleset readback identifies the exact Integration actor and active enforcement;
7. immutable branch ancestry/readback matches the CHAT canary commit.

If the current connector App cannot be uniquely selected/pinned as the bypass integration, STOP and provision a separate service publisher plus a supported CHAT-to-publisher route. Do not weaken the ruleset to user/admin bypass as a substitute.

## 3. Exact ruleset configuration
GitHub UI:
Repository FOX2 → Settings → Rules → Rulesets → New branch ruleset.

Set:
- Name: `FOX2 Dispatch Control Trust`
- Enforcement status: `Active`
- Target branches → Include by pattern:
  `refs/heads/work/FOX2-LOCAL-DISPATCH-chat`
  (If the UI expects branch-name syntax rather than full ref, select/pin the exact existing branch `work/FOX2-LOCAL-DISPATCH-chat`; CHAT will verify the API readback after save.)
- Bypass list:
  - add ONLY the GitHub App / Integration that corresponds to the current CHAT GitHub connector;
  - bypass mode: Always / permitted to bypass this ruleset;
  - do NOT add repository Admin role, Owner role, Team or ordinary user as routine bypass.

Enable rules:
- Restrict creations.
- Restrict updates.
- Restrict deletions.
- Block force pushes / non-fast-forward updates.
- Require linear history if available without conflicting with the publisher path.

Do NOT enable rules that force PR-only updates on this control ref unless the publisher path is separately redesigned, because the control branch is intentionally an immutable machine-published dispatch ledger rather than a human PR branch.

## 4. After-save readback expected by CHAT
CHAT will immediately GET:
- repository visibility;
- ruleset collection;
- exact ruleset detail by ID;
- control branch identity/head.

Required observed fields:
```text
visibility=public
ruleset.name=FOX2 Dispatch Control Trust
ruleset.enforcement=active
target=branch
conditions.ref_name includes exact dispatch control ref
rules include creation/update/deletion/non_fast_forward (or equivalent effective controls)
bypass_actors contains exactly the intended Integration/App operational publisher
ordinary user/admin bypass absent
```

## 5. Gate-A canary publication test
Only after exact ruleset readback PASS, CHAT will publish one inert canary artifact to:
`docs/agent_handoff/GATE_A_CANARY/dispatch/GATE-A-CANARY-001.json`
on `work/FOX2-LOCAL-DISPATCH-chat`.

Canary contains:
- project=FOX2;
- type=TRUST_CANARY_ONLY;
- no Agent launch;
- max_runs=0;
- no code/DEV authority;
- current Policy/Bridge hashes;
- unique nonce-like dispatch ID chosen deterministically from the canary record;
- explicit `DO_NOT_EXECUTE`.

Required positive evidence:
- CHAT connector write succeeds;
- exact remote commit SHA/blob readback succeeds;
- branch ancestry is fast-forward;
- ruleset remains active and unchanged.

## 6. Required negative control
After the positive canary, perform ONE ordinary-user direct update attempt to the same control branch through GitHub's normal web editor or ordinary user Git push (not through CHAT connector).

Expected:
`REJECTED_BY_RULESET`.

No source code, secrets or existing dispatch may be changed. Use a disposable canary path only.

If ordinary user write succeeds:
`GATE_A=FAIL_TRUST_NOT_ENFORCED`.

## 7. Gate-A disposition after canary
Gate A may advance to PASS only if:
- active ruleset exact readback PASS;
- publisher Integration identity uniquely pinned;
- CHAT connector canary PASS;
- ordinary-user negative write BLOCKED;
- branch ancestry/replay controls PASS;
- dispatch validator/trust-anchor/replay/runtime offline acceptance for BRG-010..040 PASS.

This document does not itself grant Agent launch. Gate B remains separate.

## 8. Current state
```text
REPO_PUBLIC=PASS
RULESET_CAPABILITY=PASS_AVAILABLE
RULESET_CONFIGURED=NO
CONTROL_BRANCH=PASS_EXISTS
CHAT_CONNECTOR_INSTALLATION=169139119_OBSERVED
COMMIT_METADATA_PUBLISHER_PROOF=INSUFFICIENT
RULESET_APP_BYPASS_PROOF=NOT_RUN
CANARY_WRITE=NOT_RUN
ORDINARY_USER_NEGATIVE_TEST=NOT_RUN
GATE_A=BLOCKED_ADMIN_CONFIG
AUTO_AGENT_LAUNCH=NO
MERGE=NO
LIVE=NO
```
