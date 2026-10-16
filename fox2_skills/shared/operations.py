"""Deterministic, read-only workflow analyses; consequential effects stay in host."""
from collections import Counter
from pathlib import Path
from .core import Hold, digest, verify_evidence


def file_plan(source, destination):
    """No mutation; never overwrite same-name differing content."""
    source, destination = Path(source), Path(destination)
    raw = source.read_bytes()
    status = 'COPY_REQUIRED'
    if destination.exists():
        status = 'IDENTICAL' if destination.read_bytes() == raw else 'CONFLICT'
    return {'source': str(source), 'destination': str(destination), 'sha256': digest(raw), 'status': status}


def sync_file(source, destination, allowed_root, authorized=False):
    if not authorized:
        raise Hold('BLOCKED', 'Scoped sync authorization absent')
    source, destination = Path(source), Path(destination).resolve()
    if not destination.is_relative_to(Path(allowed_root).resolve()):
        raise Hold('BLOCKED', 'Destination outside allowed root')
    raw = source.read_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open('xb') as out:
            out.write(raw)
    except FileExistsError:
        if destination.read_bytes() != raw:
            raise Hold('SOURCE_CONFLICT', 'Existing destination differs; not overwritten')
    if destination.read_bytes() != raw:
        raise Hold('UNVERIFIED', 'Destination readback mismatch')
    return {'status':'SAVE_READBACK_VERIFIED', 'sha256':digest(raw),
            'destination':str(destination), 'release_status':'NOT_RELEASED',
            'registry_status':'UNCHANGED', 'mirror_status':'BYTES_VERIFIED'}


def acceptance_review(root, acceptance, evidence):
    """Each claimed acceptance maps to byte-verified evidence and observed outcome.

    The caller still owns independent observation and semantic interpretation.
    """
    findings = {}
    for key in acceptance:
        row = evidence.get(key)
        if not row or row.get('outcome') != 'PASS' or not row.get('observed_by'):
            findings[key] = 'UNVERIFIED'
            continue
        try:
            verify_evidence(root, row.get('receipts', []))
            findings[key] = 'EVIDENCE_PRESENT'
        except Hold:
            findings[key] = 'UNVERIFIED'
    return findings


def traceability(requirements, mapping):
    gaps = [r for r in requirements if not mapping.get(r)]
    return {'covered': [r for r in requirements if r not in gaps], 'gaps': gaps}


def health(acceptance, observations, cutoff):
    states = {key: observations.get(key, 'UNKNOWN') for key in acceptance}
    return {'cutoff': cutoff, 'acceptance': states,
            'unknowns': [k for k,v in states.items() if v == 'UNKNOWN'],
            'blockers': [k for k,v in states.items() if v in ('FAIL', 'BLOCKED')]}


def recover(planned_effects, completed_effects, actual_state_verified):
    if not actual_state_verified:
        raise Hold('BLOCKED', 'Recovery requires actual state readback')
    return {'retry': [x for x in planned_effects if x not in completed_effects],
            'preserved_completed': list(completed_effects)}


def triage(findings):
    groups = Counter(row['root_cause'] for row in findings)
    return {'root_causes': dict(groups), 'priority': sorted(groups, key=lambda k: (-groups[k], k))}


def research(method, data, backtest, limits):
    missing = [name for name,value in [('method',method),('data',data),('backtest',backtest),('limits',limits)] if not value]
    return {'evidence_tier': 'INCOMPLETE' if missing else 'DOCUMENTED_PENDING_DOMAIN_VALIDATION',
            'missing': missing, 'deployment_authorized': False}
