# FOX2 — CHAT Result Intake Checklist v9 — Dictionary-Bound

**Current source resolution:** Project Dictionary v1 -> Policy V1.8.7 -> Routing V1.2.8 -> Protocol v10.

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
