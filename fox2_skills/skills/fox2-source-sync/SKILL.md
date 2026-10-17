---
name: fox2-source-sync
description: Reconcile Git documents with destination copies, preserving conflicts and history.
---
# Synchronize an authorized file delta without losing WIP

- Inventory source and destination files and compare exact bytes. Classify each as missing, identical or conflicting; never infer equality from names.
- Produce a plan first. Execute only copies explicitly covered by the existing grant and allowed root; preserve unrelated or modified WIP.
- Read copied destination bytes back, record digests and distinguish identical retry from new copy. Stop the affected copy on conflict instead of overwriting.
- Technical comparison and authorized local copying may proceed under conditional provenance. Canonical-source replacement, external publication and Registry promotion need their own authority.
- Report copied, unchanged, conflicting and unverified paths without claiming a release.

Read [scope and source guidance](../../shared/host_guidance.md) when authority, canonical sources, task state or effects matter.
