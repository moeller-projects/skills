#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate required Test Engine files and output contract behavior.
Inputs: Repository working tree containing the Test Engine skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

import importlib.util
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
_validator_spec = importlib.util.spec_from_file_location(
    "validate_output", SKILL_DIR / "scripts" / "validate-output.py"
)
if _validator_spec is None or _validator_spec.loader is None:
    raise ImportError("unable to load validate-output.py")
_validator_module = importlib.util.module_from_spec(_validator_spec)
_validator_spec.loader.exec_module(_validator_module)
validate = _validator_module.validate


def passed(message: str) -> None:
    print(f"PASS: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    validator = SKILL_DIR / "scripts" / "validate-output.py"
    for required in [
        validator,
        SKILL_DIR / "assets" / "templates" / "output.md",
        SKILL_DIR / "tests" / "validation-checklist.md",
    ]:
        if not required.is_file():
            fail(f"missing {required.name}")
    passed("test-engine required files exist")

    valid_output = """test-plan:
1. Add unit tests for valid and invalid discount codes.

coverage-gaps:
- Browser checkout E2E is blocked until staging credentials are available.

cases:
- GIVEN a valid discount code WHEN checkout is submitted THEN the order total is reduced.
- GIVEN an expired discount code WHEN checkout is submitted THEN the API returns a validation error.

risk:
- Staging-only tax logic still needs manual verification
"""
    if validate(valid_output):
        fail("valid test output unexpectedly failed")
    passed("valid test output passes")

    invalid_output = """test-plan:
1. Add unit tests for valid and invalid discount codes.

coverage-gaps:
- Browser checkout E2E is blocked until staging credentials are available.

cases:
- GIVEN a valid discount code WHEN checkout is submitted.

risk:
- Staging-only tax logic still needs manual verification
"""
    errors = validate(invalid_output)
    if not errors:
        fail("invalid test output unexpectedly passed")
    if not any("GIVEN/WHEN/THEN" in error for error in errors):
        fail("case format failure not reported")
    passed("validator rejects incomplete test cases")

    print("\nTest Engine validation completed successfully.")


if __name__ == "__main__":
    main()
