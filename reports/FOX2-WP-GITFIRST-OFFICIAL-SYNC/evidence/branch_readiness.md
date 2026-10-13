# FOX2 branch/source readiness

| Branch | Observed full HEAD | Assessment / use |
|---|---|---|
| main | `f311c1fc5b2f37962b30d4af3d90cc8dc30bd8a8` | Historical V1.0/BRD00v0.2 only; no current M1/runtime; not a DEV source |
| work/FOX2-GITFIRST-BOOTSTRAP-chat-20261012 | `f311c1fc5b2f37962b30d4af3d90cc8dc30bd8a8` | Same as main; no task additions; do not take CHAT writer |
| work/FOX2-GITFIRST-SYNC-RECOVERY-001-work-20261012 | `bd44dc2bb2fa1ba43070ea1052764320a86507c3` | PR1 draft;3 ahead main;9 exact historical/current-at-that-time docs; no review; reuse immutable baseline only |
| work/FOX2-M0-MAIN-SOURCE-DOCS-20261011 | `f311c1fc5b2f37962b30d4af3d90cc8dc30bd8a8` | Same main commit;0 unique changes; writer/WIP not visible, preserve |
| work/FOX2-M0-SOURCE-MIRROR-20261011 | `60892265d752d773829139c50039f9d81530e849` | 1 behind main, ancestor incorporated; no unique source; historical, preserve |
| work/FOX2-GITFIRST-OFFICIAL-SYNC-work-20261012 | `c016bd56ba70415910aaf39e220b40db4f5e4a4c` (source/pilot checkpoint) | Current V1.3/v2 workflow source, partial M1 mirror; final submission HEAD is external pointer |

Five pre-existing branches enumerated to empty continuation; all protected=false. PR1 is draft/unmerged/no reviews. GitHub rulesets read returns403 with account-plan upgrade/public-repo message; no permission or branch protection change made. Ruleset result cannot be described as configured enforcement. No branch deletion/rename/merge/force update. No local Windows WIP assumption.

No source/runtime implementation on any tree: backend/frontend/tests/fixtures only .gitkeep. No workflows present in tree; action runs0. Do not call service READY from document sync. Gates: complete M1 Git source, independent CHAT review, separately scoped DEV/host/model/quota/worktree/contract writer grants; actual offline/provider-disabled startup/API/UI tests; then independent provider rights/semantics tests if authorized. Current assignment gives none of these runtime permissions.

BRD01–05/07 remain Candidate outside official tree; M1 authorized scope00/06/08 is narrower than full investment intelligence service. Design import is partial1/4 original images; optional visual references are not hard dependency or accepted production imagery. A larger Candidate roadmap0.4.1/0.4.2 never replaces released M1v0.4.
