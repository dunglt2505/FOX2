"""FOX2-only SQLite repositories implementing the frozen P2-01 ports.

Each call owns its connection and transaction. DELETE journal + FULL sync keeps
crash recovery simple; readers see old or new snapshots, never half an ingest.
Evidence/registry/clock callbacks are trusted local injection points, not DTO
claims. No provider adapter is included. A missing evidence adapter quarantines.
"""
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Callable, Sequence
from uuid import uuid4

from fox2.contracts.market import MarketObservation, Bars, CONTRACT_VERSION
from fox2.contracts.watchlist import WatchlistPreference
from fox2.ports.outcomes import (CommitResult, IngestAudit, Unavailable,
                                PreferenceConflict, PreferenceFailure)
from fox2.validation.schema import MarketValidator
from fox2.validation.semantics import CapabilityContext
from .evidence import PromotionEvidence
from .migrations import migrate


class StoreError(ValueError):
    """Configuration or explicit administrative failure; sanitized message."""


def utc(value: datetime) -> str:
    if not isinstance(value, datetime) or value.utcoffset() != timedelta(0):
        raise StoreError('UTC_REQUIRED')
    return value.isoformat(timespec='microseconds')


def encode(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value) -> str:
    return hashlib.sha256(encode(value).encode()).hexdigest()


def _safe_root(root: Path) -> Path:
    root = Path(root)
    if not root.is_absolute() or not root.name.lower().startswith('fox2'):
        raise StoreError('EXPLICIT_FOX2_ROOT_REQUIRED')
    # Reject legacy roots, aliases/symlinks and every Git working tree ancestor.
    for item in (root, *root.parents):
        if item.is_symlink() or item.is_junction() or (item / '.git').exists():
            raise StoreError('UNSAFE_STORE_PATH')
    resolved = root.resolve()
    text = str(resolved).replace('\\', '/').lower()
    if re.search(r'(?:^|/)data/fox(?:/|$)', text):
        raise StoreError('LEGACY_STORE_FORBIDDEN')
    return resolved


