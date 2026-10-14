from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import subprocess
import sys

import pytest

from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.errors import AgentNotStarted, DispatchInvalid, ReplayBlocked, ToolExecFailed, ToolNotFound
from fox2_agent_bridge.ledger import SQLiteLedger, utc_now


def _dispatch_payload(worktree: Path) -> dict[str, object]:
    return {
        "schema_version": "0.6",
        "project": "FOX2",
        "type": "NORMAL_AGENT_DISPATCH",
        "dispatch_id": "FOX2-BRIDGE-E2E-CANARY-001",
        "wp_id": "FOX2-BRIDGE-E2E-CANARY",
        "repository": "dunglt2505/FOX2",
        "control_ref": "refs/heads/work/FOX2-LOCAL-DISPATCH-chat",
        "agent": {
            "product": "COPILOT",
            "interface": "GITHUB_COPILOT_CLI",
        },
        "execution_path": "BRIDGE_DIRECT_COPILOT_CLI",
        "worktree": str(worktree),
        "branch": "work/FOX2-BRIDGE-E2E-CANARY-copilot",
        "base_sha": "a" * 40,
        "prompt": {
            "git_commit": "b" * 40,
            "path": "docs/agent_handoff/BRIDGE/FOX2_BRIDGE_E2E_CANARY_PROMPT.md",
            "git_blob_sha1": "c" * 40,
            "sha256": "d" * 64,
        },
        "allowed_code_paths": [],
        "allowed_report_paths": ["reports/FOX2-BRIDGE-E2E-CANARY/**"],
        "permissions": {
            "code_allowed": True,
            "git_code_push": True,
            "git_report_write": True,
            "git_report_push": True,
            "pr_create": False,
            "merge_allowed": False,
            "production_provider": False,
            "broker_write": False,
            "live": False,
        },
        "max_runs": 1,
    }


def test_dispatch_validation_accepts_minimal_canary(bridge_config, tmp_path: Path) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    runner = BridgeE2ERunner(bridge_config, ledger)
    payload = _dispatch_payload(
        bridge_config.worktree_root / "FOX2-BRIDGE-E2E-CANARY-COPILOT"
    )
    raw = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")

    validated = runner._validate_dispatch(
        raw,
        dispatch_path=(
            "docs/agent_handoff/FOX2-BRIDGE-E2E-CANARY/dispatch/"
            "FOX2-BRIDGE-E2E-CANARY-001.json"
        ),
        observed_blob_sha="e" * 40,
    )

    assert validated["dispatch_id"] == "FOX2-BRIDGE-E2E-CANARY-001"
    assert validated["_payload_sha256"] == hashlib.sha256(raw).hexdigest()


def test_path_scope_allows_only_declared_tree() -> None:
    patterns = ("reports/FOX2-BRIDGE-E2E-CANARY/**",)
    assert BridgeE2ERunner._path_allowed(
        "reports/FOX2-BRIDGE-E2E-CANARY/bridge_called_copilot.txt",
        patterns,
    )
    assert not BridgeE2ERunner._path_allowed("agent_bridge/src/unexpected.py", patterns)


def test_dispatch_claim_is_single_use(tmp_path: Path) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    now = utc_now()

    first = ledger.claim_dispatch(
        dispatch_id="FOX2-BRIDGE-E2E-CANARY-001",
        payload_hash="1" * 64,
        execution_id="execution-1",
        observed_at_utc=now,
    )
    second = ledger.claim_dispatch(
        dispatch_id="FOX2-BRIDGE-E2E-CANARY-001",
        payload_hash="1" * 64,
        execution_id="execution-2",
        observed_at_utc=now,
    )

    assert first is True
    assert second is False
    assert ledger.dispatch_state("FOX2-BRIDGE-E2E-CANARY-001")["state"] == "CLAIMED"


def test_dispatch_validation_maps_pytest_capability_to_safe_tools(
    bridge_config, tmp_path: Path
) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    runner = BridgeE2ERunner(bridge_config, ledger)
    payload = _dispatch_payload(
        bridge_config.worktree_root / "FOX2-BRIDGE-DEV-PYTEST-COPILOT"
    )
    payload["runtime_contract"] = {
        "auto_execute": True,
        "dev_shell_capabilities": ["PYTEST"],
    }
    raw = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")

    validated = runner._validate_dispatch(
        raw,
        dispatch_path=(
            "docs/agent_handoff/FOX2-BRIDGE-E2E-CANARY/dispatch/"
            "FOX2-BRIDGE-E2E-CANARY-001.json"
        ),
        observed_blob_sha="e" * 40,
    )

    assert validated["_copilot_shell_tools"] == [
        "shell(python -m pytest --version)",
        "shell(python -m pytest -q)",
        "shell(python -m pytest tests/m1_p2_01 -q)",
    ]


