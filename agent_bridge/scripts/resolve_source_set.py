"""Produce an immutable Git-first source/prompt binding from the authoritative Dictionary.

The caller must FIRST verify Registry/release authority for --dictionary-commit.
This command does not choose a latest version, issue Dispatch or launch an Agent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from fox2_agent_bridge.source_set import (
    SourceSetError, bind_git_first_handoff, git_reader, resolve_source_set,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path,
                        default=Path(__file__).resolve().parents[2])
    parser.add_argument("--dictionary-commit", required=True,
                        help="Immutable commit selected through independently verified Registry")
    parser.add_argument("--dictionary-path", required=True,
                        help="Exact Dictionary path asserted by the authorized source registry")
    parser.add_argument("--dictionary-sha256", required=True,
                        help="Expected SHA-256 from the trusted Dictionary binding")
    parser.add_argument("--source-commit", required=True,
                        help="Immutable snapshot commit to use for BRD/Tech/other documents")
    parser.add_argument("--key", action="append", default=[],
                        help="Dictionary current key, e.g. brds.BRD-00 (repeatable)")
    parser.add_argument("--owner-candidate-override-ref",
                        help="Exact bounded Owner authority reference; NOT independent proof")
    parser.add_argument("--task-commit")
    parser.add_argument("--task-path")
    parser.add_argument("--prompt-commit")
    parser.add_argument("--prompt-path")
    parser.add_argument("--output", type=Path,
                        help="Write a new source-set file; refuses overwrite")
    args = parser.parse_args(argv)
    read, blob_sha = git_reader(args.repo_root)
    try:
        raw = read(args.dictionary_commit, args.dictionary_path)
        snapshot = resolve_source_set(
            raw, dictionary_path=args.dictionary_path,
            dictionary_commit=args.dictionary_commit,
            dictionary_sha256=args.dictionary_sha256,
            source_commit=args.source_commit,
            read_blob=read, include_keys=tuple(args.key),
            owner_candidate_override_ref=args.owner_candidate_override_ref,
        )
        given = (args.task_commit, args.task_path,
                 args.prompt_commit, args.prompt_path)
        if any(given) and not all(given):
            raise SourceSetError("Git-first handoff requires BOTH pinned task and prompt refs")
        if all(given):
            snapshot = bind_git_first_handoff(
                snapshot, task_commit=args.task_commit, task_path=args.task_path,
                prompt_commit=args.prompt_commit, prompt_path=args.prompt_path,
                read_blob=read, blob_sha=blob_sha,
            )
        output = json.dumps(snapshot, sort_keys=True, indent=2,
                            ensure_ascii=False).encode("utf-8") + b"\n"
        if args.output:
            # No changing an earlier frozen source lock.
            with args.output.open("xb") as handle:
                handle.write(output)
        else:
            print(output.decode("utf-8"), end="")
    except (SourceSetError, FileExistsError, OSError) as exc:
        parser.exit(2, f"SOURCE_SET_BLOCKED: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
