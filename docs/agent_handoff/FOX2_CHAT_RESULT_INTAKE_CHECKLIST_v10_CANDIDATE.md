# FOX2 — CHAT Result Intake Checklist v10 CANDIDATE — Dictionary-Bound

**Proposed source resolution:** Project Dictionary v1.3 CANDIDATE -> Policy V1.9.0 CANDIDATE -> Routing V1.4.0 CANDIDATE -> Protocol v13 CANDIDATE. In-flight Agent receipts retain frozen historical bindings.

For every new/re-scoped result intake:

1. **Dictionary identity**
   - read exact Dictionary path/commit/hash bound by dispatch;
   - verify dispatch schema/control/path identity is declared current/supported;
   - verify Policy/Protocol identities match Dictionary.

2. **Immutable delivery**
   - exact repository;
   - exact task branch;
   - full remote result SHA;
   - expected parent/base ancestry;
   - no unexpected history rewrite.

3. **Scope**
   - changed paths inside authorized code/report paths;
   - no frozen semantic source changed without authority.

4. **Execution tuple**
   - Agent Product;
   - model policy/tier/model/reasoning;
   - permission profile;
   - execution path;
   - delivery owner;
   - no silent substitution/downgrade.

5. **Git publication**
   - exactly one publication owner;
   - remote SHA readback equals delivered SHA;
   - no main/PR/merge/deploy unless separately authorized.

6. **Validation**
   - required tests actually PASS;
   - task-material capability checks PASS;
   - evidence resolves all material claims;
   - canonical artifact/text hygiene where applicable.

7. **Failure/replay**
   - post-start uncertainty is not falsely marked success;
   - consumed dispatch not replayed;
   - no Agent substitution.

8. **Semantic boundaries**
   - Dictionary used only for identity/compatibility;
   - Policy/BRD/Contract/Technical semantics remain consistent;
   - no provider/broker/LIVE expansion.

9. **Verdict**
   - ACCEPTED;
   - ACCEPTED_PARTIAL;
   - REWORK;
   - BLOCKED.

A stale in-commit wording such as UNREVIEWED may be non-material when immutable remote evidence proves final delivery state; do not create micro-fix WPs solely for such wording.

`CHAT_INTAKE_V9=DICTIONARY_BOUND / REMOTE_READBACK_REQUIRED / SELF_ACCEPTANCE=NO`


## CHAT direct execution evidence and next routing — candidate

For tasks completed directly by CHAT, collect actual operation authorization, input provenance, before/after destination identity, exact remote commit/byte digest and conflict guard. Do not fabricate an Agent result receipt or trigger any consumed dispatch. For Agent results, CHAT remains independent recipient/intake owner; actual tests and runtime facts remain required, never merely source claims. After review, CHAT itself performs all authorized next safe work before considering another Agent or independent WORK review. `CHAT_DIRECT_COMPLETED` is a work-result classification, not certified release authority.
