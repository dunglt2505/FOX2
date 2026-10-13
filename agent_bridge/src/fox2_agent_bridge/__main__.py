"""Command-line entry point for local Bridge health checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .app import BridgeApp
from .errors import BridgeError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fox2-bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)
    health = subparsers.add_parser("health", help="validate local Bridge core prerequisites")
    health.add_argument("--config", type=Path, help="optional TOML configuration file")
    poll = subparsers.add_parser("poll-once", help="read the FOX2 control branch once")
    poll.add_argument("--config", type=Path, help="optional TOML configuration file")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        with BridgeApp.from_file(args.config) as app:
            if args.command == "health":
                report = app.health_report()
                exit_code = 0 if report["status"] == "READY" else 1
            else:
                result = app.poll_once()
                report = result.as_dict()
                exit_code = (
                    0
                    if result.status in {
                        "NO_CHANGE",
                        "INITIALIZED",
                        "ADVANCED",
                        "ALREADY_SEEN",
                        "CANDIDATES_DISCOVERED",
                    }
                    else 3
                )
        print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
        return exit_code
    except BridgeError as exc:
        print(json.dumps({"status": "BLOCKED", "error": exc.as_dict()}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
