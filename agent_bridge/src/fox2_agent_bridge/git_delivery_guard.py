"""Bridge-owned Git delivery safety gates (shared by normal and recovery paths).

Pure validation on staged *Git blobs*, not an Agent self-report. Publication and
ledger intent remain owned by the single existing BridgeE2ERunner worker.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Any

from .errors import WorkspaceBlocked

_SECRET_BYTES = (
    re.compile(rb"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(rb"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    re.compile(rb"(?i)Bearer[ \t]+[A-Za-z0-9._~+/-]{20,}"),
    re.compile(rb"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
)
_FORBIDDEN_NAMES = (".env", ".env.", "id_rsa", "id_ed25519",
                    "credentials.json", "service-account.json")
_MAX_BLOB_BYTES = 8_000_000


def _safe_relative(path: str) -> None:
    """Reject suspicious Git paths even when a broad path glob accepts them."""
    if (not isinstance(path, str) or not path or "\x00" in path or
            "\\" in path or ":" in path or path.startswith("/") or
            any(segment in ("", ".", "..", ".git") for segment in path.split("/"))):
        raise WorkspaceBlocked("unsafe staged Git path")
    low = path.casefold()
    if any(part == low.rsplit("/", 1)[-1] or
           (part.endswith(".") and low.rsplit("/", 1)[-1].startswith(part))
           for part in _FORBIDDEN_NAMES):
        raise WorkspaceBlocked("credential-like file path cannot be published")


def validate_staged_blobs(
    git: Callable[..., Any], worktree: Path, changed: tuple[str, ...]
) -> None:
    """Fail closed on index drift, symlinks/gitlinks, unsafe names or secrets."""
    for path in changed:
        _safe_relative(path)
    raw = git(["-C", str(worktree), "diff", "--cached", "--name-only", "-z"],
              binary=True).stdout
    try:
        index_paths = [piece.decode("utf-8") for piece in raw.split(b"\x00") if piece]
    except UnicodeDecodeError as exc:
        raise WorkspaceBlocked("staged Git path encoding unavailable") from exc
    if len(index_paths) != len(changed) or set(index_paths) != set(changed):
        raise WorkspaceBlocked("staged Git index differs from exact allowed changes")
    for path in changed:
        info = git(["-C", str(worktree), "ls-files", "--stage", "-z", "--", path],
                   binary=True).stdout
        if not info:
            # A tracked deletion has no indexed blob. Still requires scoped path.
            if (worktree / Path(*path.split("/"))).exists():
                raise WorkspaceBlocked("staged path has no indexed entry")
            continue
        records = [record for record in info.split(b"\x00") if record]
        if len(records) != 1:
            raise WorkspaceBlocked("ambiguous staged file identity")
        try:
            meta, name = records[0].split(b"\t", 1)
        except ValueError as exc:
            raise WorkspaceBlocked("invalid staged Git entry") from exc
        if name.decode("utf-8", "strict") != path or meta.split(b" ", 1)[0] not in (
                b"100644", b"100755"):
            raise WorkspaceBlocked("non-regular staged file or path mismatch")
        item = worktree / Path(*path.split("/"))
        root = worktree.resolve(strict=True)
        cursor = item
        while cursor != worktree:
            if cursor.is_symlink() or (hasattr(cursor, "is_junction") and cursor.is_junction()):
                raise WorkspaceBlocked("symlink/reparse path cannot be published")
            cursor = cursor.parent
        try:
            item.resolve(strict=True).relative_to(root)
        except (OSError, ValueError) as exc:
            raise WorkspaceBlocked("staged file escaped or vanished from worktree") from exc
        blob = git(["-C", str(worktree), "show", ":" + path], binary=True).stdout
        if not isinstance(blob, bytes) or len(blob) > _MAX_BLOB_BYTES:
            raise WorkspaceBlocked("staged blob exceeds bounded secret scan")
        if any(pattern.search(blob) for pattern in _SECRET_BYTES):
            raise WorkspaceBlocked("possible secret detected in staged content")


def validate_committed_result(
    git: Callable[..., Any], worktree: Path, before_head: str,
    commit_sha: str, paths: tuple[str, ...],
) -> None:
    """Read the EXACT persisted commit tree before any resumed network push."""
    import re as _re
    if not (_re.fullmatch(r"[0-9a-f]{40}", before_head) and
            _re.fullmatch(r"[0-9a-f]{40}", commit_sha)):
        raise WorkspaceBlocked("invalid immutable publication identities")
    if not paths:
        raise WorkspaceBlocked("empty committed result cannot be published")
    for path in paths:
        _safe_relative(path)
        raw = git(["-C", str(worktree), "ls-tree", "-z", commit_sha, "--", path],
                  binary=True).stdout
        if not raw:
            # Deletion: the path must not exist in the new commit.
            continue
        entries = [x for x in raw.split(b"\x00") if x]
        if len(entries) != 1:
            raise WorkspaceBlocked("ambiguous committed file identity")
        try:
            meta, name = entries[0].split(b"\t", 1)
        except ValueError as exc:
            raise WorkspaceBlocked("invalid committed tree entry") from exc
        if (name.decode("utf-8", "strict") != path or
                meta.split(b" ", 1)[0] not in (b"100644", b"100755") or
                b" blob " not in meta):
            raise WorkspaceBlocked("non-regular committed file or path mismatch")
        blob = git(["-C", str(worktree), "show", f"{commit_sha}:{path}"],
                   binary=True).stdout
        if not isinstance(blob, bytes) or len(blob) > _MAX_BLOB_BYTES:
            raise WorkspaceBlocked("committed blob exceeds bounded secret scan")
        if any(pattern.search(blob) for pattern in _SECRET_BYTES):
            raise WorkspaceBlocked("possible secret detected in committed content")
