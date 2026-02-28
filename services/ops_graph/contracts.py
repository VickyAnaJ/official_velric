from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

IncidentType = Literal["latency_regression", "capacity_pressure", "manual_review_required"]
PolicyDecisionStatus = Literal["PASS", "POLICY_BLOCKED", "APPROVAL_REQUIRED"]
ActionStatus = Literal["succeeded", "failed", "blocked"]


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
    remediation_plan: "RemediationPlan | None" = None
    policy_decision: "PolicyDecision | None" = None
    action_results: list["ActionResult"] = field(default_factory=list)


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
