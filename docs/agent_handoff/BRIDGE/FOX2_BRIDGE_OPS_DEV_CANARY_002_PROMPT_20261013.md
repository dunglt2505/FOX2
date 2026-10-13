# FOX2 Bridge OPS DEV Canary 002 — exact pytest permission

You are the execution agent for the FOX2 Bridge OPS DEV permission canary.

Goal: prove the Bridge permits the exact command `python -m pytest --version`, while keeping shell access bounded.

Do exactly this:

1. Run exactly:
   `python -m pytest --version`

2. If and only if that command succeeds, create exactly:
   `reports/FOX2-BRIDGE-OPS-DEV-CANARY-002/pytest_permission.txt`

   with exactly these three lines:

```text
FOX2_BRIDGE_OPS_DEV_PYTEST_002_OK
dispatch=FOX2-BRIDGE-OPS-DEV-CANARY-002
pytest_permission=PYTEST_EXACT_COMMAND
```

3. Do not modify any other file.

4. Then run only these Git commands:
   - `git diff --check`
   - `git status --short`
   - `git add reports/FOX2-BRIDGE-OPS-DEV-CANARY-002/pytest_permission.txt`
   - `git commit -m "FOX2 Bridge OPS DEV canary 002: exact pytest permission"`
   - `git push origin HEAD:work/FOX2-BRIDGE-OPS-DEV-CANARY-002-copilot`

Do not run package installation, PowerShell, curl, web access, provider access, broker commands, merge, PR, main, or LIVE operations.

After the push succeeds, include this marker in your final response:

`FOX2_BRIDGE_OPS_DEV_PYTEST_002_OK`
