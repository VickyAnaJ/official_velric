from __future__ import annotations

from dataclasses import dataclass
import os


class ConfigError(ValueError):
    """Raised when required runtime configuration is missing or invalid."""


@dataclass(frozen=True)
class AppConfig:
    app_env: str
    log_level: str
    anthropic_api_key: str | None


def load_config(env: dict[str, str] | None = None) -> AppConfig:
    source = env if env is not None else os.environ
    app_env = source.get("APP_ENV", "").strip()
    if not app_env:
        raise ConfigError("APP_ENV is required")

    log_level = source.get("LOG_LEVEL", "info").strip().lower() or "info"
    if log_level not in {"debug", "info", "warning", "error"}:
        raise ConfigError("LOG_LEVEL must be one of debug|info|warning|error")

    api_key = source.get("ANTHROPIC_API_KEY", "").strip() or None
    return AppConfig(app_env=app_env, log_level=log_level, anthropic_api_key=api_key)