class SQLiteStore:
    def __init__(self, root: Path, *, profile: str = 'INVESTOR',
                 instrument_registry: Callable[[str], bool],
                 clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
                 evidence: Callable[[MarketObservation], PromotionEvidence | None] = lambda candidate: None,
                 busy_timeout_ms: int = 250, fault_hook: Callable[[str], None] = lambda stage: None):
        if profile not in ('INVESTOR', 'ISOLATED_TEST'):
            raise StoreError('INVALID_PROFILE')
        if type(busy_timeout_ms) is not int or not 0 <= busy_timeout_ms <= 5000:
            raise StoreError('INVALID_BUSY_TIMEOUT')
        self.root = _safe_root(root)
        self.path = self.root / 'fox2.sqlite3'
        if self.path.is_symlink():
            raise StoreError('UNSAFE_STORE_PATH')
        self.profile, self.registry, self.clock = profile, instrument_registry, clock
        self.evidence, self.timeout, self.hook = evidence, busy_timeout_ms, fault_hook
        self.root.mkdir(parents=True, exist_ok=True)
        with self._connection() as connection:
            migrate(connection, profile, fault_hook)

    @contextmanager
    def _connection(self):
        if _safe_root(self.root) != self.root or self.path.is_symlink():
            raise StoreError('UNSAFE_STORE_PATH')
        connection = sqlite3.connect(self.path, timeout=self.timeout / 1000, isolation_level=None)
        try:
            connection.execute('PRAGMA foreign_keys=ON')
            connection.execute(f'PRAGMA busy_timeout={self.timeout}')
            connection.execute('PRAGMA synchronous=FULL')
            if connection.execute('PRAGMA journal_mode').fetchone()[0].lower() != 'delete':
                raise StoreError('UNSUPPORTED_JOURNAL_MODE')
            yield connection
        finally:
            if connection.in_transaction:
                connection.rollback()
            connection.close()

    @contextmanager
    def _transaction(self, write=False):
        with self._connection() as connection:
            connection.execute('BEGIN IMMEDIATE' if write else 'BEGIN')
            try:
                yield connection
                connection.commit()
            except BaseException:
                connection.rollback()
                raise

    def close(self):
        """No persistent connections or background workers are retained."""

    def integrity(self) -> dict:
        with self._transaction() as c:
            return {'integrity_check': c.execute('PRAGMA integrity_check').fetchone()[0],
                    'foreign_key_check': c.execute('PRAGMA foreign_key_check').fetchall(),
                    'migration': c.execute('SELECT version,checksum FROM schema_migrations').fetchall(),
                    'journal_mode': c.execute('PRAGMA journal_mode').fetchone()[0],
                    'synchronous': c.execute('PRAGMA synchronous').fetchone()[0]}

    def _identify(self, o: MarketObservation):
        kind = getattr(o.payload, 'kind', None)
        capability = {'quote': 'QUOTE', 'bars': 'BARS', 'index_summary': 'INDEX'}.get(kind)
        if not capability or not all((o.instrument_id, o.source_id, o.origin_provider,
                                      o.board_id, o.record_id)) or o.venue == 'UNKNOWN':
            raise StoreError('INVALID_IDENTITY')
        if not self.registry(o.instrument_id):
            raise StoreError('UNKNOWN_INSTRUMENT')
        identity = [capability, o.source_id, o.origin_provider, o.instrument_id,
                    o.venue, o.board_id, o.price_basis, o.adjustment_version,
                    o.payload.timeframe if isinstance(o.payload, Bars) else None]
        series_key = digest(identity)
        if isinstance(o.payload, Bars):
            if not o.payload.items:
                raise StoreError('EMPTY_BARS')
            starts = [utc(b.start_at) for b in o.payload.items]
            if len(set(starts)) != len(starts):
                raise StoreError('DUPLICATE_BAR_IDENTITY')
            parts = []
            for bar in o.payload.items:
                part = o.model_copy(update={'payload': o.payload.model_copy(update={'items': [bar.model_copy(deep=True)]})}, deep=True)
                parts.append((utc(bar.start_at), utc(bar.start_at), part))
        else:
            if o.event_at is None:
                raise StoreError('UNKNOWN_EVENT_IDENTITY')
            parts = [(o.record_id, utc(o.event_at), o)]
        return capability, series_key, identity, parts

    def _fingerprint(self, o):
        values = o.model_dump(mode='json', by_alias=True)
        for key in ('record_id', 'revision', 'received_at', 'first_available_at',
                    'selection_audit_id', 'selection_reason', 'retrieval_channel', 'rights'):
            values.pop(key)
        if isinstance(o.payload, Bars):
            # Bar item revision is caller-owned metadata, not market identity.
            for bar in values['payload']['items']:
                bar.pop('revision')
            values['payload'].pop('from'); values['payload'].pop('to')
            values['payload'].pop('gaps')
        return digest(values)

    @staticmethod
    def _rights_ok(row, now):
        return (row is not None and row['revoked'] == 0 and row['read_state'] == 'VERIFIED'
                and row['retained_state'] == 'VERIFIED' and bool(row['evidence_ref'])
                and row['verified_until'] is not None and row['verified_until'] > now)

    @staticmethod
    def _latest_rights(c, series):
        c.row_factory = sqlite3.Row
        return c.execute('SELECT * FROM rights_registry WHERE series_key=? ORDER BY rights_id DESC LIMIT 1', (series,)).fetchone()

    def _eligibility(self, o, proof, capability, now):
        context = proof.context if proof else CapabilityContext(capability, now, use_context='RETAINED_USE')
        if context.capability != capability or context.evaluated_at != now or context.use_context != 'RETAINED_USE':
            raise StoreError('INVALID_TRUSTED_CONTEXT')
        verdict = MarketValidator().validate_semantics(o, context)
        if verdict.status == 'FAIL':
            evidence_errors = {'SESSION_MAPPING_UNVERIFIED', 'COVERAGE_UNVERIFIED', 'ADJUSTMENT_UNVERIFIED',
                               'LIVE_TRANSPORT', 'LIVE_FRESHNESS_UNKNOWN', 'FRESH_SESSION_GAP'}
            if set(verdict.errors) <= evidence_errors:
                return False
            raise StoreError('INVALID_CANDIDATE')
        evidence_ok = bool(proof and proof.evidence_ref and proof.identity_verified
                           and proof.lifecycle_verified and type(proof.order) is int and proof.order >= 0)
        quality_ok = o.quality == 'VALID' and o.mapping_state == 'VERIFIED' and o.price_basis not in ('UNKNOWN',)
        rights_ok = (o.rights.read == 'VERIFIED' and o.rights.retained_use == 'VERIFIED'
                     and bool(o.rights.evidence_ref) and o.rights.verified_until is not None
                     and o.rights.verified_until > now)
        if isinstance(o.payload, Bars):
            quality_ok = quality_ok and bool(o.calendar_version and o.session and context.session_mapping_verified)
            quality_ok = quality_ok and all(b.provisional is not None for b in o.payload.items)
        # Missing market amounts may be PARTIAL semantically and remain null.
        # Promotion still requires explicit completeness/mapping/rights evidence.
        return evidence_ok and quality_ok and rights_ok and not any(x.startswith('UNVERIFIED:') for x in verdict.unknowns)

    def _promotable(self, old, new, proof, part):
        if old is None:
            return proof.predecessor_record_id is None
        if old['logical_key'] == new['logical_key']:
            if proof.predecessor_record_id != old['record_id'] or proof.order <= old['source_order']:
                return False
            if isinstance(part.payload, Bars):
                previous = json.loads(old['payload_json'])['payload']['items'][0]
                if previous['provisional'] is False and part.payload.items[0].provisional is not False:
                    return False
            return True
        if proof.predecessor_record_id is not None:
            return False
        # No arrival/id/hash tie breaker for different events.
        order_advances = proof.order >= old['source_order'] if isinstance(part.payload, Bars) else proof.order > old['source_order']
        return new['market_at'] > old['market_at'] and order_advances

    def append_and_promote(self, candidate: MarketObservation, ingest_audit: IngestAudit) -> CommitResult:
        invalid = CommitResult('REJECTED', None, None, False, 'INVALID_CANDIDATE')
        try:
            if not isinstance(candidate, MarketObservation) or not isinstance(ingest_audit, IngestAudit):
                return invalid
            original = candidate.model_dump(mode='json', by_alias=True)
            candidate_hash = digest(original)
            if not ingest_audit.audit_id or not re.fullmatch('[a-f0-9]{64}', ingest_audit.raw_sha256):
                return invalid
            now = self.clock(); stamp = utc(now)
            capability, series, identity, parts = self._identify(candidate)
            proofs = [self.evidence(part.model_copy(deep=True)) for _, _, part in parts]
            with self._transaction(write=True) as c:
                c.row_factory = sqlite3.Row
                self.hook('ingest_begin')
                prior = c.execute('SELECT * FROM ingest_receipts WHERE audit_id=?', (ingest_audit.audit_id,)).fetchone()
                if prior:
                    if prior['raw_sha256'] != ingest_audit.raw_sha256 or prior['candidate_sha256'] != candidate_hash:
                        return invalid
                    return CommitResult(**json.loads(prior['result_json']))
                # Capture only actual trusted local receipt; caller cannot backdate.
                received_stamp = utc(ingest_audit.received_at)
                # A trusted receipt may precede verification by a bounded local
                # processing interval. Persist verification time as availability,
                # never the caller's historical availability claim.
                if not timedelta(0) <= now - ingest_audit.received_at <= timedelta(seconds=5):
                    return invalid
                latest = c.execute('SELECT MAX(first_available_at) FROM observations').fetchone()[0]
                if latest and stamp < latest:
                    return invalid
                if candidate.profile != self.profile or (self.profile == 'INVESTOR' and
                        (candidate.data_mode == 'SYNTHETIC' or candidate.retrieval_channel == 'TEST_FIXTURE')):
                    return invalid
                normalized = candidate.model_copy(update={'received_at': ingest_audit.received_at, 'first_available_at': now,
                                                          'record_id': 'pending-local-id', 'revision': 1}, deep=True)
                # Preserve upstream source identity in original_json; local IDs are independent.
                envelope = {'contract_version': CONTRACT_VERSION, 'request_id': ingest_audit.audit_id,
                            'generated_at': stamp, 'data': normalized.model_dump(mode='json', by_alias=True)}
                shape = MarketValidator().validate_shape(envelope, normalized.payload.kind)
                if not shape.shape_passed:
                    return invalid
                prepared = []
                for (logical, market_at, part), proof in zip(parts, proofs):
                    validated_part = part.model_copy(update={'received_at': ingest_audit.received_at, 'first_available_at': now,
                                                            'record_id': 'pending-local-id', 'revision': 1}, deep=True)
                    eligible = self._eligibility(validated_part, proof, capability, now)
                    fingerprint = self._fingerprint(part)
                    duplicate = c.execute('SELECT * FROM observations WHERE series_key=? AND logical_key=? AND fingerprint=?',
                                          (series, logical, fingerprint)).fetchone()
                    # Duplicate polling can carry the original known availability,
                    # or omit it, but cannot introduce a new historical claim.
                    allowed_claims = {None, stamp}
                    if duplicate:
                        allowed_claims.add(duplicate['first_available_at'])
                    if candidate.first_available_at is not None and utc(candidate.first_available_at) not in allowed_claims:
                        return invalid
                    prepared.append((logical, market_at, part, fingerprint, duplicate, proof, eligible))
                self.hook('ingest_validated')
                c.execute('INSERT OR IGNORE INTO instruments VALUES(?)', (candidate.instrument_id,))
                c.execute('INSERT OR IGNORE INTO series VALUES(?,?,?,?)', (series, candidate.instrument_id, capability, encode(identity)))
                self.hook('ingest_identity')
                if self._latest_rights(c, series) is None:
                    rights = candidate.rights
                    c.execute('INSERT INTO rights_registry(series_key,read_state,retained_state,evidence_ref,verified_until,observed_at,revoked) VALUES(?,?,?,?,?,?,0)',
                              (series, rights.read, rights.retained_use, rights.evidence_ref,
                               utc(rights.verified_until) if rights.verified_until else None, stamp))
                rights_ok = self._rights_ok(self._latest_rights(c, series), stamp)
                self.hook('ingest_rights')
                # Receipt exists before dependent audit rows; transaction hides it until commit.
                # Final result must be known before immutable receipt insertion.
                results, audit_rows, gaps = [], [], []
                for logical, market_at, part, fingerprint, duplicate, proof, eligible in prepared:
                    if duplicate:
                        results.append((duplicate['record_id'], duplicate['revision'], False, True))
                        audit_rows.append((duplicate['record_id'], False, 'DUPLICATE'))
                        continue
                    local_revision = c.execute('SELECT COALESCE(MAX(revision),0)+1 FROM observations WHERE series_key=? AND logical_key=?', (series, logical)).fetchone()[0]
                    record = str(uuid4())
                    stored = part.model_copy(update={'record_id': record, 'revision': local_revision,
                                                     'received_at': ingest_audit.received_at, 'first_available_at': now}, deep=True)
                    if isinstance(stored.payload, Bars):
                        stored = stored.model_copy(update={'payload': stored.payload.model_copy(update={
                            'items': [stored.payload.items[0].model_copy(update={'revision': local_revision})]})})
                    predecessor = proof.predecessor_record_id if proof else None
                    if predecessor:
                        parent = c.execute('SELECT series_key,logical_key FROM observations WHERE record_id=?', (predecessor,)).fetchone()
                        if parent is None or tuple(parent) != (series, logical):
                            raise StoreError('CROSS_SERIES_LINEAGE')
                    can_promote = bool(eligible and rights_ok)
                    ev = {'ref': proof.evidence_ref, 'order': proof.order, 'lifecycle_verified': proof.lifecycle_verified} if proof else {}
                    c.execute('INSERT INTO observations VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                              (record, series, logical, fingerprint, local_revision, stamp, market_at,
                               proof.order if proof else None, predecessor, int(can_promote),
                               encode(stored.model_dump(mode='json', by_alias=True)), encode(original), encode(ev)))
                    self.hook('ingest_observation')
                    if isinstance(stored.payload, Bars):
                        bar = stored.payload.items[0]
                        c.execute('INSERT INTO bar_revisions VALUES(?,?,?)', (record, logical, bar.provisional))
                    self.hook('ingest_bar')
                    old = c.execute('SELECT o.* FROM current_projection p JOIN observations o ON o.record_id=p.record_id WHERE p.series_key=?', (series,)).fetchone()
                    new = {'logical_key': logical, 'market_at': market_at}
                    promoted = bool(can_promote and self._promotable(old, new, proof, stored))
                    if promoted:
                        c.execute('INSERT INTO current_projection VALUES(?,?) ON CONFLICT(series_key) DO UPDATE SET record_id=excluded.record_id', (series, record))
                        c.execute('INSERT INTO projection_history(series_key,record_id,promoted_at) VALUES(?,?,?)', (series, record, stamp))
                    self.hook('ingest_projection')
                    reason = 'VALID' if promoted else 'AMBIGUOUS_ORDER'
                    results.append((record, local_revision, promoted, False))
                    audit_rows.append((record, promoted, reason))
                    if not promoted:
                        gaps.append((record, 'RIGHTS_BLOCKED' if not rights_ok else 'AMBIGUOUS_ORDER', '{}'))
                all_duplicate = all(row[3] for row in results)
                promoted = any(row[2] for row in results)
                # Singular frozen outcome identifies the first input item;
                # receipt_records retains every item linkage for batched bars.
                result = CommitResult('UNCHANGED' if all_duplicate else 'COMMITTED', results[0][0], results[0][1],
                                      promoted, 'DUPLICATE' if all_duplicate else 'VALID' if promoted else 'AMBIGUOUS_ORDER')
                c.execute('INSERT INTO ingest_receipts VALUES(?,?,?,?,?,?,?,?)', (ingest_audit.audit_id, received_stamp,
                          ingest_audit.raw_sha256, candidate_hash, result.status, result.reason, encode(asdict(result)), encode(original)))
                self.hook('ingest_receipt')
                for record, promoted_item, reason in audit_rows:
                    c.execute('INSERT INTO receipt_records VALUES(?,?)', (ingest_audit.audit_id, record))
                    c.execute('INSERT INTO selection_audit(audit_id,record_id,promoted,reason) VALUES(?,?,?,?)',
                              (ingest_audit.audit_id, record, int(promoted_item), reason))
                self.hook('ingest_audit')
                if isinstance(candidate.payload, Bars):
                    gaps += [(None, g.reason, encode(g.model_dump(mode='json', by_alias=True))) for g in candidate.payload.gaps]
                for record, reason, detail in gaps:
                    c.execute('INSERT INTO gaps(audit_id,record_id,reason,detail_json) VALUES(?,?,?,?)', (ingest_audit.audit_id, record, reason, detail))
                self.hook('ingest_gaps')
                self.hook('ingest_commit')
                return result
        except (sqlite3.Error, OSError):
            return CommitResult('UNAVAILABLE', None, None, False, 'UNSAFE_STORE')
        except (ValueError, TypeError, AttributeError, OverflowError):
            return invalid

    def get_observation(self, instrument_id, capability, at_or_before):
        try:
            if capability not in ('QUOTE', 'BARS', 'INDEX') or not instrument_id:
                return Unavailable('UNKNOWN')
            now = utc(self.clock())
            cutoff = utc(at_or_before) if at_or_before is not None else now
            if cutoff > now:
                return Unavailable('UNKNOWN')
            with self._transaction() as c:
                c.row_factory = sqlite3.Row
                rows = c.execute('''SELECT o.* FROM projection_history h JOIN observations o ON o.record_id=h.record_id
                    JOIN series s ON s.series_key=h.series_key
                    WHERE s.instrument_id=? AND s.capability=? AND h.promoted_at<=? AND o.first_available_at<=?
                    AND h.promotion_id=(SELECT MAX(h2.promotion_id) FROM projection_history h2
                    WHERE h2.series_key=h.series_key AND h2.promoted_at<=?)''',
                                 (instrument_id, capability, cutoff, cutoff, cutoff)).fetchall()
                self.hook('read_snapshot')
                if not rows:
                    return Unavailable('NOT_FOUND')
                # Never fall back across an unauthorized series.
                if any(not self._rights_ok(self._latest_rights(c, row['series_key']), now) for row in rows):
                    return Unavailable('RIGHTS_BLOCKED')
                if len(rows) != 1:
                    return Unavailable('UNKNOWN')
                o = MarketObservation.model_validate_json(rows[0]['payload_json'])
                if o.profile != self.profile or (self.profile == 'INVESTOR' and
                        (o.data_mode == 'SYNTHETIC' or o.retrieval_channel == 'TEST_FIXTURE')):
                    return Unavailable('UNSAFE_STORE')
                if self.profile == 'INVESTOR':
                    o = o.model_copy(update={'retrieval_channel': 'LOCAL_STORE'})
                return o
        except (sqlite3.Error, OSError, ValueError, TypeError):
            return Unavailable('UNSAFE_STORE')

    def revoke_rights(self, series_key: str, evidence_ref: str):
        """Explicit local trusted revocation; polling cannot re-grant rights."""
        if not evidence_ref:
            raise StoreError('EVIDENCE_REQUIRED')
        try:
            with self._transaction(write=True) as c:
                if self._latest_rights(c, series_key) is None:
                    raise StoreError('UNKNOWN_SERIES')
                c.execute('INSERT INTO rights_registry(series_key,read_state,retained_state,evidence_ref,verified_until,observed_at,revoked) VALUES(?,?,?,?,?,?,1)',
                          (series_key, 'BLOCKED', 'BLOCKED', evidence_ref, None, utc(self.clock())))
        except sqlite3.Error:
            raise StoreError('UNSAFE_STORE') from None

    def get_preferences(self):
        try:
            with self._transaction() as c:
                row = c.execute('SELECT version,items_json,updated_at FROM watchlist_preferences WHERE singleton=1').fetchone()
                return WatchlistPreference.model_validate_json(encode({'version': row[0], 'items': json.loads(row[1]), 'updated_at': row[2]}))
        except (sqlite3.Error, ValueError, OSError):
            return PreferenceFailure('UNSAFE_STORE')

    def replace_if_version(self, expected_version: int, items: Sequence[str]):
        try:
            if type(expected_version) is not int or expected_version < 0 or isinstance(items, (str, bytes)):
                return PreferenceFailure('INVALID_ITEMS')
            values = list(items)
            if len(values) > 100 or any(type(i) is not str or not i for i in values) or len(set(values)) != len(values):
                return PreferenceFailure('INVALID_ITEMS')
            if any(not self.registry(i) for i in values):
                return PreferenceFailure('UNKNOWN_INSTRUMENT')
            stamp = utc(self.clock())
            with self._transaction(write=True) as c:
                self.hook('preference_begin')
                version = c.execute('SELECT version FROM watchlist_preferences WHERE singleton=1').fetchone()[0]
                if version != expected_version:
                    return PreferenceConflict(version)
                self.hook('preference_validated')
                c.execute('UPDATE watchlist_preferences SET version=?,items_json=?,updated_at=? WHERE singleton=1 AND version=?',
                          (version + 1, encode(values), stamp, version))
                self.hook('preference_updated')
                self.hook('preference_commit')
                return WatchlistPreference.model_validate_json(encode({'version': version + 1, 'items': values, 'updated_at': stamp}))
        except (sqlite3.Error, OSError):
            return PreferenceFailure('UNSAFE_STORE')
        except (ValueError, TypeError):
            return PreferenceFailure('INVALID_ITEMS')
