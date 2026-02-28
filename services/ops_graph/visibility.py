from __future__ import annotations

from dataclasses import dataclass

from .audit import AuditEntry
from .rollback import RollbackResult
from .verification import VerificationResult

DEFAULT_MANUAL_BASELINE_SECONDS = 30.0 * 60.0


@dataclass(frozen=True)
class MttrSummary:
    time_to_diagnosis_s: float
    time_to_safe_action_s: float
    time_to_recovery_s: float
    manual_baseline_s: float
    improvement_s: float


def _bounded_duration(start: float, end: float | None) -> float:
    if end is None:
        return 1.0
    return max(1.0, end - start)


def compute_mttr(
    *,
    created_at: float,
    execution_completed_at: float | None,
    lifecycle_completed_at: float | None,
    manual_baseline_s: float = DEFAULT_MANUAL_BASELINE_SECONDS,
) -> MttrSummary:
    """Compute MTTR projection values for lifecycle visibility payloads."""
    diagnosis = 1.0
    safe_action = _bounded_duration(created_at, execution_completed_at)
    recovery = _bounded_duration(created_at, lifecycle_completed_at)
    improvement = max(0.0, manual_baseline_s - recovery)

    return MttrSummary(
        time_to_diagnosis_s=diagnosis,
        time_to_safe_action_s=safe_action,
        time_to_recovery_s=recovery,
        manual_baseline_s=manual_baseline_s,
        improvement_s=improvement,
    )


def build_visibility_payload(
    *,
    incident_id: str,
    lifecycle_status: str,
    verification: VerificationResult,
    rollback: RollbackResult,
    audit_entries: tuple[AuditEntry, ...],
    mttr: MttrSummary,
) -> dict[str, object]:
    """Build the polled lifecycle projection with typed fields and plain summary."""
    summary = (
        f"Verification {verification.status}; "
        f"rollback {rollback.status}; "
        f"recovery {mttr.time_to_recovery_s:.2f}s."
    )

    return {
        "incident_id": incident_id,
        "status": lifecycle_status,
        "verification": {
            "status": verification.status,
            "reason": verification.reason,
            "metric": verification.metric,
            "observed_value": verification.observed_value,
            "threshold_seconds": verification.threshold_seconds,
        },
        "rollback": {
            "status": rollback.status,
            "reason": rollback.reason,
            "action_count": len(rollback.actions),
        },
        "audit": [
            {
                "step": entry.step,
                "typed_data": entry.typed_data,
                "plain_summary": entry.plain_summary,
                "timestamp": entry.timestamp,
            }
            for entry in audit_entries
        ],
        "mttr": {
            "time_to_diagnosis_s": mttr.time_to_diagnosis_s,
            "time_to_safe_action_s": mttr.time_to_safe_action_s,
            "time_to_recovery_s": mttr.time_to_recovery_s,
            "manual_baseline_s": mttr.manual_baseline_s,
            "improvement_s": mttr.improvement_s,
        },
        "plain_summary": summary,
    }
