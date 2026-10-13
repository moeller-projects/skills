#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate the Operations output validator.
Inputs: Repository working tree containing the Operations skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

import subprocess
import json
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
- Reapply the previous ingress manifest in cluster prod-eu/context-a from release artifact ingress-prev.yaml; verify recovery with kubectl rollout status -n production

security:
- human approval required before production rollout
"""
    result = run_validator(valid_output)
    validation = json.loads(result.stdout)
    if result.returncode != 0 or not validation["valid"] or validation["errors"] or result.stderr:
        fail(f"valid ops output unexpectedly failed: {result.stdout}{result.stderr}")
    passed("valid ops output passes")

    invalid_output = """risk:
- medium likelihood / high impact — rollout can break ingress routing

plan:
1. Deploy to production immediately.

checks:
- kubectl apply --dry-run=server -f k8s/ingress.yaml

rollback:
- Reapply the previous ingress manifest in namespace production/context-a from release artifact ingress-prev.yaml; verify recovery with rollout status

security:
- verify TLS secret exists
"""
    result = run_validator(invalid_output)
    validation = json.loads(result.stdout)
    if result.returncode == 0 or validation["valid"] or not validation["errors"] or result.stderr:
        fail("production step without its own approval was accepted")
    passed("validator rejects production steps without approval")
    destructive_without_gate = valid_output.replace(
        "1. Apply the ingress manifest in staging.",
        "1. Delete the staging deployment without human approval."
    )
    result = run_validator(destructive_without_gate)
    if result.returncode == 0 or json.loads(result.stdout)["valid"]:
        fail("destructive step without its own approval was accepted")
    passed("destructive approval is checked per step")
    missing_rollback = valid_output.replace(
        "1. Apply the ingress manifest in staging.",
        "1. Delete the staging deployment — human approval required."
    ).replace(
        "- Reapply the previous ingress manifest in cluster prod-eu/context-a from release artifact ingress-prev.yaml; verify recovery with kubectl rollout status -n production",
        "- none"
    )
    result = run_validator(missing_rollback)
    if result.returncode == 0 or json.loads(result.stdout)["valid"]:
        fail("approved destructive step without rollback safeguards was accepted")
    passed("approved destructive steps require rollback safeguards")


if __name__ == "__main__":
    main()
