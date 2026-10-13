# FOX2 Bridge E2E Canary 003 — Copilot CLI

You are the execution agent for the FOX2 Bridge E2E retry canary.

The Bridge has already created the authorized parent directory. Do not run mkdir or any other directory-creation shell command.

Create exactly this file:

`reports/FOX2-BRIDGE-E2E-CANARY-003/bridge_called_copilot.txt`

with exactly these two lines:

```text
FOX2_BRIDGE_E2E_CANARY_003_OK
dispatch=FOX2-BRIDGE-E2E-CANARY-003
```

Do not modify any other file.

Then run only these Git commands:

1. `git diff --check`
2. `git status --short`
3. `git add reports/FOX2-BRIDGE-E2E-CANARY-003/bridge_called_copilot.txt`
4. `git commit -m "FOX2 Bridge E2E canary 003: Copilot reached"`
5. `git push origin HEAD:work/FOX2-BRIDGE-E2E-CANARY-003-copilot`

Do not merge, do not create a PR, do not touch main, do not modify any provider/broker/LIVE state.

After the push succeeds, include this marker in your final response:

`FOX2_BRIDGE_E2E_CANARY_003_OK`
