# P1 Result Recovery - Current Session Checks

This evidence records only checks performed during the Policy V1.7.1 recovery
session. It is not an original P1 execution log and does not verify the
conversation-recovered P1 findings.

Recovery session began at: 2026-10-12T08:45:45Z
Pinned readbacks and schema validation repeated at: 2026-10-12T08:51:46Z

## Policy and pinned Git sources

- Repository: `dunglt2505/FOX2`
- Policy commit: `ef3975952006868ef2fd4e64619ebdbf3cfc8411`
- Policy path: `docs/governance/FOX2_POLICY_V1.7.1.md`
- SHA-256 recomputed from `git show` raw bytes: `9c8784781d13e05a59749e33a72b2912ed29a9398aadcc2034fc7b60e044c99d`
- Byte count: `99233`
- Task/source-manifest publication commit: `def8985155db6329e42d480cc8c728ebbfa4d4f5`
- Official M1 source commit: `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`
- Source manifest SHA-256 recomputed from `git show` raw bytes: `6e3a90678ceba60b4cf20b2aef7c0834394243a30b0075457fcfff056576b38c`
- Result schema SHA-256 recomputed from `git show` raw bytes: `e325db19331dad718589d67dbe20ceabe1f8be774e765678bfdbc1d4c41e619b`
- The current draft `evidence_manifest.json` passed Draft 2020-12 validation against that pinned result schema at `2026-10-12T08:51:48Z` (0 validation errors). The manifest is validated again after final edits.

The M1 source receipt at the pinned source commit states 10/10 source and
companion files had exact-byte remote readback. This session checked the
receipt and its pinned source identity; it did not independently re-download
and hash all ten source blobs or access the official Library.

## Windows and local Git observations

- Host: `FoxLe-PC`
- Git: `2.56.0.windows.1`
- Python: `3.13.15`
- Node/npm: not installed or not on PATH
- Initial local branch/HEAD: `main` /
  `6662d5b61770291db4e493c0852fbc2f3b923a7b`
- Initial worktree: clean; one worktree; no merge or rebase in progress
- Report directory before recovery: absent
- Configured commit identity: `Copilot`
  (`223556219+Copilot@users.noreply.github.com`); this is Git configuration,
  not independent identity-provider verification.
- After fetching the designated report branch, it was at the pinned task
  commit and the worktree was clean on that branch.

## Remote access and write probe

- `git ls-remote origin refs/heads/work/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY-copilot`
  returned `def8985155db6329e42d480cc8c728ebbfa4d4f5`.
- `git push --dry-run origin
  def8985155db6329e42d480cc8c728ebbfa4d4f5:refs/heads/work/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY-copilot`
  returned `Everything up-to-date` with exit code 0. Because no ref update was
  pending, this did not prove permission to update a ref; only the subsequent
  actual report push can establish that technical capability.
- The task manifest designates this branch for the Copilot result. No
  competing local worktree or report commit was observed. GitHub does not
  expose a server-side exclusive-writer lease in the checks performed here.

No original P1 logs, test outputs, screenshots, raw DNSE data, or additional
P1 evidence files were found or reconstructed.
