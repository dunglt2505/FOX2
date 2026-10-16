"""Shared fail-closed services. Trust input is supplied by the owning host."""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict
from pathlib import Path
from .errors import SourceError


class Hold(SourceError):
    def __init__(self, status, reason):
        self.status = status
        super().__init__(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def preflight(operation, grants, bindings, required):
    if operation not in grants:
        raise Hold("BLOCKED", "Operation lacks scoped grant")
    for family in required:
        if bindings.get(family, {}).get("status") != "VERIFIED_EFFECTIVE":
            raise Hold("UNVERIFIED", "Required source: " + family)
    return {"status": "PERMIT", "operation": operation}


class TaskStore:
    """Exclusive creation prevents concurrent task starts; existing locks never change."""
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def start(self, task, bindings):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", task):
            raise Hold("BLOCKED", "Invalid task identity")
        path = self.root / (task + ".json")
        try:
            with path.open("x", encoding="utf-8") as out:
                json.dump({"task": task, "source_lock": bindings}, out, sort_keys=True)
        except FileExistsError as exc:
            raise Hold("BLOCKED", "Existing task: resume with frozen lock; no replay") from exc
        return json.loads(path.read_text(encoding="utf-8"))

    def resume(self, task):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", task):
            raise Hold("BLOCKED", "Invalid task identity")
        return json.loads((self.root / (task + ".json")).read_text(encoding="utf-8"))


def assess_drift(locked, proposed, required):
    changed = sorted(k for k in required if locked.get(k) != proposed.get(k))
    return {"status": "IMPACT_ASSESSMENT_REQUIRED" if changed else "RETAIN_LOCK",
            "changed_families": changed, "source_lock": locked}


def verify_evidence(root, receipts):
    root = Path(root).resolve()
    if not receipts:
        raise Hold("UNVERIFIED", "Evidence absent")
    for receipt in receipts:
        path = (root / receipt["path"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise Hold("UNVERIFIED", "Evidence path outside root or absent")
        if digest(path.read_bytes()) != receipt["sha256"]:
            raise Hold("UNVERIFIED", "Evidence hash mismatch")
    return {"status": "READBACK_VERIFIED", "count": len(receipts)}
