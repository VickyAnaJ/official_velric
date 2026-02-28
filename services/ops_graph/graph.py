from __future__ import annotations

from dataclasses import asdict, replace
import time

from .contracts import (
    ActionResult,
    AuditEntry,
    IncidentHypothesis,
    IncidentRecord,
    MttrSummary,
    PolicyDecision,
    RemediationPlan,
    RollbackResult,
    VerificationResult,
)


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
            created_at=time.time(),
        )
        self._incidents[incident_id] = record
        if incident_key:
            self._incident_key_index[incident_key] = incident_id
        return record

    def get_incident(self, incident_id: str) -> IncidentRecord | None:
        return self._incidents.get(incident_id)

    def update_execution_state(
        self,
        *,
        incident_id: str,
        plan: RemediationPlan,
        policy_decision: PolicyDecision,
        action_results: list[ActionResult],
    ) -> IncidentRecord:
        existing = self._incidents[incident_id]
        status = "active" if policy_decision.status != "PASS" else "remediating"
        updated = replace(
            existing,
            status=status,
            remediation_plan=plan,
            policy_decision=policy_decision,
            action_results=action_results,
            execution_completed_at=time.time(),
        )
        self._incidents[incident_id] = updated
        return updated

    def update_lifecycle_state(
        self,
        *,
        incident_id: str,
        status: str,
        verification_result: VerificationResult,
        rollback_result: RollbackResult,
        audit_entries: list[AuditEntry],
        mttr_summary: MttrSummary,
    ) -> IncidentRecord:
        existing = self._incidents[incident_id]
        updated = replace(
            existing,
            status=status,
            verification_result=verification_result,
            rollback_result=rollback_result,
            audit_entries=[*existing.audit_entries, *audit_entries],
            mttr_summary=mttr_summary,
            lifecycle_completed_at=time.time(),
        )
        self._incidents[incident_id] = updated
        return updated


def incident_to_response(record: IncidentRecord) -> dict[str, object]:
    return asdict(record)
