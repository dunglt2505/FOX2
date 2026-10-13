"""Explicitly distinguish Git object bytes from working-tree bytes.

These helpers are preparatory only; BRG-030 defines the canonical validation
contract and must decide which byte source is authoritative.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum


class HashSource(StrEnum):
    GIT_BLOB_BYTES = "GIT_BLOB_BYTES"
    WORKING_TREE_BYTES = "WORKING_TREE_BYTES"


@dataclass(frozen=True)
class ContentHash:
    source: HashSource
    algorithm: str
    digest: str


def hash_git_blob_bytes(data: bytes, object_format: str = "sha1") -> ContentHash:
    header = f"blob {len(data)}\0".encode("ascii")
    digest = hashlib.new(object_format, header + data).hexdigest()
    return ContentHash(HashSource.GIT_BLOB_BYTES, object_format, digest)


def hash_working_tree_bytes(data: bytes) -> ContentHash:
    return ContentHash(HashSource.WORKING_TREE_BYTES, "sha256", hashlib.sha256(data).hexdigest())