def test_dispatch_validation_rejects_unknown_dev_shell_capability(
    bridge_config, tmp_path: Path
) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    runner = BridgeE2ERunner(bridge_config, ledger)
    payload = _dispatch_payload(
        bridge_config.worktree_root / "FOX2-BRIDGE-DEV-UNSAFE-COPILOT"
    )
    payload["runtime_contract"] = {
        "auto_execute": True,
        "dev_shell_capabilities": ["ARBITRARY_SHELL"],
    }
    raw = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")

    with pytest.raises(DispatchInvalid, match="unsupported"):
        runner._validate_dispatch(
            raw,
            dispatch_path=(
                "docs/agent_handoff/FOX2-BRIDGE-E2E-CANARY/dispatch/"
                "FOX2-BRIDGE-E2E-CANARY-001.json"
            ),
            observed_blob_sha="e" * 40,
        )


def test_dispatch_validation_accepts_codex_cli_route(
    bridge_config, tmp_path: Path
) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    runner = BridgeE2ERunner(bridge_config, ledger)
    payload = _dispatch_payload(
        bridge_config.worktree_root / "FOX2-BRIDGE-CODEX-CANARY-COPILOT"
    )
    payload["agent"] = {
        "product": "CODEX",
        "interface": "OPENAI_CODEX_CLI",
    }
    payload["execution_path"] = "BRIDGE_DIRECT_CODEX_CLI"
    payload["runtime_contract"] = {"auto_execute": True}
    raw = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")

    validated = runner._validate_dispatch(
        raw,
        dispatch_path=(
            "docs/agent_handoff/FOX2-BRIDGE-E2E-CANARY/dispatch/"
            "FOX2-BRIDGE-E2E-CANARY-001.json"
        ),
        observed_blob_sha="e" * 40,
    )

    assert validated["_agent_product"] == "CODEX"
    assert validated["_copilot_shell_tools"] == []


def test_dispatch_validation_rejects_copilot_shell_capability_for_codex(
    bridge_config, tmp_path: Path
) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    runner = BridgeE2ERunner(bridge_config, ledger)
    payload = _dispatch_payload(
        bridge_config.worktree_root / "FOX2-BRIDGE-CODEX-UNSAFE-COPILOT"
    )
    payload["agent"] = {
        "product": "CODEX",
        "interface": "OPENAI_CODEX_CLI",
    }
    payload["execution_path"] = "BRIDGE_DIRECT_CODEX_CLI"
    payload["runtime_contract"] = {
        "auto_execute": True,
        "dev_shell_capabilities": ["PYTEST"],
    }
    raw = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")

    with pytest.raises(DispatchInvalid, match="must not request Copilot"):
        runner._validate_dispatch(
            raw,
            dispatch_path=(
                "docs/agent_handoff/FOX2-BRIDGE-E2E-CANARY/dispatch/"
                "FOX2-BRIDGE-E2E-CANARY-001.json"
            ),
            observed_blob_sha="e" * 40,
        )

