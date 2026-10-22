# FOX2 — Project Kanban (single board)

**Operating rule:** FOX2 Policy v2.1.0 (Owner approved 2026-10-22)  
**Status:** SOURCE_CANDIDATE; not a claim of synchronized live project status.

| BACKLOG | DOING | BLOCKED | DONE |
| --- | --- | --- | --- |
| Prioritized tasks not started | Max 2 independent code writers, one owner per writable scope | Only genuinely blocked tasks, each with a concrete unblocker | Tested accepted outputs, linked result |

## Single task record

```yaml
id: FOX2-...
goal: "Observable outcome"
status: BACKLOG|DOING|BLOCKED|DONE
owner: CHAT|CODEX|COPILOT|WORK
scope: "Affected part and write boundaries"
done_when: "Measurable behavior/test"
result: "Link or commit (after delivery)"
blocker: null
```

Update this board from verified task results, not from number of documents/preflight PASSes. Fix normal defects in the same task. Review priority whenever needed; no compulsory ceremonies. Product milestones and genuinely protected release points stay in the roadmap, not as approval columns.
