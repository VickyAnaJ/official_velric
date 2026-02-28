from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

LATENCY_METRIC = "vllm:e2e_request_latency_seconds"
DEFAULT_THRESHOLD_SECONDS = 0.80


class VerificationError(ValueError):
    """Raised when verification inputs are invalid."""


@dataclass(frozen=True)
class VerificationResult:
    status: str
    reason: str
    metric: str
    observed_value: float
    expected_direction: str
    threshold_seconds: float


def evaluate_recovery(
    observed_metrics: Mapping[str, float],
    *,
    threshold_seconds: float = DEFAULT_THRESHOLD_SECONDS,
    metric: str = LATENCY_METRIC,
) -> VerificationResult:
    """Evaluate whether post-action metrics indicate recovery."""
    if threshold_seconds <= 0:
        raise VerificationError("threshold_seconds must be > 0")

    raw_value = observed_metrics.get(metric)
    if raw_value is None:
        raise VerificationError(f"missing required metric: {metric}")

    observed_value = float(raw_value)
    passed = observed_value <= threshold_seconds

    return VerificationResult(
        status="passed" if passed else "failed",
        reason="latency_recovered" if passed else "latency_above_threshold",
        metric=metric,
        observed_value=observed_value,
        expected_direction="decreasing",
        threshold_seconds=threshold_seconds,
    )
