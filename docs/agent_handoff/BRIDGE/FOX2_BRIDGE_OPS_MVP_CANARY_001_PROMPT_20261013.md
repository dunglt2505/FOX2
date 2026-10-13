# FOX2 Bridge OPS MVP Canary 001 — Copilot CLI

You are the execution agent for the FOX2 Bridge Operational MVP canary.

The Bridge has already resolved the exact worktree and will pre-create the authorized parent directory. Do not create any other directory.

Create exactly this file:

`reports/FOX2-BRIDGE-OPS-CANARY-001/ops_mvp.txt`

with exactly these two lines:

```text
FOX2_BRIDGE_OPS_MVP_CANARY_OK
dispatch=FOX2-BRIDGE-OPS-CANARY-001
```

Do not modify any other file.

Then run only these Git commands:

1. `git diff --check`
2. `git status --short`
3. `git add reports/FOX2-BRIDGE-OPS-CANARY-001/ops_mvp.txt`
4. `git commit -m "FOX2 Bridge OPS canary 001: Copilot reached"`
5. `git push origin HEAD:work/FOX2-BRIDGE-OPS-CANARY-001-copilot`

Do not merge, do not create a PR, do not touch main, and do not modify provider/broker/LIVE state.

After the push succeeds, include this marker in your final response:

`FOX2_BRIDGE_OPS_MVP_CANARY_OK`
