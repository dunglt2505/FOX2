"""FOX2 G3: produce an OFFLINE AppLocker baseline CANDIDATE, never install it.

The explicit candidate allow-manifest requires the original SAME-host XML
snapshot SHA-256 plus Exe/Script allow path arrays, with no inferred default
rules. Rule-path ACL/coverage review and negative host trials remain G3 gates.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from fox2_agent_bridge.f1_host_baseline import build_host_baseline_candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-snapshot", type=Path, required=True)
    parser.add_argument("--effective-snapshot", type=Path, required=True)
    parser.add_argument("--allow-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    output = args.output
    summary_path = output.with_suffix(".review.json")
    if output.suffix.lower() != ".xml":
        parser.error("candidate output must have .xml extension")
    if output.exists() or summary_path.exists():
        parser.error("STOP: output already exists; never overwrite prior candidate")
    if not output.parent.is_dir():
        parser.error("output parent directory must already exist")

    proposal = json.loads(args.allow_manifest.read_text(encoding="utf-8"))
    content, summary = build_host_baseline_candidate(
        args.local_snapshot.read_bytes(), args.effective_snapshot.read_bytes(),
        proposal
    )
    try:
        with output.open("xb") as handle:
            handle.write(content)
        with summary_path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(summary, handle, sort_keys=True, indent=2)
            handle.write("\n")
    except Exception:
        if not summary_path.exists() and output.exists():
            output.unlink()
        raise
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
