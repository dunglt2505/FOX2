# FOX2 Bridge Codex CLI Canary 003

You are the Codex CLI execution agent for a FOX2 Bridge canary.

Goal: prove the Bridge can invoke Codex CLI on Windows with the pinned unelevated sandbox fallback, run the controlled Python/pytest environment, create one authorized result file, and let the Bridge verify/commit/push the result.

Do exactly this:

1. Run:
   `python -m pytest --version`

2. If and only if that command succeeds, create exactly:
   `reports/FOX2-BRIDGE-CODEX-CANARY-003/codex_bridge.txt`

   with exactly these three lines:

```text
FOX2_BRIDGE_CODEX_CLI_CANARY_003_OK
dispatch=FOX2-BRIDGE-CODEX-CANARY-003
agent=CODEX
```

3. Do not modify any other file.

4. Do not run `git add`, `git commit`, `git push`, merge, PR, package installation, provider access, broker commands, or LIVE operations. The Bridge owns Git commit/push after you exit.

5. Finish your response with this exact marker:

`FOX2_BRIDGE_CODEX_CLI_CANARY_003_OK`
