"""Fixed FOX2 paths and containment checks for Bridge-controlled files."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from .errors import PathInvalid

PROJECT_ROOT = Path(r"C:\Projects\FOX2")
BRIDGE_ROOT = Path(r"C:\Projects\FOX2-AgentBridge")
WORKTREE_ROOT = Path(r"C:\Projects\FOX2-worktrees")


def canonical(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def is_within(path: Path, root: Path) -> bool:
    resolved_path = canonical(path)
    resolved_root = canonical(root)
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError:
        return False
    return True


def validate_path(
    path: Path,
    *,
    allowed_roots: Iterable[Path],
    label: str,
) -> Path:
    if not path.is_absolute():
        raise PathInvalid(f"{label} must be an absolute path")
    resolved = canonical(path)
    if not any(is_within(resolved, root) for root in allowed_roots):
        raise PathInvalid(f"{label} resolves outside its allowed roots")
    if os.name == "nt" and resolved.drive.lower() not in {
        canonical(root).drive.lower() for root in allowed_roots
    }:
        raise PathInvalid(f"{label} resolves to an unexpected drive")
    return resolved
