"""Command-line entry point for FOX2 Bridge."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .errors import BridgeError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fox2-bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    health = subparsers.add_parser("health", help="validate local Bridge core prerequisites")
    health.add_argument("--config", type=Path, help="optional TOML configuration file")

    poll = subparsers.add_parser("poll-once", help="read the FOX2 control branch once")
    poll.add_argument("--config", type=Path, help="optional TOML configuration file")

    smoke = subparsers.add_parser(
        "copilot-smoke",
        help="launch one bounded no-write GitHub Copilot CLI prompt in an exact FOX2 worktree",
    )
    smoke.add_argument("--config", type=Path, help="optional TOML configuration file")
    smoke.add_argument("--worktree", type=Path, required=True, help="exact FOX2 worktree path")
    smoke.add_argument("--timeout", type=int, default=120, help="timeout in seconds")

    e2e = subparsers.add_parser(
        "e2e-once",
        help="execute one exact immutable FOX2 dispatch path through its selected Agent CLI",
    )
    e2e.add_argument("--config", type=Path, help="optional TOML configuration file")
    e2e.add_argument("--dispatch-path", required=True, help="exact control-branch dispatch path")
    e2e.add_argument("--timeout", type=int, default=300, help="Agent timeout in seconds")

    recovery = subparsers.add_parser("recover-delivery", help="recover delivery without launching an Agent")
    recovery.add_argument("--config", type=Path)
    recovery.add_argument("--dispatch-path", required=True)

    run_next = subparsers.add_parser(
        "run-next",
        help="poll and execute one eligible runtime_contract.auto_execute dispatch",
    )
    run_next.add_argument("--config", type=Path, help="optional TOML configuration file")
    run_next.add_argument("--timeout", type=int, default=300, help="Agent timeout in seconds")

    status = subparsers.add_parser(
        "status",
        help="show persisted dispatch/execution state",
    )
    status.add_argument("--config", type=Path, help="optional TOML configuration file")
    status.add_argument("--dispatch-id", help="optional exact dispatch id")
    status.add_argument("--limit", type=int, default=20, help="recent rows when no id is supplied")

    for name in ("start", "pause", "resume", "check-now", "status", "stop"):
        worker = subparsers.add_parser(f"worker-{name}", help=f"background Worker {name}")
        worker.add_argument("--config", type=Path)
        if name == "start":
            worker.add_argument("--timeout", type=int, default=300)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    # Lazy import keeps --help independent from runtime/tool discovery imports.
    from .app import BridgeApp

    try:
        if args.command.startswith("worker-") and args.command != "worker-start":
            from .worker import control_worker
            report = control_worker(BridgeApp.from_file(args.config), args.command.removeprefix("worker-"))
            print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
            return 0
        with BridgeApp.from_file(args.config) as app:
            if args.command == "worker-start":
                from .worker import BackgroundWorker
                BackgroundWorker(app, timeout_seconds=args.timeout).run()
                report = {"status": "STOPPED"}
                exit_code = 0
            elif args.command == "health":
                report = app.health_report()
                exit_code = 0 if report["status"] == "READY" else 1
            elif args.command == "poll-once":
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
            elif args.command == "copilot-smoke":
                result = app.copilot_smoke(
                    worktree=args.worktree,
                    timeout_seconds=args.timeout,
                )
                report = result.as_dict()
                exit_code = 0 if result.status == "COPILOT_EXITED" else 4
            elif args.command == "e2e-once":
                result = app.e2e_once(
                    dispatch_path=args.dispatch_path,
                    timeout_seconds=args.timeout,
                )
                report = result.as_dict()
                exit_code = 0 if result.status == "PUSHED_UNREVIEWED" else 5
            elif args.command == "recover-delivery":
                result = app.recover_delivery(dispatch_path=args.dispatch_path)
                report = result.as_dict()
                exit_code = 0 if result.status == "PUSHED_UNREVIEWED" else 5
            elif args.command == "run-next":
                result = app.ops_run_next(timeout_seconds=args.timeout)
                report = result.as_dict()
                exit_code = (
                    0
                    if result.status in {"PUSHED_UNREVIEWED", "NO_ELIGIBLE_DISPATCH"}
                    else 5
                )
            else:
                report = app.ops_status(
                    dispatch_id=args.dispatch_id,
                    limit=args.limit,
                )
                exit_code = 0

        print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
        return exit_code
    except BridgeError as exc:
        print(
            json.dumps(
                {"status": "BLOCKED", "error": exc.as_dict()},
                ensure_ascii=True,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2
    except KeyboardInterrupt:
        print(
            json.dumps(
                {
                    "status": "INTERRUPTED",
                    "error": {
                        "code": "USER_INTERRUPT",
                        "message": "Bridge command interrupted by local user",
                    },
                },
                ensure_ascii=True,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
