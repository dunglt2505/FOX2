"""Offline artifact generation only. Does not install, start or apply anything."""
import argparse
import json
from pathlib import Path

from fox2_agent_bridge.f1_policy import Artifact, policy_artifact, transition_artifact


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True,
                        help='reviewed host baseline XML; never harvested automatically')
    parser.add_argument('--local-snapshot', type=Path)
    parser.add_argument('--effective-snapshot', type=Path)
    parser.add_argument('--rollback-artifact', type=Path)
    args = parser.parse_args()
    transition_inputs = (args.local_snapshot, args.effective_snapshot, args.rollback_artifact)
    if any(transition_inputs) and not all(transition_inputs):
        parser.error('local/effective snapshots and rollback artifact must be supplied together')
    value = json.loads(args.inventory.read_text(encoding='utf-8'))
    xml, manifest = policy_artifact(tuple(Artifact(**a) for a in value['artifacts']),
        source_commit=value['source_commit'], package_digest=value['package_digest'],
        baseline_xml=args.baseline.read_bytes(), conditional_modes=value.get('conditional_modes'))
    args.output.write_bytes(xml)
    args.output.with_suffix('.json').write_text(json.dumps(manifest, sort_keys=True, indent=2) + '\n',
                                              encoding='utf-8', newline='\n')
    if all(transition_inputs):
        audit, transition = transition_artifact(local_snapshot=args.local_snapshot.read_bytes(),
            effective_snapshot=args.effective_snapshot.read_bytes(), final_xml=xml,
            f1_rule_ids=manifest['f1_rule_ids'], rollback_artifact=args.rollback_artifact.read_bytes())
        args.output.with_suffix('.audit.xml').write_bytes(audit)
        args.output.with_suffix('.transition.json').write_text(
            json.dumps(transition, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
