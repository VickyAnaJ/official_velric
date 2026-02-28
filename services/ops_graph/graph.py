from __future__ import annotations

from dataclasses import asdict

from .contracts import IncidentHypothesis, IncidentRecord


class InMemoryGraphStore:
    """Typed in-memory graph stand-in for SLICE-OPS-01."""

    def __init__(self) -> None:
        self._incidents: dict[str, IncidentRecord] = {}
        self._incident_key_index: dict[str, str] = {}

    def has_incident_key(self, incident_key: str) -> bool:
        return incident_key in self._incident_key_index

    def get_incident_id_by_key(self, incident_key: str) -> str:
        return self._incident_key_index[incident_key]

    def save_incident(
        self,
        *,
        incident_id: str,
        incident_key: str | None,
        metrics: dict[str, float],
        hypothesis: IncidentHypothesis,
        severity: str = "high",
    ) -> IncidentRecord:
        record = IncidentRecord(
            incident_id=incident_id,
            incident_key=incident_key,
            status="active",
            severity=severity,
            metrics=metrics,
            hypothesis=hypothesis,
        )
        self._incidents[incident_id] = record
        if incident_key:
            self._incident_key_index[incident_key] = incident_id
        return record

    def get_incident(self, incident_id: str) -> IncidentRecord | None:
        return self._incidents.get(incident_id)


def incident_to_response(record: IncidentRecord) -> dict[str, object]:
    return asdict(record)
