# FOX2 Bridge E2E Canary — Copilot CLI

You are the execution agent for the FOX2 Bridge E2E canary.

## Exact task

Work only in the current Git worktree and current branch.

Create exactly this file:

`reports/FOX2-BRIDGE-E2E-CANARY/bridge_called_copilot.txt`

with exactly these two lines:

```text
FOX2_BRIDGE_E2E_CANARY_OK
dispatch=FOX2-BRIDGE-E2E-CANARY-001
```

Do not modify any other file.

Then run:

1. `git diff --check`
2. `git status --short`
3. `git add reports/FOX2-BRIDGE-E2E-CANARY/bridge_called_copilot.txt`
4. `git commit -m "FOX2 Bridge E2E canary: Copilot reached"`
5. `git push origin HEAD:work/FOX2-BRIDGE-E2E-CANARY-copilot`

Do not merge, do not create a PR, do not touch main, do not modify any provider/broker/LIVE state.

After the push succeeds, include this marker in your final response:

`FOX2_BRIDGE_E2E_CANARY_OK`
