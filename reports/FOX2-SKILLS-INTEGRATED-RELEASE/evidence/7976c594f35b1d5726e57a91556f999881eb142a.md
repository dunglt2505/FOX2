# CODEX — BRIDGE-DESKTOP-BATCH-A — Project Dictionary Rollup

Apply the exact CHAT plan:

`docs/agent_handoff/FOX2-BRIDGE-DESKTOP-BATCH-A/CHAT_PROJECT_DICTIONARY_ROLLUP_PLAN.md`

Do not rediscover architecture and do not split this into sub-WPs.

Role: Bridge compatibility implementation  
Agent: CODEX CLI  
Model: gpt-6.1-sol  
Reasoning: medium  
Permission: FULL_ACCESS  
Delivery owner: AGENT

Use the canonical Project Dictionary at exact Git commit:
`28866ee6a61bde3fc3837ebd999c7b470afc7486:docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`

Implement generated binding + drift test + config/poller/schema normalization exactly as the CHAT plan specifies.

Preserve all existing passing Batch A behavior and full regressions.

Writable scope remains only:
- agent_bridge/**
- reports/BRIDGE-DESKTOP-BATCH-A/**

No Policy/BRD/Technical edits by CODEX.
No PR/main/merge/deploy/provider/broker/LIVE.

Run focused + full Bridge tests, regenerate existing Batch A evidence, git diff check, commit/push same task branch, verify remote SHA.

Finish only with:

FOX2_BRIDGE_DESKTOP_BATCH_A_DICTIONARY_ROLLUP_PUSHED_UNREVIEWED
