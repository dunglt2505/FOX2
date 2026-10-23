# FOX2 Skills v0.5.9 — VS Code Codex Extension coding handoff

- Owner direction 2026-10-23: for new interactive coding tasks, Router prefers CODEX in **Visual Studio Code Codex Extension** when observed capable; CLI/Bridge reserved for headless/installed-host and proven supervised runs.
- Prompt Builder emits a self-contained VS Code paste-ready prompt with Goal/Scope/Context/Execution/Acceptance/Return, correct workspace/worktree and result Git ref. It never pretends to inject directly into extension or start Agent without actual integration acknowledgement.
- Native IDE work does not require automatic PowerShell launcher. Preserve pwsh Git syntax/exit-code safeguards for explicitly selected host script jobs.
- Separate Git publisher rights: Agent push only if authorized; Bridge push only with proven IDE/worktree integration; otherwise authorized publisher handoff and GIT_DELIVERY_PENDING. Never double push or replay consumed Dispatch.
- No changes to earlier 0.5.8 Skill Routing Matrix, one Whole-WP, test-only evidence, result acceptance or Watch/Board sync semantics.
- Static tests and manifest inventory only; actual Windows VS Code Extension handoff and Bridge integration NOT_RUN in this package. No main merge, LIVE, installed host behavior, or human governance promotion implied.
