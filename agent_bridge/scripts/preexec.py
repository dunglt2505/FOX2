"""Shared CLI. Only publication plus exact readback emits RECEIPT_PUSHED."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from fox2_agent_bridge.preexec import PreExec, Requirements
from fox2_agent_bridge.preexec.engine import canonical, safe_path
from fox2_agent_bridge.preexec.profiles import ROUTES, checks, identity


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=('app', 'bridge', 'rollout'), required=True)
    parser.add_argument('--worktree', type=Path, required=True)
    parser.add_argument('--source-head', required=True)
    parser.add_argument('--pinned-agent', choices=('CODEX', 'COPILOT'))
    parser.add_argument('--cleanup-stale-receipt', action='store_true')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--publish', action='store_true')
    mode.add_argument('--snapshot-root', type=Path, help='Evidence only; no commit/push and no durable PASS claim')
    parser.add_argument('--snapshot-path', help='Authorized reports/.../preexec/*.json path inside snapshot root')
    args = parser.parse_args(argv)
    wp, branch, task, receipt_path = identity(args.profile)
    if args.snapshot_root:
        if not args.snapshot_path:
            parser.error('--snapshot-path is required for snapshots')
        receipt_path = args.snapshot_path
    config = Requirements(wp, branch, args.worktree.resolve(), args.source_head, task,
                          receipt_path, ROUTES, args.pinned_agent)
    result = PreExec(config, checks=checks(args.profile)).run(publish=args.publish,
                    cleanup=args.cleanup_stale_receipt)
    if args.snapshot_root and result.receipt:
        try:
            output = safe_path(args.snapshot_root.resolve(), receipt_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(canonical(result.receipt))
        except Exception:
            print('PREFLIGHT_INFRA_FAILURE=SNAPSHOT_WRITE_FAILED')
            return 32
        print('PREFLIGHT_SNAPSHOT_STATUS=' + result.receipt['status'])
        print('PREFLIGHT_PUBLICATION=NOT_ATTEMPTED')
    if result.failure:
        print('PREFLIGHT_INFRA_FAILURE=' + result.failure)
    elif result.remote_sha:
        print('RECEIPT_PUSHED=' + result.remote_sha)
        print('PREFLIGHT_STATUS=' + result.receipt['status'])
    if args.snapshot_root and not result.failure:
        # Codes 0/20 are reserved for durable PASS/BLOCKED publication.
        return 33
    return result.exit_code


if __name__ == '__main__':
    raise SystemExit(main())
