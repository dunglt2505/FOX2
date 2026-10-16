"""Host-callable bounded helpers. No dispatch, publication or promotion side effects."""
import json
from pathlib import Path
from .core import Hold, preflight, verify_evidence

ROOT = Path(__file__).resolve().parents[1]


def invoke(skill, request, bindings, grants, evidence_root):
    catalog = json.loads((ROOT / 'contracts.json').read_text(encoding='utf-8'))
    if skill not in catalog:
        raise Hold('BLOCKED', 'Unknown Skill')
    contract = catalog[skill]
    if not request.get('task_id') or not request.get('cutoff'):
        raise Hold('BLOCKED', 'Task identity and cutoff required')
    if request.get('state') == 'COMPLETED':
        raise Hold('BLOCKED', 'Finished task; no replay')
    preflight(skill, grants, bindings, contract['sources'])
    data = request.get('input', {})
    missing = [k for k in contract['inputs'] if k not in data or data[k] is None]
    if missing:
        raise Hold('BLOCKED', 'Missing inputs: ' + ', '.join(missing))
    # Readback is a distinct evidence class from semantic acceptance.
    receipt = verify_evidence(evidence_root, request.get('evidence', []))
    return {'status': 'PREPARED_FOR_HOST_REVIEW', 'skill': skill,
            'task_id': request['task_id'], 'cutoff': request['cutoff'],
            'source_lock': bindings, 'readback': receipt,
            'output': {k: data[k] for k in contract['inputs']},
            'acceptance': contract['acceptance'], 'effects': []}


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--skill', required=True)
    p.add_argument('--request', required=True)
    p.add_argument('--evidence-root', required=True)
    a = p.parse_args()
    r = json.loads(Path(a.request).read_text(encoding='utf-8'))
    # Serialized claims cannot authorize a real host invocation.
    try:
        result = invoke(a.skill, r, {}, [], a.evidence_root)
    except Hold as exc:
        print(json.dumps({'status': exc.status, 'reason': str(exc)}))
        return 2
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
