#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "main.jac",
    ROOT / "mock_vllm.py",
    ROOT / "requirements.txt",
    ROOT / "README.md",
]


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("Missing bootstrap artifacts:")
        for item in missing:
            print(f"- {item}")
        return 1

    readme = (ROOT / "README.md").read_text()
    required_commands = [
        "export ANTHROPIC_API_KEY",
        "python3 mock_vllm.py",
        "jac start main.jac",
    ]
    missing_commands = [cmd for cmd in required_commands if cmd not in readme]
    if missing_commands:
        print("README is missing required setup commands:")
        for item in missing_commands:
            print(f"- {item}")
        return 2

    print("Bootstrap artifacts verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
