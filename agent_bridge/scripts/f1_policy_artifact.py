"""Offline artifact generation only. Does not install, start or apply anything."""
import argparse
import json
from pathlib import Path

from fox2_agent_bridge.f1_policy import Artifact, policy_artifact


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    value = json.loads(args.inventory.read_text(encoding='utf-8'))
    xml, manifest = policy_artifact(tuple(Artifact(**a) for a in value['artifacts']),
        source_commit=value['source_commit'], package_digest=value['package_digest'])
    args.output.write_bytes(xml)
    args.output.with_suffix('.json').write_text(json.dumps(manifest, sort_keys=True, indent=2) + '\n',
                                              encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
