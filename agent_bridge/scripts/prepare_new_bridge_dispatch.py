"""Prepare a NEW v3 Dispatch candidate with explicit BRIDGE delivery by default.

Input must be a complete, UNPUBLISHED v3 JSON draft; this tool neither issues nor
publishes a Dispatch and does not grant permission, source authority or replay.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from fox2_agent_bridge.dispatch_draft import prepare_new_dispatch_draft


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--new-draft", action="store_true", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--delivery-owner", choices=("BRIDGE", "AGENT"), default="BRIDGE")
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("STOP: cannot overwrite the immutable or original input")
    source = json.loads(args.input.read_text(encoding="utf-8"))
    candidate = prepare_new_dispatch_draft(source, delivery_owner=args.delivery_owner)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(candidate, output, sort_keys=True, indent=2)
        output.write("\n")
    print(json.dumps({
        "delivery_owner": candidate["delivery_owner"],
        "dispatch_id": candidate["dispatch_id"],
        "status": "UNPUBLISHED_DRAFT_ONLY",
        "git_delivery": "NOT_RUN",
        "old_dispatch_mutated": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
