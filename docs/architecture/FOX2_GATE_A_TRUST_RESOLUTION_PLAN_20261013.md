# FOX2 — Gate A Trust Resolution Plan
Date: 2026-10-13
Status: ACTIVE_ARCHITECTURE_BLOCKER / NO_GATE_A_PASS
Applies to: FOX2 Local Agent Bridge v0.4

## 1. Target
Bridge v0.4 target:
`CHAT -> immutable Git dispatch -> Bridge receive/validate -> later Agent launch`.

Selected MVP trust target in v0.4:
`GITHUB_APP + ENFORCED_CONTROL_REF`.

Gate A cannot PASS from schema/hash checks alone. Dispatch provenance must be enforced, not merely documented.

## 2. Fresh capability evidence
Authenticated CHAT GitHub checks on 2026-10-13 observed:
- repository `dunglt2505/FOX2`: private, owner type `User`;
- authenticated repository permissions exposed to CHAT include admin/maintain/push/pull;
- repository rulesets API returns HTTP 403:
  `Upgrade to GitHub Pro or make this repository public to enable this feature.`
- main branch protection API returned HTTP 403 `Resource not accessible by integration`.
- therefore no effective protected/enforced control ref is currently proven.

Disposition:
`AUTOMATED_GATE_A=BLOCKED_CAPABILITY_UNAVAILABLE`.

This does NOT block BRG-003 source baseline or offline implementation/testing of BRG-010/020/030/040. It blocks certification and Agent launch through the target automated path.

## 3. Preferred resolution — minimum architecture change
Keep Bridge Technical v0.4 unchanged and satisfy its selected trust target.

Required external/platform prerequisites:
1. Enable a GitHub plan/capability that supports enforceable repository rulesets for this private repository (the current API explicitly indicates GitHub Pro or public visibility; public visibility is not recommended for FOX2).
2. Provision a dedicated FOX2 GitHub App/service publisher with least privilege.
3. Establish a dedicated immutable control ref/branch for dispatch.
4. Enforce creation/update restrictions so only the dedicated publisher identity can produce trusted dispatch commits; separately prohibit force-push/deletion as supported.
5. Pin exact ruleset/control-ref IDs and read them back through authenticated API.
6. Define credential/token custody, rotation, revocation and failure behavior.
7. Prove CHAT's authorized route to the dedicated publisher identity and bind publication evidence to exact dispatch/Owner-selection/decision receipts.
8. Execute Gate-A negative tests: unauthorized writer, mutated dispatch, wrong ancestry, replay, mismatched decision receipt, unavailable publisher.

This route is preferred because it preserves the released v0.4 trust design and minimizes specification churn.

## 4. Alternative resolution — only if preferred capability is rejected/unavailable
Design a new trust mechanism that does not depend on the unavailable control-ref enforcement.

Requirements:
- equivalent or stronger provenance than self-declared JSON/ordinary commit author text;
- independent verifiability by Bridge before launch;
- explicit publisher identity and credential custody;
- tamper-evident binding of dispatch + task + prompt + source + Owner-selection/decision receipts;
- replay resistance and revocation;
- no reliance on mutable Issue/branch text;
- negative tests for impersonation and stale/mutated dispatch.

This route requires:
1. a Technical Spec revision (v0.5 Candidate first);
2. independent trust/security review;
3. Owner approval/release;
4. new Gate-A certification evidence.

Do not silently replace the v0.4 trust target inside code.

## 5. Parallel work allowed now
- BRG-003 sanitized baseline.
- BRG-010 Bridge Core.
- BRG-020 DispatchPoller.
- BRG-030 DispatchValidator/ReplayGuard.
- BRG-040 RuntimeAttestor.
All may be developed/tested offline under scoped bootstrap authority.

STOP before:
- claiming Gate A PASS;
- launching Copilot/Codex through Bridge;
- trusting an unprotected branch as authoritative dispatch;
- automatic result delivery/closed-loop claims.

## 6. Decision state
```text
PREFERRED=ENABLE_ENFORCED_CONTROL_REF_AND_DEDICATED_PUBLISHER
PREFERRED_REQUIRES_EXTERNAL_PLATFORM_CHANGE=YES
ALTERNATIVE=NEW_TRUST_MECHANISM_REQUIRES_TECH_SPEC_REVISION_AND_REVIEW
CURRENT_GATE_A=BLOCKED_CAPABILITY_UNAVAILABLE
BRG003_010_040_OFFLINE_PROGRESS=ALLOWED_SUBJECT_TO_OWN_GATES
AUTO_AGENT_LAUNCH=NO
MERGE=NO
LIVE=NO
```
