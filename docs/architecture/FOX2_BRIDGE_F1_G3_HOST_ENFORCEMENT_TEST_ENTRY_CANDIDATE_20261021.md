# FOX2 — Bridge F1 G3 Host Enforcement/Test Entry — CANDIDATE

Date: 2026-10-21  
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`  
Feature: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`  
Stage: TEST  
Class: `AUTHORIZED_CANDIDATE_WRITE / NON-EXECUTABLE`

## Current accepted predecessor

G2 BUILD is CHAT-accepted:
- code: `66e8f0a8b3a93140b5f908628b55ac965e15b96e`;
- result/evidence: `ac1d1184255945b2c4304641360a1e661ff2d7bd`;
- CHAT review: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/G2_A01_CHAT_RESULT_REVIEW_20261021.md` @ `dcf42dd76c8f22e155d469d356e1f1219f3d7b14`.

G2 acceptance does NOT authorize G3 host mutation.

## Live governance source resolution

Current governance release branch readback: `work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019` @ `d34da1e3b4918a902646621b487ca8ad3e05b0e0`.

For new/re-scoped G3 coordination:
- Policy 2.0.0 — OWNER-approved governance effective; machine installed effectivity NOT_ATTESTED.
- Dictionary 1.3 — governance effective for new/re-scoped CHAT work; Bridge installed machine adoption NOT_ATTESTED.
- Routing 1.4.0 — governance effective for new/re-scoped CHAT work.
- Git-first Protocol 12 — released unchanged.
- BRD-09 v0.1 REV3 and Bridge TechSpec v0.7 REV10 remain CANDIDATE globally; G1/G2 task-specific accepted design/build evidence supplies this Whole-WP stage contract.

No source listed here grants deploy/main/merge/provider/broker/LIVE rights.

## G3 purpose

G3 proves **isolated Windows host enforcement** of the accepted F1 design. It is not Owner-host production adoption and not Canary.

G3 must demonstrate that the G2 source actually behaves as a privileged Windows trust boundary when installed into an isolated test target:
1. protected ProgramData authority root;
2. LocalSystem trusted service;
3. effective AppLocker enforcement with AppIDSvc active;
4. authenticated named-pipe caller identity;
5. service-owned global claim + suspended CreateProcessAsUser spawn;
6. copied/alternate-root legacy execution closure;
7. restart/revoke/rollback/tombstone semantics under real service lifecycle;
8. fail-closed behavior on service/AppIDSvc/policy/source/package/store drift.

## Privileged operations requiring separate Owner G3 authority

None of the following may occur from this candidate alone:

- elevate to Administrator;
- create/modify ACLs under ProgramData authority root;
- install/configure/start/stop/delete the FOX2 F1 Windows service;
- configure AppIDSvc startup or start/stop AppIDSvc;
- apply/replace effective AppLocker policy;
- reboot the Windows test target;
- create a real positive service-owned Agent child;
- intentionally stop/crash service/AppIDSvc during tests;
- run rollback/reinstall host mutation;
- alter scheduled tasks/startup outside explicit G3 fixture scope.

A future executable G3 task/PowerShell must enumerate each mutation and rollback action explicitly.

## G3 target boundary

Preferred target: disposable/isolated Windows 11 Pro test VM or otherwise isolated test host with rollback/recovery available.

Do NOT begin by mutating the Owner's daily-use installed Bridge host unless a later G4/adoption scope explicitly authorizes that target.

G3 and G4 stay separate:
- **G3:** isolated enforcement evidence.
- **G4:** Owner-host installed adoption/readiness.

## Required host PreExec before any mutation

A future G3 host PreExec must record at minimum:

### Identity / source
- exact Windows target identity and edition/build;
- exact G2 source/result/review SHAs;
- exact generated package/policy/adoption-plan digests;
- clean/non-main Git source;
- no competing material writer;
- G2 A01 remains closed/no replay.

### Administrative capability
- PowerShell 7+;
- elevated Administrator token available for G3 only;
- Service Control Manager create/config/query rights;
- ProgramData ACL read/write rights for the isolated fixture root;
- AppLocker cmdlets available;
- Application Identity service exists;
- ability to query effective AppLocker policy;
- rollback/recovery path proven before policy mutation.

### Safety / rollback
- current effective policy exported before changes;
- current AppIDSvc/service states recorded;
- test service name and authority root do not collide with production/Owner adoption identity unless specifically authorized;
- test rollback procedure can restore prior AppLocker/AppIDSvc/service/ACL state;
- positive execution stays blocked until all required negative gates have passed.

### Tooling
- Python/runtime/package prerequisites for the accepted G2 package;
- .NET/Desktop prerequisite if included in G3 package;
- required Windows native APIs observable;
- no Internet/provider/trading broker dependency.

PreExec outcome must be durable `PASS / BLOCKED / INFRA_FAILED`; NOT_RUN is never PASS.

## Required G3 execution order

After explicit G3 authority + fresh source resolution + task-specific host PreExec PASS:

1. **Snapshot and recovery proof**
   - export current effective AppLocker policy;
   - record AppIDSvc state;
   - prove rollback instructions and isolated target.

2. **Package/provenance construction**
   - construct the exact G2-derived Windows package in an isolated build environment;
   - verify package digest, source-module inventory and accepted source SHA;
   - no installation yet.

3. **Protected host state preparation**
   - create isolated authority root with reviewed ACL/owner;
   - provision reconciled broker store and sealed adoption/test plan;
   - verify ordinary user cannot modify/replace/reparse protected state.

4. **AppLocker deployment**
   - generate exact policy artifact from reviewed inventory;
   - apply Enforce mode to relied-upon Exe/Script/MSI/Dll collections;
   - ensure AppIDSvc is running;
   - query effective policy and verify canonical digest equals expected artifact;
   - unexpected policy/system dependency gap => DENY/HOLD.

5. **Service installation/start**
   - install exact LocalSystem service binary command;
   - verify SCM account/type/start mode/image path;
   - verify protected runtime inventory and service singleton/pipe identity.

6. **Negative gates before any positive spawn**
   - service absent/stopped => DENY;
   - AppIDSvc stopped => DENY;
   - effective policy mismatch => DENY;
   - forged SID/session/request/source/package/nonce/epoch => DENY;
   - unprotected/reparse runtime or adoption-plan drift => DENY;
   - copied legacy executable/script/interpreter alternate-root probes => blocked by actual AppLocker enforcement;
   - direct launcher/ledger/local E2E bypass => DENY.

7. **Single bounded positive fixture**
   - only after all required negatives PASS;
   - authenticated interactive caller;
   - service-owned claim + suspended child + Job + resume;
   - exactly one same-dispatch creation;
   - no caller-side Popen fallback;
   - credential/session usability recorded without exposing credentials.

8. **Lifecycle / no-replay**
   - restart service => epoch increments;
   - old lease/request cannot spawn;
   - consumed identity stays consumed;
   - policy/AppIDSvc loss after staging closes authority;
   - service crash/stop closes owned Job as designed;
   - clock rollback/revocation returns DENY.

9. **Rollback**
   - revoke authority;
   - remove/disable test service as scoped;
   - restore prior AppLocker/AppIDSvc state;
   - preserve broker consumed/tombstone state required for no-replay evidence;
   - verify positive authority ends in DENY.

## G3 acceptance matrix

G3 is PASS only when all material isolated-host gates have real evidence:

- E1 protected root owner/DACL/reparse attack closure;
- E2 SCM LocalSystem service exact binary/config/singleton;
- E3 effective AppLocker Enforce policy digest + AppIDSvc running;
- E4 actual copied/alternate-root legacy executable/script/interpreter blocks;
- E5 authenticated pipe peer identity and untrusted server/caller denial;
- E6 one real service-owned positive CreateProcessAsUser fixture after negatives;
- E7 same-dispatch concurrency => exactly one creation + global consumption;
- E8 restart/revoke/policy-loss/service-loss/clock rollback => no replay/new spawn;
- E9 source/package/task/adoption-plan drift => DENY;
- E10 rollback restores host controls and ends at DENY while preserving tombstones.

Any required FAIL / BLOCKED / NOT_RUN => G3 not accepted.

## Explicit non-effects

Even G3 PASS would NOT by itself authorize:
- Owner-host G4 adoption;
- Canary009;
- `INTERNAL_FOX2_BRIDGE_READY`;
- main/merge;
- production/provider/trading broker/LIVE.

## Current verdict

`G3_ENTRY_PREPARED / EXECUTION_BLOCKED`

Observed:
- G2 BUILD accepted;
- G3 host enforcement NOT_RUN;
- no G3 privileged authority;
- no G3 host PreExec;
- current F1 positive runtime remains DENY.

REAL_BLOCKER: explicit Owner authorization for the bounded G3 privileged isolated-host mutation/test scope above.

NEXT_SAFE_ACTION after that authority: re-resolve live governance/source, bind the exact isolated target/source/package/policy, run task-specific G3 host PreExec, then issue one governed G3 execution task. No G2 replay.
