from __future__ import annotations

from .contracts import IncidentHypothesis

LATENCY_THRESHOLD_SECONDS = 0.8
KV_PRESSURE_THRESHOLD = 0.8


def classify_incident(metrics: dict[str, float]) -> IncidentHypothesis:
    latency = metrics.get("vllm:e2e_request_latency_seconds", 0.0)
    kv_pressure = metrics.get("vllm:kv_cache_usage_perc", 0.0)

    if latency >= LATENCY_THRESHOLD_SECONDS:
        return IncidentHypothesis(
            incident_type="latency_regression",
            confidence=0.92,
            summary="Detected latency regression from p95 latency and load signals.",
        )

    if kv_pressure >= KV_PRESSURE_THRESHOLD:
        return IncidentHypothesis(
            incident_type="capacity_pressure",
            confidence=0.86,
            summary="Detected capacity pressure from high KV cache utilization.",
        )

    return IncidentHypothesis(
        incident_type="manual_review_required",
        confidence=0.5,
        summary="Insufficient confidence for supported incident types; manual review required.",
    )