@pytest.fixture
def execution_harness(bridge_config, monkeypatch):
    """Real validation, adapters and ledger; local control/worktree fixtures."""
    def make(product):
        worktree = bridge_config.worktree_root / 'FIX-01-FAKE-AGENT'
        worktree.mkdir(parents=True)
        (worktree / '.git').write_text('gitdir: test', encoding='utf-8')
        payload = _dispatch_payload(worktree)
        payload['agent'] = {
            'product': product,
            'interface': 'OPENAI_CODEX_CLI' if product == 'CODEX' else 'GITHUB_COPILOT_CLI',
            'model_policy': 'PINNED', 'model': 'fixture-model',
        }
        payload['execution_path'] = f'BRIDGE_DIRECT_{product}_CLI'
        raw = (json.dumps(payload, sort_keys=True) + '\n').encode()
        dispatch_path = f"docs/agent_handoff/BRIDGE/dispatch/{payload['dispatch_id']}.json"
        transport = SimpleNamespace(
            query_control_sha=lambda _: 'c' * 40,
            fetch_control=lambda *_: None,
            read_dispatch_blob=lambda *_: (raw, 'd' * 40),
        )
        ledger = SQLiteLedger(bridge_config.database_path)
        ledger.initialize()
        runner = BridgeE2ERunner(bridge_config, ledger, transport=transport)
        monkeypatch.setattr('fox2_agent_bridge.e2e_runner.DispatchPoller.poll_once',
                            lambda _: SimpleNamespace(status='NO_CHANGE'))
        monkeypatch.setattr(runner, '_resolve_worktree', lambda _: (worktree, 'a' * 40))
        monkeypatch.setattr(runner, '_resolve_prompt', lambda _: 'immutable local fixture prompt')
        monkeypatch.setattr(runner, '_commit_and_push_codex_result',
                            lambda **_: pytest.fail('non-zero/pre-spawn failure must not publish'))
        from fox2_agent_bridge.codex_adapter import CodexAdapter
        from fox2_agent_bridge.copilot_adapter import CopilotAdapter
        selected = CodexAdapter if product == 'CODEX' else CopilotAdapter
        alternate = CopilotAdapter if product == 'CODEX' else CodexAdapter
        monkeypatch.setattr(selected, '_resolve_executable', lambda _: Path(sys.executable))
        monkeypatch.setattr(alternate, 'run_prompt',
                            lambda *args, **kwargs: pytest.fail('alternate Agent substitution'))
        module = f'fox2_agent_bridge.{product.lower()}_adapter'
        monkeypatch.setattr(module + '.help_text', lambda *_: '--model --no-ask-user')
        return runner, ledger, payload, dispatch_path, selected, module
    return make


@pytest.mark.parametrize('product', ['CODEX', 'COPILOT'])
@pytest.mark.parametrize('exit_code,diagnostic', [(1, 'execution failed'), (75, 'quota exhausted')])
def test_nonzero_after_agent_start_needs_reconciliation(
    execution_harness, monkeypatch, tmp_path, product, exit_code, diagnostic,
):
    runner, ledger, payload, dispatch_path, _, module = execution_harness(product)
    child = tmp_path / 'fake_agent.py'
    child.write_text(
        'import json, os, sqlite3, sys\n'
        'from pathlib import Path\n'
        'database, dispatch_id, product, exit_code, diagnostic = sys.argv[1:]\n'
        'if product == "CODEX":\n'
        '    assert sys.stdin.read().strip() == "immutable local fixture prompt"\n'
        'with sqlite3.connect(database) as connection:\n'
        '    state, stage, execution_id = connection.execute(\n'
        '        "SELECT state, stage, execution_id FROM executions WHERE dispatch_id=?",\n'
        '        (dispatch_id,)).fetchone()\n'
        'assert state == "RUNNING" and stage == "RUNNING"\n'
        'proof = {"event": "STARTED", "pid": os.getpid(), "state": state,\n'
        '         "stage": stage, "execution_id": execution_id, "model": "fixture-model"}\n'
        'Path("partial-result.json").write_text(json.dumps(proof), encoding="utf-8")\n'
        'print(json.dumps(proof), flush=True)\n'
        'print(diagnostic, file=sys.stderr, flush=True)\n'
        'sys.exit(int(exit_code))\n', encoding='utf-8',
    )
    native_popen = subprocess.Popen
    launches = []
    def launch_local_child(command, **kwargs):
        launches.append(command)
        assert ledger.dispatch_status(payload['dispatch_id'])['stage'] == 'RUNNING'
        return native_popen(
            [sys.executable, str(child), str(ledger.database_path), payload['dispatch_id'],
             product, str(exit_code), diagnostic], **kwargs,
        )
    monkeypatch.setattr(module + '.subprocess.Popen', launch_local_child)

    with pytest.raises(ToolExecFailed, match=f'non-zero exit code {exit_code}'):
        runner.run_once(dispatch_path=dispatch_path)

    status = ledger.dispatch_status(payload['dispatch_id'])
    proof = json.loads((Path(payload['worktree']) / 'partial-result.json').read_text())
    assert proof['event'] == 'STARTED' and proof['pid'] > 0
    assert proof['state'] == proof['stage'] == 'RUNNING'
    assert proof['execution_id'] == status['execution_id']
    assert status['dispatch_state'] == status['execution_state'] == 'NEEDS_RECONCILIATION'
    assert status['stage'] == 'AGENT_EXITED'
    assert status['payload_hash'] == hashlib.sha256(
        runner.transport.read_dispatch_blob(None, None)[0]).hexdigest()
    assert status['checkpoint']['agent_exit_code'] == exit_code
    assert json.loads(status['checkpoint']['agent_stdout']) == proof
    assert status['checkpoint']['agent_stderr'].strip() == diagnostic
    assert status['checkpoint']['agent_metadata']['observed_model'] == 'fixture-model'
    result = status['result'][product.lower()]
    assert result['exit_code'] == exit_code
    assert result['stderr'].strip() == diagnostic
    assert json.loads(result['stdout']) == proof
    assert not ledger.claim_dispatch(
        dispatch_id=payload['dispatch_id'], payload_hash=status['payload_hash'],
        execution_id='replay', observed_at_utc=utc_now(),
    )
    with pytest.raises(ReplayBlocked):
        runner.run_once(dispatch_path=dispatch_path)
    from fox2_agent_bridge.desktop import reconcile
    assert reconcile(ledger, runner) == []
    assert ledger.dispatch_status(payload['dispatch_id']) == status
    assert len(launches) == 1
    snapshot = runner.config.bridge_root / 'data' / 'results' / f"{payload['dispatch_id']}.json"
    report = json.loads(snapshot.read_text())
    assert report['status'] == 'NEEDS_RECONCILIATION'
    assert report['result'][product.lower()]['exit_code'] == exit_code


