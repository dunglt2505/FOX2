"""Foundation diagnostics only; no DSM/store/provider wiring."""
from fastapi import APIRouter
from fox2.config import Settings
from fox2.contracts.health import ProcessHealth, SourceHealth


def health_router(settings: Settings) -> APIRouter:
    router = APIRouter()

    @router.get("/api/health", response_model=ProcessHealth)
    def process_health():
        return ProcessHealth(status="OK", provider_enabled=settings.provider_enabled)

    @router.get("/api/data-sources/health", response_model=list[SourceHealth])
    def source_health():
        return [SourceHealth(capability=capability, readiness="UNAVAILABLE", state="UNKNOWN",
                             gap_state="UNKNOWN", rights_state="UNKNOWN", verified_until=None,
                             reason="NOT_INTEGRATED") for capability in ("QUOTE", "BARS", "INDEX")]

    return router
