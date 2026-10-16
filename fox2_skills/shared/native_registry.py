"""Adapter for the observed FOX2 Dictionary and files[] release manifest.

Identity verification does not establish current authority. The host must provide
an independently authorized release-chain verifier; none is bundled or inferred.
"""
import json
import re
import hashlib
from .core import Hold, digest
from .errors import SourceError


def bind(git, bootstrap, family, authority_verifier=None):
    if not bootstrap or authority_verifier is None:
        raise Hold('UNVERIFIED', 'Missing owner-authorized bootstrap/release-chain verifier')
    try:
        commit = bootstrap['commit']
        if not re.fullmatch('[a-f0-9]{40}', commit):
            raise Hold('UNVERIFIED', 'Bootstrap requires immutable commit')
        if not git.authenticated:
            raise Hold('UNVERIFIED', 'Authenticated readback required')
        registry_bytes = git.read_file(bootstrap['dictionary_path'], commit)
        manifest_bytes = git.read_file(bootstrap['manifest_path'], commit)
        registry, manifest = json.loads(registry_bytes), json.loads(manifest_bytes)
        # This callback owns applicability, semantic owner, lineage, supersession,
        # allowed refs and competing releases. A status string cannot replace it.
        decision = authority_verifier(bootstrap, registry_bytes, manifest_bytes, family)
        if decision.get('status') != 'VERIFIED_EFFECTIVE' or not decision.get('evidence'):
            raise Hold(decision.get('status', 'UNVERIFIED'), 'Authority chain unresolved')
        if registry.get('dictionary_id') != 'FOX2_PROJECT_DICTIONARY':
            raise Hold('UNVERIFIED', 'Unsupported Dictionary identity')
        if registry.get('project', {}).get('id') != 'FOX2':
            raise Hold('SOURCE_CONFLICT', 'Project identity mismatch')
        if registry.get('status') != 'RELEASED_EFFECTIVE':
            raise Hold('UNVERIFIED', 'Dictionary not released')
        entry = registry['current'][family]
        if entry.get('status', 'RELEASED_EFFECTIVE') != 'RELEASED_EFFECTIVE':
            raise Hold('UNVERIFIED', 'Candidate pointer')
        records = {x['path']: x for x in manifest['files']}
        # A release manifest must bind the exact Dictionary bytes too.
        for path, content in [(bootstrap['dictionary_path'], registry_bytes),
                              (entry['path'], git.read_file(entry['path'], commit))]:
            record = records[path]
            blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
            if record.get('sha256'):
                matches = digest(content) == record['sha256'] and len(content) == record['bytes']
            else:
                matches = bool(record.get('blob_sha')) and blob == record['blob_sha']
            if not matches:
                raise Hold('UNVERIFIED', 'Manifest byte/hash mismatch: ' + path)
        return {'status': 'VERIFIED_EFFECTIVE', 'family': family, 'commit': commit,
                'path': entry['path'], 'sha256': digest(git.read_file(entry['path'], commit)),
                'registry_sha256': digest(registry_bytes),
                'manifest_sha256': digest(manifest_bytes), 'authority_evidence': decision['evidence']}
    except Hold:
        raise
    except (OSError, TimeoutError) as exc:
        raise Hold('UNAVAILABLE', 'Git unavailable; no cached PASS') from exc
    except (ValueError, KeyError, TypeError, AttributeError, SourceError) as exc:
        raise Hold('UNVERIFIED', 'Incomplete/unsupported native release evidence') from exc
