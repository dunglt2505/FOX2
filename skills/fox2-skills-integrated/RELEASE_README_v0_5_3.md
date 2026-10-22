# FOX2 Skills v0.5.3 — plugin transport hotfix

No behavioral change from v0.5.2.

## Reason

The v0.5.2 Git source and Board-promotion contract were correct, but cloud readback found a publication-transport byte defect in `skills/fox2-mgmt-delivery/SKILL.md`: one control character replaced the letter `o` in the sentence `CHAT owns result acceptance`.

The Plugin Creator also normalizes ordering in `.codex-plugin/plugin.json`; that semantic normalization is not treated as a behavior defect.

## Preserved behavior

The v0.5.2 Master Plan → Agile Board promotion contract remains unchanged:

- `OUTCOME_DEFINED`
- `DEPENDENCIES_KNOWN`
- `SOURCE_READY_ENOUGH`
- `ACCEPTANCE_ACTIONABLE`
- `NEXT_SAFE_ACTION_KNOWN`

and exactly one decision:

- `KEEP_IN_MASTER_PLAN`
- `PROMOTE_TO_BACKLOG`
- `PROMOTE_TO_DOING`
- `BLOCKED`

## Hotfix scope

- clean `fox2-mgmt-delivery/SKILL.md` bytes;
- bump plugin metadata to v0.5.3;
- refresh release metadata/hash inventory;
- no product code, Bridge runtime, broker/provider/LIVE, or task rebind.

v0.5.2 is superseded for plugin runtime by v0.5.3 because of the cloud byte defect. Git history remains immutable evidence.
