from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

IncidentType = Literal["latency_regression", "capacity_pressure", "manual_review_required"]
PolicyDecisionStatus = Literal["PASS", "POLICY_BLOCKED", "APPROVAL_REQUIRED"]
ActionStatus = Literal["succeeded", "failed", "blocked"]
VerificationStatus = Literal["passed", "failed"]
RollbackStatus = Literal["not_needed", "completed", "failed"]


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
    created_at: float = 0.0
    remediation_plan: "RemediationPlan | None" = None
    policy_decision: "PolicyDecision | None" = None
    action_results: list["ActionResult"] = field(default_factory=list)
    verification_result: "VerificationResult | None" = None
    rollback_result: "RollbackResult | None" = None
    audit_entries: list["AuditEntry"] = field(default_factory=list)
    mttr_summary: "MttrSummary | None" = None
    execution_completed_at: float | None = None
    lifecycle_completed_at: float | None = None


@dataclass(frozen=True)
class PlanAction:
    action_type: str
    target: str
    params: dict[str, float | int | str | bool]


@dataclass(frozen=True)
class RemediationPlan:
    plan_id: str
    incident_id: str
    actions: list[PlanAction]
    verification_condition: str
    rollback_required: bool


@dataclass(frozen=True)
class PolicyConfig:
    allowlisted_actions: tuple[str, ...]
    confidence_threshold: float
    require_approval: bool


@dataclass(frozen=True)
class PolicyDecision:
    status: PolicyDecisionStatus
    reason: str
    confidence: float
    requires_approval: bool


@dataclass(frozen=True)
class ActionResult:
    action_type: str
    target: str
    status: ActionStatus
    message: str


@dataclass(frozen=True)
class VerificationResult:
    status: VerificationStatus
    reason: str
    observed_latency_seconds: float
    threshold_seconds: float


@dataclass(frozen=True)
class RollbackResult:
    status: RollbackStatus
    actions: list[ActionResult]
    reason: str


@dataclass(frozen=True)
class AuditEntry:
    step: str
    summary: str
    timestamp: float


@dataclass(frozen=True)
class MttrSummary:
    time_to_diagnosis_s: float
    time_to_safe_action_s: float
    time_to_recovery_s: float
    manual_baseline_s: float
    improvement_s: float
