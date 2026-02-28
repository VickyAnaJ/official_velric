from __future__ import annotations

from .contracts import VerificationResult

DEFAULT_LATENCY_THRESHOLD_SECONDS = 0.8


def evaluate_recovery(
    *,
    observed_metrics: dict[str, float],
    threshold_seconds: float = DEFAULT_LATENCY_THRESHOLD_SECONDS,
) -> VerificationResult:
    observed_latency = float(observed_metrics.get("vllm:e2e_request_latency_seconds", 0.0))
    passed = observed_latency <= threshold_seconds
    return VerificationResult(
        status="passed" if passed else "failed",
        reason="latency_recovered" if passed else "latency_above_threshold",
        observed_latency_seconds=observed_latency,
        threshold_seconds=threshold_seconds,
    )
