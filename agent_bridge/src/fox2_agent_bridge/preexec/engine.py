"""One fail-closed lifecycle for all FOX2 pre-dispatch receipts."""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
import hashlib
import errno
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

from jsonschema import Draft202012Validator, FormatChecker

from .. import project_dictionary as registry
from ..agent_policy import validate_selection
from .probes import agent_probe, observation


class InfrastructureFailure(Exception):
    """Fixed classification only; never carries raw command output."""


def git(root, *args):
    try:
        result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InfrastructureFailure('GIT_UNAVAILABLE') from exc
    if result.returncode:
        raise InfrastructureFailure('GIT_OPERATION_FAILED')
    return result.stdout


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def safe_path(root, relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or '\\' in relative or ':' in relative:
        raise InfrastructureFailure('UNSAFE_RECEIPT_PATH')
    result = root / relative
    if not result.resolve().is_relative_to(root.resolve()):
        raise InfrastructureFailure('UNSAFE_RECEIPT_PATH')
    return result


def secret_scan(raw):
    # Canonical evidence contains fixed classifications, not arbitrary subprocess text.
    if re.search(rb'(?i)(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|https?://[^\s/]+:[^\s/]+@|(?:authorization|access_token|api_key)\s*[=:])', raw):
        raise InfrastructureFailure('SECRET_HYGIENE_FAILED')


@dataclass(frozen=True)
class Requirements:
    wp_id: str
    branch: str
    worktree: Path
    source_head: str
    task_path: str
    receipt_path: str
    routes: tuple[dict, ...]
    pinned_agent: str | None = None

    def validate(self):
        if not re.fullmatch(r'work/FOX2-[A-Za-z0-9._/-]+', self.branch) or not re.fullmatch(r'[0-9a-f]{40}', self.source_head):
            raise InfrastructureFailure('INVALID_SOURCE_BINDING')
        if not self.worktree.is_absolute():
            raise InfrastructureFailure('INVALID_WORKTREE_BINDING')
        if not re.fullmatch(r'reports/.+/preexec/.+\.json', self.receipt_path):
            raise InfrastructureFailure('INVALID_RECEIPT_PATH')
        safe_path(self.worktree, self.task_path)
        safe_path(self.worktree, self.receipt_path)
        products = []
        for route in self.routes:
            try:
                normalized = validate_selection(route)
            except Exception as exc:
                raise InfrastructureFailure('INVALID_ROUTE_BINDING') from exc
            # Never normalize a route into a different requested tuple.
            if normalized != route:
                raise InfrastructureFailure('INCOMPLETE_ROUTE_BINDING')
            products.append(route['product'])
        if not products or len(set(products)) != len(products) or (self.pinned_agent and self.pinned_agent not in products):
            raise InfrastructureFailure('INVALID_AGENT_BINDING')


@dataclass(frozen=True)
class Outcome:
    receipt: dict | None
    exit_code: int
    remote_sha: str | None = None
    failure: str | None = None


def competing_writer(worktree):
    """Observe uncoordinated Windows writers without persisting command lines."""
    if os.name != 'nt':
        return False
    script = r'''$all = @(Get-CimInstance Win32_Process); $ignore = @(); $id = ''' + str(os.getpid()) + r''';
while ($id -and $id -notin $ignore) { $ignore += $id; $p = $all | Where-Object ProcessId -eq $id; $id = $p.ParentProcessId }
$target = $env:FOX2_PREFLIGHT_TARGET
$writers = @($all | Where-Object { $_.ProcessId -notin $ignore -and $_.Name -match '^(codex|copilot|python|pwsh|powershell)\.exe$' -and $_.CommandLine -and $_.CommandLine.Contains($target) })
if ($writers.Count -gt 0) { exit 20 } else { exit 0 }'''
    try:
        result = subprocess.run(['pwsh', '-NoLogo', '-NoProfile', '-Command', script],
                                env={**os.environ, 'FOX2_PREFLIGHT_TARGET': str(worktree)},
                                capture_output=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InfrastructureFailure('WRITER_STATE_UNKNOWN') from exc
    if result.returncode not in (0, 20):
        raise InfrastructureFailure('WRITER_STATE_UNKNOWN')
    return result.returncode == 20


@contextmanager
def writer_lock(root):
    """OS lock lives in this worktree's Git metadata and survives only its owner."""
    directory = Path(git(root, 'rev-parse', '--absolute-git-dir').decode().strip())
    path = directory / 'fox2-preexec.lock'
    try:
        stream = path.open('a+b')
    except OSError as exc:
        raise InfrastructureFailure('WRITER_LOCK_FAILED') from exc
    with stream:
        # Windows byte-range locks can cover EOF. Do not read or initialize the
        # byte before ownership: a competing owner's lock prohibits that read.
        stream.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            classification = 'COMPETING_WRITER' if exc.errno in (errno.EACCES, errno.EAGAIN, errno.EDEADLK) else 'WRITER_LOCK_FAILED'
            raise InfrastructureFailure(classification) from exc
        try:
            yield
        finally:
            try:
                stream.seek(0)
                if os.name == 'nt':
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(stream, fcntl.LOCK_UN)
            except OSError as exc:
                raise InfrastructureFailure('WRITER_RELEASE_FAILED') from exc


class PreExec:
    def __init__(self, requirements: Requirements, *, checks=None, probe=agent_probe,
                 writer_observer=competing_writer):
        self.requirements = requirements
        self.checks = checks or {}
        self.probe = probe
        self.writer_observer = writer_observer
        self.root = requirements.worktree
        # A trusted generated schema permits sanitized local failure evidence
        # even when the target worktree cannot supply its current contracts.
        self.schema = registry.PREFLIGHT_RECEIPT_SCHEMA

    def failure_receipt(self, failure):
        r = self.requirements
        task_source = None
        try:
            task = git(self.root, 'show', f'{r.source_head}:{r.task_path}')
            task_source = {'git_path': r.task_path, 'git_commit_sha': r.source_head,
                           'sha256': hashlib.sha256(task).hexdigest()}
        except InfrastructureFailure:
            pass
        receipt = {'schema_version': self.schema['properties']['schema_version']['const'],
                   'receipt_type': self.schema['properties']['receipt_type']['const'],
                   'project': registry.PROJECT_ID, 'wp_id': r.wp_id,
                   'checked_at': datetime.now(UTC).isoformat(), 'task_branch': r.branch,
                   'receipt_path': r.receipt_path, 'source_head': r.source_head,
                   'task_source': task_source, 'status': 'INFRA_FAILED',
                   'capabilities': {'shared_preexec': observation('UNKNOWN', failure=failure, code=None)},
                   'blockers': [{'code': failure, 'class': 'OTHER', 'material': True,
                                 'sanitized_detail': 'Safe preflight could not be established; no publication attempted.'}],
                   'worktree': {'status': 'INFRA_FAILED', 'path': str(self.root),
                                'competing_writer': 'PRESENT' if failure == 'COMPETING_WRITER' else 'UNKNOWN',
                                'stale_receipt_cleanup': 'NOT_RUN'},
                   'candidate_route': None,
                   'dispatch_state': {'executable_dispatch_published': False, 'dispatch_consumed': False},
                   'agent_execution_started': False,
                   'notes': ['Local diagnostic evidence only. No durable task-branch readiness claim.']}
        self.validate_receipt(receipt)
        return receipt

    def contracts(self):
        try:
            raw = git(self.root, 'show', f'{self.requirements.source_head}:{registry.SOURCE_PATH}')
        except InfrastructureFailure as exc:
            raise InfrastructureFailure('SOURCE_CONTRACT_UNAVAILABLE') from exc
        if hashlib.sha256(raw).hexdigest() != registry.SOURCE_SHA256:
            raise InfrastructureFailure('DICTIONARY_DRIFT')
        dictionary = json.loads(raw)
        for key, expected_hash in registry.CURRENT_CONTRACT_SHA256.items():
            identity = dictionary['current'][key]
            if identity != registry.CURRENT[key]:
                raise InfrastructureFailure('DICTIONARY_DRIFT')
            contract = git(self.root, 'show', f'{self.requirements.source_head}:{identity["path"]}')
            if hashlib.sha256(contract).hexdigest() != expected_hash:
                raise InfrastructureFailure('CONTRACT_SOURCE_DRIFT')
        self.schema = json.loads(git(self.root, 'show', f'{self.requirements.source_head}:{dictionary["current"]["preflight_receipt_schema"]["path"]}'))
        Draft202012Validator.check_schema(self.schema)

    def validate_receipt(self, receipt):
        Draft202012Validator(self.schema, format_checker=FormatChecker()).validate(receipt)
        identifiers = registry.IDENTIFIERS
        for value in receipt['capabilities'].values():
            if value['status'] not in identifiers['preflight_capability_statuses']:
                raise InfrastructureFailure('RECEIPT_ENUM_DRIFT')
        for blocker in receipt['blockers']:
            if blocker['class'] not in identifiers['preflight_blocker_classes']:
                raise InfrastructureFailure('RECEIPT_ENUM_DRIFT')
        raw = canonical(receipt)
        secret_scan(raw)
        return raw

    def hygiene(self, *, cleanup=False):
        r = self.requirements
        if Path(git(self.root, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != self.root.resolve():
            raise InfrastructureFailure('WORKTREE_MISMATCH')
        if git(self.root, 'branch', '--show-current').decode().strip() != r.branch:
            raise InfrastructureFailure('BRANCH_MISMATCH')
        if git(self.root, 'rev-parse', 'HEAD').decode().strip() != r.source_head:
            raise InfrastructureFailure('SOURCE_HEAD_MISMATCH')
        if git(self.root, 'diff', '--name-only', '--diff-filter=U').strip():
            raise InfrastructureFailure('UNMERGED_WORKTREE')
        entries = git(self.root, 'worktree', 'list', '--porcelain').decode().split('\n\n')
        owners = [e for e in entries if f'branch refs/heads/{r.branch}\n' in e + '\n']
        if len(owners) != 1 or Path(owners[0].splitlines()[0][9:]).resolve() != self.root.resolve():
            raise InfrastructureFailure('WORKTREE_OWNERSHIP_MISMATCH')
        if self.writer_observer(self.root):
            raise InfrastructureFailure('COMPETING_WRITER')
        # -z preserves filenames; renames have a second field and are never auto-cleaned.
        dirty = git(self.root, 'status', '--porcelain=v1', '-z', '--untracked-files=all').split(b'\0')
        dirty = [x for x in dirty if x]
        if not dirty:
            return 'NOT_NEEDED'
        if len(dirty) != 1 or dirty[0][3:].decode() != r.receipt_path or b'R' in dirty[0][:2] or b'C' in dirty[0][:2]:
            raise InfrastructureFailure('UNRELATED_WIP')
        if not cleanup:
            raise InfrastructureFailure('RECEIPT_WIP')
        path = safe_path(self.root, r.receipt_path)
        # Path alone is insufficient proof. Require matching schema, WP and source.
        try:
            stale = json.loads(path.read_bytes())
            self.validate_receipt(stale)
            if (stale['wp_id'], stale['task_branch'], stale['receipt_path'], stale['source_head']) != (r.wp_id, r.branch, r.receipt_path, r.source_head):
                raise ValueError('stale identity mismatch')
        except Exception as exc:
            raise InfrastructureFailure('STALE_RECEIPT_NOT_PROVEN') from exc
        git(self.root, 'reset', '--quiet', 'HEAD', '--', r.receipt_path)
        tracked = git(self.root, 'ls-files', '--', r.receipt_path).strip()
        if tracked:
            git(self.root, 'restore', '--source=HEAD', '--worktree', '--', r.receipt_path)
        else:
            path.unlink()
        return 'SAFE_ONLY'

    def build(self, cleanup):
        r = self.requirements
        task = git(self.root, 'show', f'{r.source_head}:{r.task_path}')
        receipt = {'schema_version': self.schema['properties']['schema_version']['const'],
                   'receipt_type': self.schema['properties']['receipt_type']['const'], 'project': registry.PROJECT_ID,
                   'wp_id': r.wp_id, 'checked_at': datetime.now(UTC).isoformat(),
                   'task_branch': r.branch, 'receipt_path': r.receipt_path, 'source_head': r.source_head,
                   'task_source': {'git_path': r.task_path, 'git_commit_sha': r.source_head,
                                   'sha256': hashlib.sha256(task).hexdigest()},
                   'status': 'PASS', 'capabilities': {}, 'blockers': [],
                   'worktree': {'status': 'PASS', 'path': str(self.root), 'competing_writer': 'NONE_OBSERVED',
                                'stale_receipt_cleanup': cleanup},
                   'candidate_route': None, 'dispatch_state': {'executable_dispatch_published': False,
                   'dispatch_consumed': False}, 'agent_execution_started': False,
                   'notes': ['Routing evidence only. CHAT selects the final implementation Agent.']}
        capabilities = receipt['capabilities']
        infra = False
        for name, check in self.checks.items():
            if name.lower() in {x['product'].lower() for x in r.routes} or name == registry.IDENTIFIERS['agent_route_materiality']['aggregate_capability']:
                raise InfrastructureFailure('RESERVED_CAPABILITY')
            try:
                capabilities[name] = check(self.root)
            except Exception:
                capabilities[name] = observation('UNKNOWN', failure='CHECK_INFRA_FAILED', code=None)
                infra = True
        for route in r.routes:
            try:
                value = self.probe(dict(route), self.root)
            except Exception:
                value = observation('UNKNOWN', material=False, failure='PROBE_INFRA_FAILED', code=None)
                infra = True
            value = dict(value)
            value['material'] = route['product'] == r.pinned_agent
            capabilities[route['product'].lower()] = value
        eligible = [route for route in r.routes if capabilities[route['product'].lower()]['status'] == 'PASS'
                    and (not r.pinned_agent or route['product'] == r.pinned_agent)]
        aggregate = registry.IDENTIFIERS['agent_route_materiality']['aggregate_capability']
        capabilities[aggregate] = observation('PASS' if eligible else 'FAIL', failure=None if eligible else 'NO_ELIGIBLE_AGENT_ROUTE')
        # Multiple successful alternatives never imply a selected Agent.
        if len(eligible) == 1:
            receipt['candidate_route'] = dict(eligible[0])
        for name, value in capabilities.items():
            if value.get('material', True) and value['status'] != 'PASS':
                failure = value.get('failure_class') or 'CAPABILITY_NOT_READY'
                group = 'AUTH' if failure == 'AUTH_REQUIRED' else 'CAPACITY' if failure == 'CAPACITY_OR_QUOTA' else 'CAPABILITY'
                receipt['blockers'].append({'code': 'CHECK_' + re.sub('[^A-Z0-9_]', '_', name.upper()),
                                            'class': group, 'material': True,
                                            'sanitized_detail': 'Required capability did not prove readiness.'})
                if value['status'] == 'UNKNOWN':
                    receipt['notes'].append('HOLD_UNKNOWN: a material observation remains unproven.')
        receipt['status'] = 'INFRA_FAILED' if infra else 'BLOCKED' if receipt['blockers'] else 'PASS'
        self.validate_receipt(receipt)
        return receipt

    def publish(self, receipt):
        r = self.requirements
        # Recheck source, writer and WIP immediately before the sole allowed write.
        self.hygiene()
        if git(self.root, 'ls-remote', '--refs', 'origin', 'refs/heads/' + r.branch).decode().split()[0] != r.source_head:
            raise InfrastructureFailure('REMOTE_SOURCE_MISMATCH')
        path = safe_path(self.root, r.receipt_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.validate_receipt(receipt))
        git(self.root, 'add', '--', r.receipt_path)
        git(self.root, 'diff', '--cached', '--check')
        staged = git(self.root, 'diff', '--cached', '--name-only', '-z').split(b'\0')
        if [x.decode() for x in staged if x] != [r.receipt_path]:
            raise InfrastructureFailure('STAGED_ALLOWLIST_FAILED')
        git(self.root, 'commit', '-m', f'preflight: record {r.wp_id} {receipt["status"].lower()}')
        local = git(self.root, 'rev-parse', 'HEAD').decode().strip()
        # Hooks or uncoordinated writers must not alter the bounded publication.
        if git(self.root, 'rev-parse', 'HEAD^').decode().strip() != r.source_head:
            raise InfrastructureFailure('PUBLICATION_SOURCE_CHANGED')
        changed = git(self.root, 'diff', r.source_head, local, '--name-only', '-z').split(b'\0')
        if [x.decode() for x in changed if x] != [r.receipt_path]:
            raise InfrastructureFailure('COMMITTED_ALLOWLIST_FAILED')
        if git(self.root, 'show', local + ':' + r.receipt_path) != self.validate_receipt(receipt):
            raise InfrastructureFailure('COMMITTED_RECEIPT_MISMATCH')
        if git(self.root, 'status', '--porcelain=v1', '-z', '--untracked-files=all').strip():
            raise InfrastructureFailure('PUBLICATION_WIP_CHANGED')
        if git(self.root, 'branch', '--show-current').decode().strip() != r.branch:
            raise InfrastructureFailure('BRANCH_MISMATCH')
        if self.writer_observer(self.root):
            raise InfrastructureFailure('COMPETING_WRITER')
        git(self.root, 'push', 'origin', 'HEAD:refs/heads/' + r.branch)
        lines = git(self.root, 'ls-remote', '--refs', 'origin', 'refs/heads/' + r.branch).decode().split()
        if not lines or lines[0] != local:
            raise InfrastructureFailure('REMOTE_READBACK_FAILED')
        # Read actual remote receipt bytes as well as its exact tip.
        git(self.root, 'fetch', 'origin', 'refs/heads/' + r.branch)
        if git(self.root, 'rev-parse', 'FETCH_HEAD').decode().strip() != local:
            raise InfrastructureFailure('REMOTE_READBACK_FAILED')
        if git(self.root, 'show', local + ':' + r.receipt_path) != self.validate_receipt(receipt):
            raise InfrastructureFailure('REMOTE_RECEIPT_MISMATCH')
        return local

    def run(self, *, publish=True, cleanup=False):
        receipt = None
        try:
            self.requirements.validate()
            with writer_lock(self.root):
                self.contracts()
                cleaned = self.hygiene(cleanup=cleanup)
                receipt = self.build(cleaned)
                # Probes cannot leave product changes or silently advance the head.
                self.hygiene()
                sha = self.publish(receipt) if publish else None
                return Outcome(receipt, {'PASS': 0, 'BLOCKED': 20, 'INFRA_FAILED': 30}[receipt['status']], sha)
        except InfrastructureFailure as exc:
            if receipt is None:
                try:
                    receipt = self.failure_receipt(str(exc))
                except Exception:
                    pass
            return Outcome(receipt, 31, failure=str(exc))
        except Exception:
            return Outcome(receipt, 32, failure='PREFLIGHT_INFRA_FAILED')
