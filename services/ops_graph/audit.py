from __future__ import annotations

import time
from dataclasses import dataclass

from .rollback import RollbackResult
from .verification import VerificationResult


@dataclass(frozen=True)
class AuditEntry:
    step: str
    typed_data: dict[str, object]
    plain_summary: str
    timestamp: float


def build_lifecycle_audit_entries(
    *,
    verification: VerificationResult,
    rollback: RollbackResult,
    now: float | None = None,
) -> tuple[AuditEntry, ...]:
    """Build append-only lifecycle audit entries from verification and rollback outcomes."""
    timestamp = time.time() if now is None else float(now)

    entries: list[AuditEntry] = [
        AuditEntry(
            step="verify",
            typed_data={
                "status": verification.status,
                "reason": verification.reason,
                "metric": verification.metric,
                "observed_value": verification.observed_value,
                "threshold_seconds": verification.threshold_seconds,
            },
            plain_summary=(
                f"Verification {verification.status}: {verification.reason}; "
                f"{verification.metric}={verification.observed_value:.3f} "
                f"(threshold {verification.threshold_seconds:.3f})"
            ),
            timestamp=timestamp,
        )
    ]

    if rollback.status != "not_needed":
        entries.append(
            AuditEntry(
                step="rollback",
                typed_data={
                    "status": rollback.status,
                    "reason": rollback.reason,
                    "action_count": len(rollback.actions),
                },
                plain_summary=f"Rollback {rollback.status}: {rollback.reason}",
                timestamp=timestamp,
            )
        )

    entries.append(
        AuditEntry(
            step="audit",
            typed_data={"status": "appended", "entry_count": len(entries) + 1},
            plain_summary="Lifecycle audit entries appended.",
            timestamp=timestamp,
        )
    )

    return tuple(entries)


def append_audit_entries(existing: tuple[AuditEntry, ...], new_entries: tuple[AuditEntry, ...]) -> tuple[AuditEntry, ...]:
    """Append entries without mutating existing history."""
    return existing + new_entries
