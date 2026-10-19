"""Dictionary-first selection and Git-first prompt binding regressions.

Synthetic future versions intentionally prove no version/path allowlist is needed.
No Git writes, Bridge execution, or network operations.
"""
import hashlib
import json
import re

import pytest

from fox2_agent_bridge.source_set import (
    SourceSetError, bind_git_first_handoff, resolve_source_set,
)
from fox2_agent_bridge.dispatch_schema_v3_contract import DISPATCH_SCHEMA_V3


DICT_SHA = "a" * 40
SNAPSHOT_SHA = "b" * 40
TASK_SHA = "c" * 40
PROMPT_SHA = "d" * 40
DIC_PATH = "docs/governance/FOX2_PROJECT_DICTIONARY_v9.4.json"
POLICY_PATH = "docs/governance/FOX2_POLICY_V92.0.md"
BRD_PATH = "docs/brd_mirror/FOX2-BRD-00_v31.2.md"
SPEC_PATH = "docs/architecture/FOX2_M1_TECHNICAL_SPEC_v56.md"
PROMPT_PATH = "docs/agent_handoff/FOX2-WP/codex_prompt.md"
TASK_PATH = "docs/agent_handoff/FOX2-WP/task.md"


def _json(value):
    return json.dumps(value, sort_keys=True).encode("utf-8")


def fixture():
    dictionary = {
        "dictionary_id": "FOX2_PROJECT_DICTIONARY",
        "dictionary_version": "9.4",
        "status": "RELEASED_EFFECTIVE",
        "project": {"id": "FOX2"},
        "current": {
            "policy": {"version": "92.0", "path": POLICY_PATH},
            "brds": {
                "BRD-00": {"version": "31.2", "status": "RELEASED_EFFECTIVE",
                           "path": BRD_PATH},
                "BRD-09": {"version": "44.4", "status": "CANDIDATE",
                           "path": "docs/brd_mirror/FOX2-BRD-09_v44.4.md"},
            },
            "technical_specs": {
                "m1": {"version": "56", "status": "RELEASED_EFFECTIVE",
                       "path": SPEC_PATH, "registry_binding_path":
                       "docs/architecture/FOX2_M1_TECH_BINDING_v88.md"},
            },
        },
    }
    payloads = {
        (SNAPSHOT_SHA, POLICY_PATH): b"policy 92",
        (SNAPSHOT_SHA, BRD_PATH): b"brd 31.2",
        (SNAPSHOT_SHA, SPEC_PATH): b"tech 56",
        (SNAPSHOT_SHA, "docs/architecture/FOX2_M1_TECH_BINDING_v88.md"): b"binding",
        (SNAPSHOT_SHA, "docs/brd_mirror/FOX2-BRD-09_v44.4.md"): b"candidate",
        (TASK_SHA, TASK_PATH): b"task",
        (PROMPT_SHA, PROMPT_PATH): b"prompt already committed",
    }

    def read(commit, path):
        if (commit, path) not in payloads:
            raise SourceSetError("not in immutable Git snapshot")
        return payloads[(commit, path)]

    raw = _json(dictionary)
    kwargs = dict(dictionary_bytes=raw, dictionary_path=DIC_PATH,
                  dictionary_commit=DICT_SHA,
                  dictionary_sha256=hashlib.sha256(raw).hexdigest(),
                  source_commit=SNAPSHOT_SHA, read_blob=read)
    return kwargs, read, dictionary


def test_resolves_future_versions_from_dictionary_with_no_hardcoded_allowlist():
    kwargs, _, _ = fixture()
    source = resolve_source_set(**kwargs)
    assert source["dictionary"]["version"] == "9.4"
    assert source["documents"]["policy"]["version"] == "92.0"
    assert source["documents"]["brds.BRD-00"]["version"] == "31.2"
    assert source["documents"]["technical_specs.m1"]["path"] == SPEC_PATH
    assert source["documents"]["technical_specs.m1.registry_binding_path"]["sha256"]
    assert source["excluded_candidate_keys"] == ["brds.BRD-09"]
    assert source["authority"]["independent_authority_verified"] is False
    assert source["source_commit"] == SNAPSHOT_SHA


def test_rejects_dictionary_bytes_drift_even_at_same_commit():
    kwargs, _, _ = fixture()
    kwargs["dictionary_sha256"] = "f" * 64
    with pytest.raises(SourceSetError, match="SHA-256 mismatch"):
        resolve_source_set(**kwargs)


