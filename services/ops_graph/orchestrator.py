from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from .graph import InMemoryGraphStore, incident_to_response
from .mock_metrics import parse_metrics_payload
from .triage import classify_incident


class MetricsSourceError(RuntimeError):
    """Raised when the metrics source cannot be read safely."""


@dataclass
class OrchestratorResult:
    status_code: int
    payload: dict[str, object]


class IncidentOrchestrator:
    def __init__(self, store: InMemoryGraphStore, metrics_source: "MetricsSource") -> None:
        self._store = store
        self._metrics_source = metrics_source

    def trigger_incident(self, incident_key: str | None) -> OrchestratorResult:
        if incident_key and self._store.has_incident_key(incident_key):
            existing_id = self._store.get_incident_id_by_key(incident_key)
            existing = self._store.get_incident(existing_id)
            assert existing is not None
            data = incident_to_response(existing)
            data["idempotent"] = True
            return OrchestratorResult(status_code=200, payload=data)

        try:
            metrics_payload = self._metrics_source.get_payload()
        except Exception as exc:  # pragma: no cover - tested via integration boundary
            raise MetricsSourceError("Unable to read metrics source") from exc

        metrics = parse_metrics_payload(metrics_payload)
        hypothesis = classify_incident(metrics)
        incident_id = str(uuid4())
        record = self._store.save_incident(
            incident_id=incident_id,
            incident_key=incident_key,
            metrics=metrics,
            hypothesis=hypothesis,
        )
        data = incident_to_response(record)
        data["idempotent"] = False
        return OrchestratorResult(status_code=201, payload=data)


class MetricsSource:
    def get_payload(self) -> str:
        raise NotImplementedError
