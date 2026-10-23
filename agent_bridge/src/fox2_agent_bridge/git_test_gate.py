"""Required-test evidence supplied by the trusted Bridge host, never the Agent.

The host verifier runs its admitted test plan outside Agent token lifetime.
Unconfigured required tests fail closed. Neither Dispatch JSON nor stdout can
provide a verifier or manufacture evidence. No shell commands are inferred from
the human-readable required_tests strings.
"""
from __future__ import annotations

from pathlib import Path
import re

from .errors import WorkspaceBlocked


def verify_test_evidence(required, tree_sha: str, evidence) -> dict:
    if (not isinstance(required, (list, tuple)) or
            any(not isinstance(name, str) or not name for name in required) or
            len(set(required)) != len(required)):
        raise WorkspaceBlocked("invalid required test contract")
    if not re.fullmatch(r"[0-9a-f]{40}", tree_sha):
        raise WorkspaceBlocked("invalid tested Git tree identity")
    if not required:
        return {"tree_sha": tree_sha, "status": "NOT_REQUIRED", "results": {}}
    if (not isinstance(evidence, dict) or evidence.get("tree_sha") != tree_sha or
            not isinstance(evidence.get("results"), dict) or
            set(evidence["results"]) != set(required) or
            any(value != "PASS" for value in evidence["results"].values())):
        raise WorkspaceBlocked("required tests missing, failed or bound to a different tree")
    return {"tree_sha": tree_sha, "status": "PASS",
            "results": {name: "PASS" for name in required}}


def run_test_gate(git, worktree: Path, required, verifier=None) -> dict:
    tree = git(["-C", str(worktree), "write-tree"]).stdout.strip()
    evidence = None
    if required:
        if not callable(verifier):
            raise WorkspaceBlocked("required tests have no trusted Bridge host verifier")
        try:
            evidence = verifier(worktree, tree, tuple(required))
        except Exception as exc:
            raise WorkspaceBlocked("Bridge required-test verifier failed") from exc
    verified = verify_test_evidence(required, tree, evidence)
    # Tests must describe exactly what will be committed. Refuse a mutated
    # index, tracked bytes or new untracked outputs after the trusted test run.
    after = git(["-C", str(worktree), "write-tree"]).stdout.strip()
    unstaged = git(["-C", str(worktree), "diff", "--quiet"], check=False)
    untracked = git(["-C", str(worktree), "ls-files", "--others", "--exclude-standard", "-z"],
                    binary=True).stdout
    if after != tree or unstaged.returncode != 0 or untracked:
        raise WorkspaceBlocked("worktree changed during Bridge required tests")
    return verified
