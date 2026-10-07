#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate the Ops Engine output validator.
Inputs: Repository working tree containing the Ops Engine skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def passed(message: str) -> None:
    print(f"PASS: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    validator = SKILL_DIR / "scripts" / "validate-output.py"
    if not validator.is_file():
        fail("missing validate-output.py")
    passed("validator exists")

    def run_validator(text: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(validator)],
            input=text,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    valid_output = """risk:
- medium likelihood / high impact — rollout can break ingress routing

plan:
1. Apply the ingress manifest in staging.

checks:
- kubectl apply --dry-run=server -f k8s/ingress.yaml

rollback:
- Reapply the previous ingress manifest from release artifact ingress-prev.yaml

security:
- human approval required before production rollout
"""
    result = run_validator(valid_output)
    if result.returncode != 0 or result.stdout.strip() != "OK":
        fail(f"valid ops output unexpectedly failed: {result.stdout}{result.stderr}")
    passed("valid ops output passes")

    invalid_output = """risk:
- medium likelihood / high impact — rollout can break ingress routing

plan:
1. Deploy to production immediately.

checks:
- kubectl apply --dry-run=server -f k8s/ingress.yaml

rollback:
- Reapply the previous ingress manifest from release artifact ingress-prev.yaml

security:
- verify TLS secret exists
"""
    result = run_validator(invalid_output)
    if result.returncode == 0:
        fail("production plan without approval unexpectedly passed")
    if "human approval gate" not in result.stderr.lower():
        fail("production approval failure not reported")
    passed("validator rejects production steps without approval")

    print("\nOps Engine validation completed successfully.")


if __name__ == "__main__":
    main()
