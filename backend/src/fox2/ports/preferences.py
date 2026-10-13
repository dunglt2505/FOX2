"""Atomic CAS contract only; storage P2-02, service P2-04.

Validate verified unique IDs (max100), compare expected nonnegative version,
replace list, increment version and timestamp in one transaction. Conflict or
failure preserves the prior list/version. No provider or broker operation.
"""
from typing import Protocol, Sequence
from .outcomes import PreferenceResultOrConflict

class PreferenceRepositoryPort(Protocol):
    def replace_if_version(self, expected_version: int,
                           items: Sequence[str]) -> PreferenceResultOrConflict: ...
