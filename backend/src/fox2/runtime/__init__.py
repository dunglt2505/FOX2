"""Offline composition; no provider transport or credential loading."""
from datetime import datetime, timezone
from collections import deque
from pathlib import Path
from threading import Lock

from fox2.application.registry import InstrumentRegistry
from fox2.application.services import MarketService, WatchlistService
from fox2.config import Settings
from fox2.dsm import DataSourceManager
from fox2.ports.outcomes import PreferenceFailure, Unavailable
from fox2.store import SQLiteStore


class LocalRepository:
    """Lazy explicit-root store; import/factory never creates directories."""
    def __init__(self, settings: Settings, registry: InstrumentRegistry):
        self._settings, self._registry = settings, registry
        self._store = None
        self._lock = Lock()

    def _open(self):
        with self._lock:
            if self._store is None:
                if self._settings.store_root is None:
                    raise ValueError('Explicit store root required')
                self._store = SQLiteStore(Path(self._settings.store_root), profile='INVESTOR',
                                          instrument_registry=self._registry.contains)
            return self._store

    def get_observation(self, instrument_id, capability, at_or_before):
        try:
            return self._open().get_observation(instrument_id, capability, at_or_before)
        except Exception:
            return Unavailable('UNSAFE_STORE')

    def get_preferences(self):
        try:
            return self._open().get_preferences()
        except Exception:
            return PreferenceFailure('UNSAFE_STORE')

    def replace_if_version(self, expected_version, items):
        try:
            return self._open().replace_if_version(expected_version, items)
        except Exception:
            return PreferenceFailure('UNSAFE_STORE')


class OfflineRuntime:
    def __init__(self, settings: Settings, *, registry: InstrumentRegistry | None = None,
                 repository=None, policies=None,
                 clock=lambda: datetime.now(timezone.utc), audit_sink=None):
        self.registry = registry if registry is not None else InstrumentRegistry()
        self.repository = repository if repository is not None else LocalRepository(settings, self.registry)
        # Bounded local diagnostic ledger; DSM records contain hashes/codes, no prices.
        self.selection_audits = deque(maxlen=1000)
        self.dsm = DataSourceManager(self.repository, policies=policies, profile='INVESTOR',
                                     provider_enabled=False, clock=clock,
                                     audit_sink=audit_sink if audit_sink is not None else self.selection_audits.append)
        self.market = MarketService(self.registry, self.dsm, clock)
        self.watchlist = WatchlistService(self.repository)
