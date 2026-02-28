from __future__ import annotations

from .contracts import IncidentRecord, MttrSummary

DEFAULT_MANUAL_BASELINE_SECONDS = 30.0 * 60.0


def compute_mttr(incident: IncidentRecord, manual_baseline_s: float = DEFAULT_MANUAL_BASELINE_SECONDS) -> MttrSummary:
    diagnosis = 1.0
    safe_action = max(1.0, (incident.execution_completed_at or incident.created_at) - incident.created_at)
    recovery = max(1.0, (incident.lifecycle_completed_at or incident.created_at) - incident.created_at)
    improvement = max(0.0, manual_baseline_s - recovery)
    return MttrSummary(
        time_to_diagnosis_s=diagnosis,
        time_to_safe_action_s=safe_action,
        time_to_recovery_s=recovery,
        manual_baseline_s=manual_baseline_s,
        improvement_s=improvement,
    )
