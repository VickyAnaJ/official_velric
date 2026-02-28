from __future__ import annotations

from dataclasses import dataclass

from .audit import build_lifecycle_audit_entries
from .contracts import IncidentRecord, RollbackResult, VerificationResult
from .executor import ActionAdapter, LocalActionAdapter
from .graph import InMemoryGraphStore, incident_to_response
from .rollback import run_rollback
from .verification import evaluate_recovery
from .visibility import compute_mttr


@dataclass
class LifecycleResult:
    status_code: int
    payload: dict[str, object]


class LifecycleOrchestrator:
    def __init__(
        self,
        store: InMemoryGraphStore,
        rollback_adapter: ActionAdapter | None = None,
    ) -> None:
        self._store = store
        self._rollback_adapter = rollback_adapter if rollback_adapter is not None else LocalActionAdapter()

    def process_incident(self, *, incident_id: str, observed_metrics: dict[str, float]) -> LifecycleResult:
        incident = self._store.get_incident(incident_id)
        if incident is None:
            return LifecycleResult(status_code=404, payload={"error": "incident_not_found"})

        if not incident.action_results:
            return LifecycleResult(
                status_code=422,
                payload={"error": "missing_action_results", "detail": "execute step has not run"},
            )

        verification = evaluate_recovery(observed_metrics=observed_metrics)

        rollback_result: RollbackResult
        status = "resolved"
        if verification.status == "failed":
            rollback_result = run_rollback(incident.action_results, adapter=self._rollback_adapter)
            status = "resolved_with_rollback" if rollback_result.status == "completed" else "manual_review_required"
        else:
            rollback_result = RollbackResult(status="not_needed", actions=[], reason="verification_passed")

        audit_entries = build_lifecycle_audit_entries(verification=verification, rollback=rollback_result)
        interim = self._store.update_lifecycle_state(
            incident_id=incident_id,
            status=status,
            verification_result=verification,
            rollback_result=rollback_result,
            audit_entries=audit_entries,
            mttr_summary=compute_mttr(incident),
        )
        finalized = self._store.update_lifecycle_state(
            incident_id=incident_id,
            status=status,
            verification_result=verification,
            rollback_result=rollback_result,
            audit_entries=[],
            mttr_summary=compute_mttr(interim),
        )

        payload = incident_to_response(finalized)
        payload["plain_summary"] = (
            f"Verification {verification.status}; rollback {rollback_result.status}; status {finalized.status}."
        )
        return LifecycleResult(status_code=200, payload=payload)
