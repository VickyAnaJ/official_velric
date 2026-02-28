from __future__ import annotations

import time

from .contracts import AuditEntry, RollbackResult, VerificationResult


def build_lifecycle_audit_entries(
    *,
    verification: VerificationResult,
    rollback: RollbackResult,
) -> list[AuditEntry]:
    now = time.time()
    entries = [
        AuditEntry(
            step="verify",
            summary=(
                f"Verification {verification.status}: {verification.reason}; "
                f"latency={verification.observed_latency_seconds:.3f}s threshold={verification.threshold_seconds:.3f}s"
            ),
            timestamp=now,
        )
    ]

    if rollback.status != "not_needed":
        entries.append(
            AuditEntry(
                step="rollback",
                summary=f"Rollback {rollback.status}: {rollback.reason}",
                timestamp=now,
            )
        )

    entries.append(
        AuditEntry(
            step="audit",
            summary="Lifecycle audit entries appended.",
            timestamp=now,
        )
    )
    return entries
