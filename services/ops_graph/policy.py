from __future__ import annotations

from .contracts import PolicyConfig, PolicyDecision, RemediationPlan


class PolicyConfigError(ValueError):
    """Raised when policy config is invalid."""


def validate_policy_config(config: PolicyConfig) -> None:
    if not config.allowlisted_actions:
        raise PolicyConfigError("allowlisted_actions must not be empty")
    if config.confidence_threshold < 0.0 or config.confidence_threshold > 1.0:
        raise PolicyConfigError("confidence_threshold must be between 0.0 and 1.0")


def default_policy_config() -> PolicyConfig:
    return PolicyConfig(
        allowlisted_actions=("shift_traffic", "set_deployment_status", "rollback_config"),
        confidence_threshold=0.80,
        require_approval=False,
    )


def evaluate_policy(
    *,
    plan: RemediationPlan,
    confidence: float,
    config: PolicyConfig,
    approval_token: str | None,
) -> PolicyDecision:
    validate_policy_config(config)

    if confidence < config.confidence_threshold:
        return PolicyDecision(
            status="POLICY_BLOCKED",
            reason="confidence_below_threshold",
            confidence=confidence,
            requires_approval=False,
        )

    for action in plan.actions:
        if action.action_type not in config.allowlisted_actions:
            return PolicyDecision(
                status="POLICY_BLOCKED",
                reason=f"action_not_allowlisted:{action.action_type}",
                confidence=confidence,
                requires_approval=False,
            )

    if config.require_approval and approval_token != "approved":
        return PolicyDecision(
            status="APPROVAL_REQUIRED",
            reason="approval_token_required",
            confidence=confidence,
            requires_approval=True,
        )

    return PolicyDecision(
        status="PASS",
        reason="policy_passed",
        confidence=confidence,
        requires_approval=False,
    )
