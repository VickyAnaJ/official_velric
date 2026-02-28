from __future__ import annotations


def fixed_incident_key(seed: int = 1) -> str:
    return f"incident-{seed:04d}"


def fixed_env() -> dict[str, str]:
    return {
        "APP_ENV": "development",
        "LOG_LEVEL": "info",
        "ANTHROPIC_API_KEY": "test-key",
    }
