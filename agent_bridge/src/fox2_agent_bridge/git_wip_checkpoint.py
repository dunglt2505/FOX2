"""Opt-in, fail-closed WIP checkpoint using existing Bridge Git subprocess.

This is NOT an Agent callback or an automatic error handler. It requires
independent immutable grant verification and actual child-tree quiescence
attestation from the installed host. Both default unavailable.
It preserves task HEAD/index and failed consumed Dispatch state.
"""
from __future__ import annotations

import hashlib
import json
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any

from .errors import WorkspaceBlocked
from .git_delivery_guard import _safe_relative, validate_staged_blobs, validate_committed_result

_SHA = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_REF = re.compile(r"work/FOX2-[A-Za-z0-9/_-]{4,160}\Z")
_ID = re.compile(r"FOX2-[A-Za-z0-9_-]{4,120}\Z")


@dataclass(frozen=True)
class WipGrant:
    dispatch_id: str
    execution_id: str
    wp_id: str
    task_branch: str
    recovery_branch: str
    before_head: str
    payload_sha256: str
    grant_source_sha: str
    grant_sha256: str
    changed_paths: tuple[str, ...]
    report_path: str
    test_status: str
    failure_kind: str

    def validate(self) -> None:
        fields = (self.dispatch_id, self.execution_id, self.wp_id,
                  self.task_branch, self.recovery_branch)
        if not all(isinstance(s, str) and _ID.fullmatch(s) for s in fields[:3]):
            raise WorkspaceBlocked("invalid WIP task/attempt identity")
        if not all(isinstance(s, str) and _REF.fullmatch(s) for s in fields[3:]):
            raise WorkspaceBlocked("WIP ref must be explicit non-protected FOX2 branch")
        if ("-WIP-" not in self.recovery_branch or
                self.recovery_branch == self.task_branch or
                self.recovery_branch.endswith("/") or
                ".." in self.recovery_branch):
            raise WorkspaceBlocked("recovery must use a separate WIP-only ref")
        if not (_SHA.fullmatch(self.before_head) and
                _SHA.fullmatch(self.grant_source_sha) and
                _SHA256.fullmatch(self.payload_sha256) and
                _SHA256.fullmatch(self.grant_sha256)):
            raise WorkspaceBlocked("missing immutable WIP grant/source pins")
        if (not isinstance(self.changed_paths, tuple) or
                not 1 <= len(self.changed_paths) <= 200 or
                len(self.changed_paths) != len(set(self.changed_paths))):
            raise WorkspaceBlocked("WIP paths must be bounded and unique")
        for path in self.changed_paths:
            _safe_relative(path)
        _safe_relative(self.report_path)
        if (not self.report_path.startswith(f"reports/{self.wp_id}/") or
                not self.report_path.endswith("/wip_incomplete.json") or
                self.report_path in self.changed_paths):
            raise WorkspaceBlocked("WIP manifest must have its own bounded report path")
        if self.test_status not in {"FAIL", "NOT_RUN", "UNKNOWN"}:
            raise WorkspaceBlocked("WIP cannot claim a passing test gate")
        if (self.failure_kind not in
                {"NONZERO", "QUOTA", "TIMEOUT", "INTERRUPT", "CRASH", "UNKNOWN"}):
            raise WorkspaceBlocked("WIP failure kind missing")

    def digest(self) -> str:
        data = json.dumps({
            "dispatch": self.dispatch_id, "execution": self.execution_id,
            "wp": self.wp_id, "task": self.task_branch,
            "recovery": self.recovery_branch, "base": self.before_head,
            "payload": self.payload_sha256, "grant_source": self.grant_source_sha,
            "grant_hash": self.grant_sha256, "paths": self.changed_paths,
            "report": self.report_path, "test": self.test_status,
            "error": self.failure_kind,
        }, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(data).hexdigest()


def _one_ref(runner, branch: str) -> str | None:
    result = runner._git(
        ["ls-remote", "--refs", "origin", f"refs/heads/{branch}"])
    rows = [x.split("\t", 1) for x in result.stdout.splitlines() if x.strip()]
    if not rows:
        return None
    if (len(rows) != 1 or len(rows[0]) != 2 or
            rows[0][1] != f"refs/heads/{branch}" or
            not _SHA.fullmatch(rows[0][0])):
        raise WorkspaceBlocked("ambiguous WIP remote ref readback")
    return rows[0][0]


def publish_wip_checkpoint(
    runner: Any, *, grant: WipGrant,
    authority_verifier: Callable[[WipGrant], bool] | None = None,
    quiescence_verifier: Callable[[str], bool] | None = None,
) -> dict[str, object]:
    """Publisher callable only after original failed attempt and external grants.

    No success result ref, never changes main worktree HEAD or its index.
    A retry reuses the stored commit, never manufactures another commit.
    """
    if not isinstance(grant, WipGrant):
        raise WorkspaceBlocked("WIP requires typed immutable grant")
    grant.validate()
    if (authority_verifier is None or
            authority_verifier(grant) is not True):
        raise WorkspaceBlocked("independent recovery-source permission not verified")
    if (quiescence_verifier is None or
            quiescence_verifier(grant.execution_id) is not True):
        raise WorkspaceBlocked("Agent and child writer quiescence not verified")
    row = runner.ledger.dispatch_status(grant.dispatch_id)
    if (row is None or row["execution_id"] != grant.execution_id or
            row["dispatch_state"] != "NEEDS_RECONCILIATION" or
            row["execution_state"] not in ("NEEDS_RECONCILIATION", "RUNNING") or
            row["payload_hash"] != grant.payload_sha256):
        raise WorkspaceBlocked("WIP original consumed failed Dispatch not proved")
    context = row.get("checkpoint") or {}
    payload = context.get("payload") or {}
    if (payload.get("delivery_owner") != "BRIDGE" or
            payload.get("wp_id") != grant.wp_id or
            payload.get("branch") != grant.task_branch or
            context.get("before_head") != grant.before_head or
            row.get("result") is None or
            not isinstance(payload.get("worktree"), str)):
        raise WorkspaceBlocked("WIP task/source/owner checkpoint mismatch")
    worktree = Path(payload["worktree"])
    if runner._git(["-C", str(worktree), "branch", "--show-current"]).stdout.strip() != grant.task_branch:
        raise WorkspaceBlocked("WIP original task branch drift")
    if runner._git(["-C", str(worktree), "rev-parse", "HEAD"]).stdout.strip() != grant.before_head:
        raise WorkspaceBlocked("WIP original task HEAD drift")
    if _one_ref(runner, grant.task_branch) != grant.before_head:
        raise WorkspaceBlocked("WIP original remote task branch drift")
    existing = runner.ledger.wip_intent(grant.execution_id)
    intent = grant.digest()
    if existing is not None:
        if (existing["intent_sha256"] != intent or
                existing["before_head"] != grant.before_head or
                existing["recovery_ref"] != grant.recovery_branch):
            raise WorkspaceBlocked("recovery already has a different durable intent")
        after = str(existing["commit_sha"])
        changes = tuple(grant.changed_paths) + (grant.report_path,)
        validate_committed_result(
            runner._git, worktree, grant.before_head, after, changes)
    else:
        if _one_ref(runner, grant.recovery_branch) is not None:
            raise WorkspaceBlocked("recovery ref already exists; no overwrite")
        changed = runner._dirty_changed_paths(worktree)
        if changed != tuple(sorted(grant.changed_paths)):
            raise WorkspaceBlocked("WIP local changes differ from exact recovery grant")
        runner._verify_changed_paths(payload=payload, changed=changed)
        runner._git(["-C", str(worktree), "diff", "--check"])
        # Dedicated Git index: never commit/stage in the task's real index.
        with tempfile.TemporaryDirectory(prefix="fox2-wip-") as tmp:
            index = str(Path(tmp) / "checkpoint.index")
            env = {"GIT_INDEX_FILE": index}
            def git_index(args, *, binary=False):
                return runner._git(args, binary=binary, extra_env=env)
            git_index(["-C", str(worktree), "read-tree", grant.before_head])
            git_index(["-C", str(worktree), "add", "-A", "--", *changed])
            git_index(["-C", str(worktree), "diff", "--cached", "--check"])
            validate_staged_blobs(git_index, worktree, changed)
            manifest = {
                "schema": "FOX2_GIT_WIP_INCOMPLETE_1",
                "status": "WIP_INCOMPLETE",
                "publisher": "BRIDGE",
                "acceptance": "NOT_ACCEPTED",
                "dispatch_id": grant.dispatch_id,
                "execution_id": grant.execution_id,
                "logical_task_id": grant.wp_id,
                "original_task_branch": grant.task_branch,
                "recovery_ref": grant.recovery_branch,
                "before_head": grant.before_head,
                "source_grant_commit": grant.grant_source_sha,
                "source_grant_sha256": grant.grant_sha256,
                "test_status": grant.test_status,
                "error_kind": grant.failure_kind,
                "changed_paths": list(changed),
                "agent_and_child_writer": "QUIESCENCE_VERIFIED_BY_HOST_CALLBACK",
                "final_result": "NOT_PUBLISHED",
                "next_safe_action": "CHAT_REVIEW_AND_NEW_AUTHORIZED_ATTEMPT",
            }
            report = Path(tmp) / "wip.json"
            report.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n",
                              encoding="utf-8")
            blob = git_index(
                ["-C", str(worktree), "hash-object", "-w", str(report)]
            ).stdout.strip()
            if not _SHA.fullmatch(blob):
                raise WorkspaceBlocked("invalid WIP report blob")
            git_index(["-C", str(worktree), "update-index", "--add", "--cacheinfo",
                       f"100644,{blob},{grant.report_path}"])
            tree = git_index(["-C", str(worktree), "write-tree"]).stdout.strip()
            if not _SHA.fullmatch(tree):
                raise WorkspaceBlocked("invalid WIP tree")
            after = runner._git([
                "-C", str(worktree), "-c", "user.name=FOX2 Bridge",
                "-c", "user.email=fox2-bridge@local.invalid",
                "commit-tree", tree, "-p", grant.before_head,
                "-m", f"FOX2 WIP_INCOMPLETE {grant.dispatch_id} {grant.execution_id}",
            ]).stdout.strip()
            if not _SHA.fullmatch(after):
                raise WorkspaceBlocked("invalid WIP commit identity")
            validate_committed_result(
                runner._git, worktree, grant.before_head, after,
                changed + (grant.report_path,))
        # The durable intent MUST precede any network side effect.
        runner.ledger.prepare_wip_intent(
            dispatch_id=grant.dispatch_id, execution_id=grant.execution_id,
            intent_sha256=intent, recovery_ref=grant.recovery_branch,
            before_head=grant.before_head, commit_sha=after)
    remote = _one_ref(runner, grant.recovery_branch)
    if remote is None:
        runner._git(["-C", str(worktree), "push", "origin",
                     f"{after}:refs/heads/{grant.recovery_branch}"])
        remote = _one_ref(runner, grant.recovery_branch)
    if remote != after:
        raise WorkspaceBlocked("WIP Git remote conflicts with exact immutable commit")
    runner.ledger.verify_wip_remote(
        execution_id=grant.execution_id, intent_sha256=intent,
        expected_sha=after, observed_sha=remote)
    return {
        "status": "WIP_INCOMPLETE",
        "publisher": "BRIDGE", "acceptance": "NOT_ACCEPTED",
        "execution_id": grant.execution_id,
        "recovery_ref": grant.recovery_branch,
        "remote_commit_sha": remote,
        "test_status": grant.test_status,
        "next_safe_action": "CHAT_REVIEW_NEW_AUTHORIZED_ATTEMPT",
    }
