# FOX2 — CHAT M1 v0.4 Source Recovery Result

**Source gate:** `GIT_SOURCE_READY=YES` for the pinned Git commit `1e1972cb204ac780e68878c34f6a59d205bdb18c` on branch `work/FOX2-M1-V04-SOURCE-RECOVERY-chat-20261012`.

**Scope:** 8 released M1 sources and 2 companions. **Remote readback:** 10/10 exact Git blob SHA matches expected blobs computed from official Library raw bytes. Change diff against prior PR #2 head `1534e021c952147c42816a7f95c086ab59829b38`: 10 additions, no runtime code changes. Source CSV original mixed line endings preserved; its SHA-256 remains `ad1fd6ef4b4b150132366a5ccf1d465aa347e6411060f32fae4672777fb4bf92`.

**Source publication:** Library release receipt `FOX2_M1_V04_LIBRARY_RELEASE_RECEIPT_20261011.json` remains canonical. New derivative Git receipt: `docs/agent_handoff/FOX2_M1_V04_SOURCE_SYNC_RECEIPT_20261012.json` and updated `SOURCE_INDEX.json`.

**Prior blocker:** Previous API tool safety refusal root cause remains unknown. The Owner expressly requested one retry. The standard supported connector operation succeeded, with no runtime/source mutation and no need to assert why the earlier call was refused.

**Not performed:** 105 M1 functional tests; Copilot/Windows preflight; source integration into `main`; GitHub branch protection; independent DEV model/quota/worktree/writer grants; DNSE Production access; merge, broker or LIVE.

**Next gate:** CHAT may prepare future Agent handoff against an explicitly pinned verified Git commit **only after** separate `CODE_ALLOWED` scope, Agent capability, source/host/worktree/WIP and writer permission checks. Source YES is not DEV YES.

**Controls:** `CODE_ALLOWED=NO`, `MERGE_ALLOWED=NO`, `MAIN_PUSH=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO`.
