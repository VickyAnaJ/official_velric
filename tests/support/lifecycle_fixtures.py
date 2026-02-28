from __future__ import annotations

from copy import deepcopy
from typing import Any


def build_execution_state_fixture(*, scenario: str = "verify_pass") -> dict[str, Any]:
    """Return deterministic mocked execution-state payloads for lifecycle tests."""
    if scenario not in {"verify_pass", "verify_fail"}:
        raise ValueError(f"unsupported scenario: {scenario}")

    base = {
        "incident_id": "inc-lifecycle-001",
        "execute_status": "executed",
        "action_results": [
            {
                "action_type": "shift_traffic",
                "target": "route:prod_split",
                "status": "succeeded",
                "message": "executed",
            },
            {
                "action_type": "set_deployment_status",
                "target": "deployment:canary",
                "status": "succeeded",
                "message": "executed",
            },
        ],
    }

    if scenario == "verify_fail":
        base["observed_metrics"] = {"vllm:e2e_request_latency_seconds": 1.20}
    else:
        base["observed_metrics"] = {"vllm:e2e_request_latency_seconds": 0.32}

    return deepcopy(base)


def assert_audit_append_only(before: list[dict[str, Any]], after: list[dict[str, Any]]) -> None:
    """Validate append-only semantics for audit entries."""
    if len(after) < len(before):
        raise AssertionError("audit entries shrank; append-only violated")

    prefix = after[: len(before)]
    if prefix != before:
        raise AssertionError("audit prefix changed; existing entries were modified")
