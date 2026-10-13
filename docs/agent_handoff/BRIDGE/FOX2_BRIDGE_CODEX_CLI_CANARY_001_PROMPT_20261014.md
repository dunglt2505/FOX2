# FOX2 Bridge Codex CLI Canary 001

You are the Codex CLI execution agent for a FOX2 Bridge canary.

Goal: prove the Bridge can invoke Codex CLI, Codex can run the controlled Python/pytest environment and create one authorized result file, and the Bridge can then verify/commit/push the result itself.

Do exactly this:

1. Run:
   `python -m pytest --version`

2. If and only if that command succeeds, create exactly:
   `reports/FOX2-BRIDGE-CODEX-CANARY-001/codex_bridge.txt`

   with exactly these three lines:

```text
FOX2_BRIDGE_CODEX_CLI_CANARY_OK
dispatch=FOX2-BRIDGE-CODEX-CANARY-001
agent=CODEX
```

3. Do not modify any other file.

4. Do not run `git add`, `git commit`, `git push`, merge, PR, package installation, provider access, broker commands, or LIVE operations. The Bridge owns Git commit/push after you exit.

5. Finish your response with this exact marker:

`FOX2_BRIDGE_CODEX_CLI_CANARY_OK`
