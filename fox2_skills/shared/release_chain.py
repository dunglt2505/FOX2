"""Release-chain decision engine. Only a trusted host can supply authority facts.

Git content, serialized requests and conditional technical baselines cannot create
an AuthoritySnapshot. Snapshot production/approval remains an external trust boundary.
"""
from dataclasses import dataclass
import json
import re
from .core import digest


@dataclass(frozen=True)
class Ownership:
    family: str
    path: str
    semantic_owner: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class ApprovedRelease:
    identity: str
    status: str
    scope: str
    manifest_commit: str
    manifest_path: str
    manifest_sha256: str
    source_commit: str
    dictionary_sha256: str
    ownership: tuple[Ownership, ...]
    release_evidence: tuple[str, ...]
    supersedes: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuthoritySnapshot:
    repository: str
    scope: str
    cutoff: str
    root_evidence: tuple[str, ...]
    complete_inventory_evidence: tuple[str, ...]
    allowed_commits: frozenset[str]
    releases: tuple[ApprovedRelease, ...]


class ReleaseChainVerifier:
    """Called by native_registry.bind; fetch fresh host evidence on every call.

    authority_provider(scope, cutoff) returns an independently verified complete
    AuthoritySnapshot, or None. It must never deserialize task-supplied claims
    into trusted facts. Evidence strings are provenance, not self-authenticating
    certificates. No default provider, registry writer or promotion exists here.
    """
    def __init__(self, scope, cutoff, authority_provider=None):
        self.scope, self.cutoff, self.provider = scope, cutoff, authority_provider

    def __call__(self, bootstrap, dictionary_bytes, manifest_bytes, family):
        def hold(reason, status='AUTHORITY_UNVERIFIED'):
            return {'status': status, 'reason': reason, 'evidence': []}
        try:
            dictionary, manifest = json.loads(dictionary_bytes), json.loads(manifest_bytes)
            source = manifest.get('source_set_head', bootstrap['commit'])
            observed = {'manifest_commit': bootstrap['commit'], 'source_commit': source,
                        'dictionary_sha256': digest(dictionary_bytes),
                        'manifest_sha256': digest(manifest_bytes)}
            if not re.fullmatch('[a-f0-9]{40}', source):
                return hold('Non-immutable source commit')
            if dictionary.get('project', {}).get('repository') != 'dunglt2505/FOX2':
                return hold('Repository scope mismatch', 'SOURCE_CONFLICT')
            if dictionary.get('dictionary_id') != 'FOX2_PROJECT_DICTIONARY':
                return hold('Dictionary identity unsupported')
            if self.provider is None:
                return {**hold('Conditional baseline has no independently certified authority snapshot'),
                        'observed': observed}
            snapshot = self.provider(self.scope, self.cutoff)
            if not isinstance(snapshot, AuthoritySnapshot):
                return hold('Trusted authority provider has no verified snapshot')
            if (snapshot.repository != 'dunglt2505/FOX2' or snapshot.scope != self.scope
                    or snapshot.cutoff != self.cutoff):
                return hold('Authority snapshot does not apply to this task/cutoff')
            if not snapshot.root_evidence or not snapshot.complete_inventory_evidence:
                return hold('Trust root or complete competing-release inventory evidence missing')
            if source not in snapshot.allowed_commits or bootstrap['commit'] not in snapshot.allowed_commits:
                return hold('Immutable ref is outside the authorized release closure')
            releases = {r.identity: r for r in snapshot.releases}
            if len(releases) != len(snapshot.releases):
                return hold('Duplicate release identities', 'SOURCE_CONFLICT')
            applicable = {k:r for k,r in releases.items() if r.scope == self.scope and r.status == 'RELEASED_EFFECTIVE'}
            def ancestors(identity, trail=()):
                if identity in trail:
                    raise ValueError('Supersession cycle')
                release = releases[identity]
                result = set()
                for parent in release.supersedes:
                    if parent not in applicable:
                        raise ValueError('Missing or inapplicable released predecessor')
                    result.add(parent)
                    result.update(ancestors(parent, trail+(identity,)))
                return result
            superseded = set()
            for identity in applicable:
                superseded.update(ancestors(identity))
            candidates = [r for k,r in applicable.items() if k not in superseded
                          and any(o.family == family for o in r.ownership)]
            if len(candidates) > 1:
                return hold('Competing unsuperseded EFFECTIVE releases for family', 'SOURCE_CONFLICT')
            if not candidates:
                return hold('No applicable current EFFECTIVE release for family')
            release = candidates[0]
            if (release.manifest_commit != bootstrap['commit'] or release.manifest_path != bootstrap['manifest_path']
                    or release.source_commit != source or release.manifest_sha256 != digest(manifest_bytes)
                    or release.dictionary_sha256 != digest(dictionary_bytes)):
                return hold('Observed anchor is superseded or differs from authorized release')
            owners = [o for o in release.ownership if o.family == family]
            if (len(owners) != 1 or not owners[0].semantic_owner or not owners[0].evidence
                    or not release.release_evidence):
                return hold('Owning semantic source/release approval evidence missing')
            entry = dictionary['current'][family]
            if owners[0].path != entry['path']:
                return hold('Dictionary conflicts with semantic owner path', 'SOURCE_CONFLICT')
            if dictionary.get('status') != 'RELEASED_EFFECTIVE' or entry.get('status','RELEASED_EFFECTIVE') != 'RELEASED_EFFECTIVE':
                return hold('Dictionary or source is Candidate/unreleased')
            # The byte adapter subsequently enforces the manifest file records.
            return {'status':'VERIFIED_EFFECTIVE', 'release_identity':release.identity,
                    'evidence':list(snapshot.root_evidence + snapshot.complete_inventory_evidence
                                    + release.release_evidence + owners[0].evidence), 'observed':observed}
        except (ValueError, KeyError, TypeError, AttributeError):
            return hold('Incomplete/invalid release-chain evidence')
