# FOX2 Skills — install, use and rollback

## Current installation

The intact package is installed and enabled in the active user's native host as
`fox2-skills-integrated@fox2-local`. All 17 names are returned by `skills/list` and
are available in the current conversation's Skills catalog. Names carry the prefix
`fox2-skills-integrated:`. The installed cache is under the user's Codex plugin
cache, separate from the source checkout. No credential was copied.

Use the normal Skill selector/mention for the desired FOX2 task. A factual draft,
read-only review, technical comparison or authorized bounded local test can use
explicitly labeled conditional inputs. Each Skill now gives its own task-specific
workflow. Actual assignment must still follow applicable project routing rules.

The shared Python runtime is optional preparation for governed execution; it is
not necessary to return an analytical draft and cannot grant authority.

## Install or refresh the complete package

The repository-local marketplace is `.agents/plugins/marketplace.json` under the
package root. It points to this same package, so there is one maintained source.

```powershell
codex plugin marketplace add C:/Projects/FOX2-worktrees/FOX2-SKILLS-INTEGRATED-RELEASE/fox2_skills
codex plugin add fox2-skills-integrated@fox2-local
codex plugin list --marketplace fox2-local --json
```

The native app-server `skills/list` request with `forceReload=true` confirms loaded
names/paths. Explicit `turn/start` skill inputs contain `type=skill`, returned
`name` and installed `path`. Use `account/read` only to establish authentication
status; never copy credentials into a test runtime. The current installation was
checked against exact source bytes after refresh.

Keep the package intact: each Skill depends on sibling `shared/` guidance or tools.
Do not copy isolated Skill folders and lose their relative dependencies. Existing
install destinations or modified user files must be preserved during rollback.

## Source authority and meaningful work

The Owner's source baseline remains conditional, not certified EFFECTIVE. This
does not block authorized independent analysis. The shared host guidance keeps
authority checks at source certification, canonical changes, executable governance
handoffs, dispatch and release/promotion actions. No Skill grants permissions or
automatically rebinds an in-flight source lock.

For governed binding use `shared.native_registry.bind` with
`shared.release_chain.ReleaseChainVerifier(scope, cutoff, authority_provider)`.
The provider must independently verify scope, cutoff, owning approval, allowed
immutable refs and complete competing-release/supersession closure. The typed
AuthoritySnapshot is a host adapter contract, not an approval schema or a new
Registry. No provider means AUTHORITY_UNVERIFIED. Never deserialize a task's own
claims into trusted authority records or use synthetic test providers for release.

`tools/verify_release_chain.py --help` describes the authenticated read-only audit
of an explicitly named conditional baseline. Its CLI has no authority-file bypass.
Its expected conditional result is AUTHORITY_UNVERIFIED, exit 2 and no effects.

## Evidence limits

53 regression tests and all 17 metadata validations pass. The active native host
loaded 17 Skills and completed one batch of 17 concrete analytical fixture requests.
Those outputs were reviewed against domain-specific rubrics. This is actual model
invocation, with supplied fixtures; it is not 17 separate isolated sessions, an
implicit-routing evaluation, live domain data certification, or proof of write-side
effects. An earlier read-only host attempt also exposed an execution-helper setup
failure; no successful shell/write behavior is inferred from that failed attempt.

The original isolated package install/uninstall/rollback and real local file-operation
helper tests remain useful evidence, separate from the model's analytical responses.
Source-governed release acceptance remains NOT_READY.

## Remove or rollback

```powershell
codex plugin remove fox2-skills-integrated@fox2-local
```

Only remove it when the user requests uninstall. The installation remains active.
For a separately copied isolated package use `tools/package_install.py rollback`
with its original receipt; changed owned files cause a conflict instead of deletion.

After updating evidence/report, run `tools/assemble_delivery.py` to package the
existing integrated report. It does not manufacture test or readiness claims.
`tools/build_contracts.py` maintains only helper contracts, not curated SKILL.md prose.
