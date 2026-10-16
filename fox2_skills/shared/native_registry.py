"""Native release-byte adapter; effectivity requires an owning host verifier."""
import json
import re
import hashlib
import subprocess
from .core import Hold, digest
from .errors import SourceError


def bind(git, bootstrap, family, authority_verifier=None):
    if not bootstrap or authority_verifier is None:
        raise Hold('UNVERIFIED', 'Missing owner-authorized bootstrap/release-chain verifier')
    try:
        manifest_commit = bootstrap['commit']
        if not re.fullmatch('[a-f0-9]{40}', manifest_commit):
            raise Hold('UNVERIFIED', 'Bootstrap requires immutable commit')
        if not git.authenticated:
            raise Hold('UNVERIFIED', 'Authenticated readback required')
        manifest_bytes = git.read_file(bootstrap['manifest_path'], manifest_commit)
        manifest = json.loads(manifest_bytes)
        # Native coordinated releases commit the manifest after their source set.
        # This pointer selects bytes only; the verifier must authorize the chain.
        source_commit = manifest.get('source_set_head', manifest_commit)
        if not isinstance(source_commit, str) or not re.fullmatch('[a-f0-9]{40}', source_commit):
            raise Hold('UNVERIFIED', 'Release requires immutable source_set_head')
        registry_bytes = git.read_file(bootstrap['dictionary_path'], source_commit)
        registry = json.loads(registry_bytes)
        decision = authority_verifier(bootstrap, registry_bytes, manifest_bytes, family)
        if decision.get('status') != 'VERIFIED_EFFECTIVE' or not decision.get('evidence'):
            raise Hold(decision.get('status', 'UNVERIFIED'), decision.get('reason', 'Authority chain unresolved'))
        if registry.get('dictionary_id') != 'FOX2_PROJECT_DICTIONARY':
            raise Hold('UNVERIFIED', 'Unsupported Dictionary identity')
        if registry.get('project', {}).get('id') != 'FOX2':
            raise Hold('SOURCE_CONFLICT', 'Project identity mismatch')
        if registry.get('status') != 'RELEASED_EFFECTIVE':
            raise Hold('UNVERIFIED', 'Dictionary not released')
        entry = registry['current'][family]
        if entry.get('status', 'RELEASED_EFFECTIVE') != 'RELEASED_EFFECTIVE':
            raise Hold('UNVERIFIED', 'Candidate pointer')
        records = {}
        for record in manifest['files']:
            path = record['path']
            if path in records:
                raise Hold('SOURCE_CONFLICT', 'Duplicate manifest path: ' + path)
            records[path] = record
        source_bytes = git.read_file(entry['path'], source_commit)
        for path, content in [(bootstrap['dictionary_path'], registry_bytes),
                              (entry['path'], source_bytes)]:
            record = records[path]
            blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
            if record.get('sha256'):
                matches = digest(content) == record['sha256'] and len(content) == record['bytes']
            else:
                matches = bool(record.get('blob_sha')) and blob == record['blob_sha']
            if not matches:
                raise Hold('UNVERIFIED', 'Manifest byte/hash mismatch: ' + path)
        return {'status': 'VERIFIED_EFFECTIVE', 'family': family, 'commit': source_commit,
                'manifest_commit': manifest_commit, 'dictionary_commit': source_commit,
                'path': entry['path'], 'sha256': digest(source_bytes),
                'registry_sha256': digest(registry_bytes),
                'manifest_sha256': digest(manifest_bytes), 'authority_evidence': decision['evidence']}
    except Hold:
        raise
    except (OSError, subprocess.SubprocessError) as exc:
        raise Hold('UNAVAILABLE', 'Git unavailable; no cached PASS') from exc
    except (ValueError, KeyError, TypeError, AttributeError, SourceError) as exc:
        raise Hold('UNVERIFIED', 'Incomplete/unsupported native release evidence') from exc