@pytest.mark.parametrize('product', ['CODEX', 'COPILOT'])
@pytest.mark.parametrize('failure', ['missing_tool', 'unsupported_capability', 'spawn_oserror'])
def test_proven_prespawn_failure_remains_terminal(
    execution_harness, monkeypatch, product, failure,
):
    runner, ledger, payload, dispatch_path, selected, module = execution_harness(product)
    attempts = []
    def never_spawn(command, **kwargs):
        attempts.append(command)
        if failure == 'spawn_oserror':
            raise PermissionError('fixture spawn denied before process creation')
        pytest.fail('proven pre-spawn rejection must not create a process')
    monkeypatch.setattr(module + '.subprocess.Popen', never_spawn)
    if failure == 'missing_tool':
        def missing(_):
            raise ToolNotFound('fixture exact Agent tool unavailable')
        monkeypatch.setattr(selected, '_resolve_executable', missing)
        expected = ToolNotFound
    else:
        expected = AgentNotStarted
        if failure == 'unsupported_capability':
            monkeypatch.setattr(module + '.help_text', lambda *_: '')
    with pytest.raises(expected):
        runner.run_once(dispatch_path=dispatch_path)
    status = ledger.dispatch_status(payload['dispatch_id'])
    assert status['dispatch_state'] == status['execution_state'] == 'FAILED'
    assert status['error_code'] == expected.code
    assert 'agent_exit_code' not in status['checkpoint']
    assert len(attempts) == (1 if failure == 'spawn_oserror' else 0)
    assert not ledger.claim_dispatch(
        dispatch_id=payload['dispatch_id'], payload_hash=status['payload_hash'],
        execution_id='replay', observed_at_utc=utc_now(),
    )
    with pytest.raises(ReplayBlocked):
        runner.run_once(dispatch_path=dispatch_path)
    assert len(attempts) == (1 if failure == 'spawn_oserror' else 0)


@pytest.mark.parametrize('stage', ['AGENT_EXITED', 'PUBLISHING'])
@pytest.mark.parametrize('exit_code', [1, 75])
def test_restart_after_nonzero_exit_checkpoint_never_publishes(tmp_path, stage, exit_code):
    from fox2_agent_bridge.desktop import reconcile
    ledger = SQLiteLedger(tmp_path / 'bridge.db')
    ledger.initialize()
    ledger.claim_dispatch(dispatch_id='nonzero', payload_hash='a' * 64,
                          execution_id='e', observed_at_utc=utc_now())
    checkpoint = {'agent_exit_code': exit_code, 'agent_stdout': 'partial work',
                  'agent_stderr': 'quota/execution failure'}
    ledger.checkpoint('e', stage, checkpoint)
    verifier = SimpleNamespace(_verify_result=lambda **_: pytest.fail('non-zero recovery must not verify as published'))
    assert reconcile(ledger, verifier)[0]['outcome'] == 'NEEDS_RECONCILIATION'
    status = ledger.dispatch_status('nonzero')
    assert status['execution_state'] == status['dispatch_state'] == 'NEEDS_RECONCILIATION'
    assert status['checkpoint'] == checkpoint
    assert not ledger.claim_dispatch(dispatch_id='nonzero', payload_hash='a' * 64,
                                     execution_id='replay', observed_at_utc=utc_now())
