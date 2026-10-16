"""Trusted local universe snapshot; HTTP callers cannot register instruments."""
from hashlib import sha256
import re
from typing import Literal, Sequence

from fox2.contracts.instruments import Instrument, InstrumentSearchResult


class ApplicationError(Exception):
    def __init__(self, status: int, detail: str):
        self.status, self.detail = status, detail


class InstrumentRegistry:
    def __init__(self, items: Sequence[Instrument] = (), *, source: str | None = None,
                 revision: str | None = None,
                 coverage: Literal['COMPLETE', 'PARTIAL', 'UNKNOWN'] = 'UNKNOWN'):
        values = tuple(Instrument.model_validate_json(i.model_dump_json()) for i in items)
        if coverage not in ('COMPLETE', 'PARTIAL', 'UNKNOWN'):
            raise ValueError('Invalid coverage')
        if values and (not source or not revision or coverage == 'UNKNOWN'):
            raise ValueError('Verified universe provenance required')
        if len({i.instrument_id for i in values}) != len(values) or len({i.symbol for i in values}) != len(values):
            raise ValueError('Ambiguous instrument identity')
        if any(not re.fullmatch(r'[A-Z0-9][A-Z0-9._-]{0,31}', i.symbol) for i in values):
            raise ValueError('Invalid symbol')
        self._items = tuple(sorted(values, key=lambda i: (i.symbol, i.instrument_id)))
        self.source, self.revision, self.coverage = source, revision, coverage
        self._by_symbol = {i.symbol: i for i in values}
        self._by_id = {i.instrument_id: i for i in values}
        # Opaque cursor binds page offset to the exact universe and search.
        self._identity = sha256(repr((source, revision, coverage, self._items)).encode()).hexdigest()

    def contains(self, instrument_id: str) -> bool:
        return instrument_id in self._by_id

    def resolve(self, symbol: str, kind: str = 'STOCK') -> Instrument:
        if not re.fullmatch(r'[A-Z0-9][A-Z0-9._-]{0,31}', symbol):
            raise ApplicationError(422, 'Invalid request')
        item = self._by_symbol.get(symbol)
        if item is None or item.instrument_type != kind:
            raise ApplicationError(404, 'Unknown instrument')
        return item

    def indices(self) -> tuple[Instrument, ...]:
        return tuple(i for i in self._items if i.instrument_type == 'INDEX')

    def search(self, query: str, limit: int, cursor: str | None) -> InstrumentSearchResult:
        if len(query) > 32 or any(ord(c) < 32 for c in query) or not 1 <= limit <= 100:
            raise ApplicationError(422, 'Invalid request')
        matches = [i for i in self._items if i.instrument_type == 'STOCK' and query.upper() in i.symbol]
        signature = sha256((self._identity + query.upper()).encode()).hexdigest()[:32]
        offset = 0
        if cursor is not None:
            if not re.fullmatch(r'[a-f0-9]{32}\.[0-9]{1,10}', cursor):
                raise ApplicationError(422, 'Invalid request')
            digest, raw_offset = cursor.split('.')
            offset = int(raw_offset)
            if digest != signature or not 0 < offset < len(matches):
                raise ApplicationError(422, 'Invalid request')
        end = offset + limit
        return InstrumentSearchResult(items=matches[offset:end], universe_source=self.source,
                                      universe_revision=self.revision, coverage=self.coverage,
                                      cursor=f'{signature}.{end}' if end < len(matches) else None)