def test_does_not_choose_candidate_dictionary_or_candidate_brd_automatically():
    kwargs, _, dictionary = fixture()
    dictionary["status"] = "OWNER_APPROVED_MIGRATION_CANDIDATE"
    raw = _json(dictionary)
    kwargs["dictionary_bytes"] = raw
    kwargs["dictionary_sha256"] = hashlib.sha256(raw).hexdigest()
    with pytest.raises(SourceSetError, match="not released"):
        resolve_source_set(**kwargs)
    kwargs["owner_candidate_override_ref"] = "Owner:2026-10-19:scope"
    source = resolve_source_set(**kwargs)
    assert "brds.BRD-09" not in source["documents"]
    assert "brds.BRD-09" in source["excluded_candidate_keys"]


def test_candidate_brd_requires_explicit_key_and_owner_ref():
    kwargs, _, _ = fixture()
    kwargs["include_keys"] = ("brds.BRD-09",)
    with pytest.raises(SourceSetError, match="candidate"):
        resolve_source_set(**kwargs)
    kwargs["owner_candidate_override_ref"] = "Owner:2026-10-19:scope"
    source = resolve_source_set(**kwargs)
    assert source["documents"]["brds.BRD-09"]["status"] == "CANDIDATE"
    assert source["authority"]["independent_authority_verified"] is False


@pytest.mark.parametrize("path", [
    "docs/governance/../escape.md",
    "/tmp/unsafe.json",
    "docs/governance/FOX2\\POLICY.md",
    "docs//governance/file.md",
])
def test_rejects_unsafe_future_dictionary_paths(path):
    kwargs, _, dictionary = fixture()
    dictionary["current"]["policy"]["path"] = path
    kwargs["dictionary_bytes"] = _json(dictionary)
    kwargs["dictionary_sha256"] = hashlib.sha256(kwargs["dictionary_bytes"]).hexdigest()
    with pytest.raises(SourceSetError, match="unsafe"):
        resolve_source_set(**kwargs)


def test_source_missing_at_bound_commit_fails_closed():
    kwargs, _, _ = fixture()
    kwargs["source_commit"] = "e" * 40
    with pytest.raises(SourceSetError):
        resolve_source_set(**kwargs)


def test_missing_git_prompt_or_bad_task_path_never_generates_final_handoff():
    kwargs, read, _ = fixture()
    source = resolve_source_set(**kwargs)
    with pytest.raises(SourceSetError):
        bind_git_first_handoff(
            source, task_commit=TASK_SHA, task_path=TASK_PATH,
            prompt_commit=PROMPT_SHA, prompt_path="docs/agent_handoff/FOX2-WP/missing.md",
            read_blob=read, blob_sha=lambda *_: "1" * 40)
    with pytest.raises(SourceSetError, match="task.md"):
        bind_git_first_handoff(
            source, task_commit=TASK_SHA, task_path=PROMPT_PATH,
            prompt_commit=PROMPT_SHA, prompt_path=PROMPT_PATH,
            read_blob=read, blob_sha=lambda *_: "1" * 40)


def test_git_first_manifest_binds_exact_prompt_and_task_not_an_executable_dispatch():
    kwargs, read, _ = fixture()
    source = resolve_source_set(**kwargs)
    handoff = bind_git_first_handoff(
        source, task_commit=TASK_SHA, task_path=TASK_PATH,
        prompt_commit=PROMPT_SHA, prompt_path=PROMPT_PATH,
        read_blob=read, blob_sha=lambda *_: "1" * 40)
    assert handoff["prompt"] == {
        "path": PROMPT_PATH, "git_commit": PROMPT_SHA, "git_blob_sha1": "1" * 40,
        "sha256": hashlib.sha256(b"prompt already committed").hexdigest(),
    }
    assert handoff["task"]["sha256"] == hashlib.sha256(b"task").hexdigest()
    assert handoff["handoff_status"] == "SOURCE_BOUND_NOT_EXECUTABLE"


def test_schema_never_lists_dictionary_filenames_and_keeps_runtime_exact_check():
    git_path = DISPATCH_SCHEMA_V3["properties"]["dictionary"]["properties"]["git_path"]
    assert "enum" not in git_path and "const" not in git_path
    assert re.fullmatch(git_path["pattern"], DIC_PATH)
    assert not re.fullmatch(git_path["pattern"], "docs/untrusted/custom.json")
    assert not re.fullmatch(git_path["pattern"], "docs/governance/../evil.json")
