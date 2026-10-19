"""Dictionary-first immutable handoff source selection.

The caller must supply an externally authorized Dictionary identity. This
module verifies bytes and emits an immutable source snapshot; it does NOT
decide Owner authority, promote candidates or execute Agents.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Callable

_SHA1 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_RELEASED = {"RELEASED_EFFECTIVE"}
_CANDIDATE = {"CANDIDATE", "OWNER_APPROVED_MIGRATION_CANDIDATE"}


class SourceSetError(ValueError):
    """A source or binding is unsafe, ambiguous or missing."""


def _sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _commit(value: str) -> str:
    if not isinstance(value, str) or not _SHA1.fullmatch(value):
        raise SourceSetError("an immutable 40-hex Git commit is required")
    return value


def _path(value: str, prefix: str = "docs/") -> str:
    if (not isinstance(value, str) or not value.startswith(prefix)
            or "\\" in value or any(part in {"", ".", ".."} for part in value.split("/"))
            or any(ord(char) < 32 for char in value)):
        raise SourceSetError("unsafe source path")
    return value


def git_reader(root: Path) -> tuple[Callable[[str, str], bytes],
                                    Callable[[str, str], str]]:
    """Always read commit:path, never branch tip, current workspace or latest filename."""
    def read(commit: str, path: str) -> bytes:
        cmd = ["git", "-C", str(root), "show", f"{_commit(commit)}:{_path(path)}"]
        proc = subprocess.run(cmd, capture_output=True, check=False)
        if proc.returncode:
            raise SourceSetError("immutable source cannot be read")
        return proc.stdout

    def blob_sha(commit: str, path: str) -> str:
        cmd = ["git", "-C", str(root), "rev-parse", f"{_commit(commit)}:{_path(path)}"]
        proc = subprocess.run(cmd, capture_output=True, check=False)
        if proc.returncode:
            raise SourceSetError("immutable Git blob identity unavailable")
        digest = proc.stdout.decode("ascii", errors="strict").strip()
        if not _SHA1.fullmatch(digest):
            raise SourceSetError("invalid Git blob identity")
        return digest

    return read, blob_sha


def _flatten(current: dict, prefix: str = "") -> dict[str, dict]:
    entries: dict[str, dict] = {}
    for key, value in current.items():
        identifier = f"{prefix}.{key}" if prefix else key
        if not isinstance(value, dict):
            raise SourceSetError("invalid Dictionary current entry")
        if "path" in value:
            _path(value["path"])
            if not isinstance(value.get("version"), str) or not value["version"]:
                raise SourceSetError(f"{identifier}: missing document version")
            entries[identifier] = value
        else:
            entries.update(_flatten(value, identifier))
    return entries


def resolve_source_set(
    dictionary_bytes: bytes, *, dictionary_path: str, dictionary_commit: str,
    dictionary_sha256: str, source_commit: str,
    read_blob: Callable[[str, str], bytes],
    include_keys: tuple[str, ...] = (),
    owner_candidate_override_ref: str | None = None,
) -> dict:
    """Resolve only Registry-selected documents from an explicitly bound Dictionary.

    Never interpret 'highest version' or a file's claimed EFFECTIVE as approval.
    Owner candidate ref records an exception claim; independent authority review
    is still necessary. Default excludes candidate BRD/Technical inputs.
    """
    _commit(dictionary_commit)
    _commit(source_commit)
    _path(dictionary_path, "docs/governance/")
    if not isinstance(dictionary_sha256, str) or not _SHA256.fullmatch(dictionary_sha256):
        raise SourceSetError("invalid expected Dictionary SHA-256")
    if _sha256(dictionary_bytes) != dictionary_sha256:
        raise SourceSetError("Dictionary source SHA-256 mismatch")
    try:
        dictionary = json.loads(dictionary_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SourceSetError("invalid Dictionary JSON") from exc
    if dictionary.get("dictionary_id") != "FOX2_PROJECT_DICTIONARY":
        raise SourceSetError("unsupported Dictionary identity")
    if dictionary.get("project", {}).get("id") != "FOX2":
        raise SourceSetError("Dictionary project mismatch")
    status = dictionary.get("status")
    if status not in _RELEASED and not owner_candidate_override_ref:
        raise SourceSetError("Dictionary is not released; explicit Owner candidate reference required")
    if owner_candidate_override_ref is not None:
        if not isinstance(owner_candidate_override_ref, str) or not owner_candidate_override_ref.strip():
            raise SourceSetError("empty Owner exception reference")
    records = _flatten(dictionary.get("current", {}))
    selected = set(include_keys) if include_keys else set(records)
    unknown = selected - set(records)
    if unknown:
        raise SourceSetError("unknown Dictionary key(s): " + ", ".join(sorted(unknown)))
    documents: dict[str, dict] = {}
    excluded: list[str] = []
    for key in sorted(selected):
        record = records[key]
        document_status = record.get("status")
        if document_status in _CANDIDATE:
            if include_keys and not owner_candidate_override_ref:
                raise SourceSetError(f"{key}: candidate requires bounded Owner reference")
            if not include_keys:
                excluded.append(key)
                continue
        path = _path(record["path"])
        content = read_blob(source_commit, path)
        if not isinstance(content, bytes):
            raise SourceSetError("source reader must return bytes")
        documents[key] = {
            "version": record["version"], "path": path,
            "git_commit": source_commit, "sha256": _sha256(content),
            "status": document_status or "UNSPECIFIED_IN_DICTIONARY",
        }
        for field in ("schema_path", "master_plan_path", "registry_binding_path"):
            if field in record:
                subpath = _path(record[field])
                subcontent = read_blob(source_commit, subpath)
                documents[key + "." + field] = {
                    "version": record["version"], "path": subpath,
                    "git_commit": source_commit, "sha256": _sha256(subcontent),
                    "status": document_status or "UNSPECIFIED_IN_DICTIONARY",
                }
    return {
        "schema": "FOX2_SOURCE_SET_V1",
        "source_selection": "DICTIONARY_FIRST_IMMUTABLE",
        "dictionary": {
            "version": dictionary.get("dictionary_version"), "path": dictionary_path,
            "git_commit": dictionary_commit, "sha256": dictionary_sha256,
            "status": status,
        },
        "authority": {
            "owner_candidate_override_ref": owner_candidate_override_ref,
            "independent_authority_verified": False,
            "status": "REQUIRES_GOVERNED_AUTHORITY_CHECK",
        },
        "source_commit": source_commit,
        "documents": documents,
        "excluded_candidate_keys": excluded,
    }


def bind_git_first_handoff(
    source_set: dict, *, task_commit: str, task_path: str,
    prompt_commit: str, prompt_path: str,
    read_blob: Callable[[str, str], bytes],
    blob_sha: Callable[[str, str], str],
) -> dict:
    """Bind prompt/task bytes already present in Git; never fabricate an Agent run."""
    if source_set.get("schema") != "FOX2_SOURCE_SET_V1":
        raise SourceSetError("unsupported source set")
    if not task_path.endswith("/task.md"):
        raise SourceSetError("task.md expected")
    _path(task_path, "docs/agent_handoff/")
    _path(prompt_path, "docs/agent_handoff/")
    _commit(task_commit)
    _commit(prompt_commit)
    task = read_blob(task_commit, task_path)
    prompt = read_blob(prompt_commit, prompt_path)
    if not task or not prompt:
        raise SourceSetError("empty Git task or prompt")
    prompt_blob_sha1 = blob_sha(prompt_commit, prompt_path)
    if not _SHA1.fullmatch(prompt_blob_sha1):
        raise SourceSetError("invalid prompt Git blob")
    return {
        **source_set,
        "task": {"path": task_path, "commit_sha": task_commit,
                 "sha256": _sha256(task)},
        "prompt": {"path": prompt_path, "git_commit": prompt_commit,
                   "git_blob_sha1": prompt_blob_sha1, "sha256": _sha256(prompt)},
        "handoff_status": "SOURCE_BOUND_NOT_EXECUTABLE",
    }
