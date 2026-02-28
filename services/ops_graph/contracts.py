from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

IncidentType = Literal["latency_regression", "capacity_pressure", "manual_review_required"]


@dataclass(frozen=True)
class IncidentHypothesis:
    incident_type: IncidentType
    confidence: float
    summary: str


@dataclass(frozen=True)
class IncidentRecord:
    incident_id: str
    incident_key: str | None
    status: str
    severity: str
    metrics: dict[str, float]
    hypothesis: IncidentHypothesis
