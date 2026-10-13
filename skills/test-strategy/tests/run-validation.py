#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate required Test Strategy files and output contract behavior.
Inputs: Repository working tree containing the Test Strategy skill directory.
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
    passed("test-strategy required files exist")

    valid_output = """test-plan:
1. Add unit tests for valid and invalid discount codes.

coverage-gaps:
- Browser checkout E2E is blocked until staging credentials are available.

cases:
- case: valid discount reduces order total
  given: a valid discount code and a $100 order
  when: checkout calculates the total
  then: total is reduced and returned to the caller
  level: unit
  priority: high
- case: expired discount is rejected
  given: an expired discount code
  when: checkout validates the code
  then: a validation error is returned
  level: integration
  priority: critical

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
- test case translated from acceptance criteria: valid discount code reduces the order total.

"""
    errors = validate(invalid_output)
    if not errors:
        fail("invalid test output unexpectedly passed")
    if not any("missing section: risk:" in error for error in errors):
        fail("missing required section was not reported")
    passed("validator rejects output with a missing required section")
    missing_case_fields = valid_output.replace("  level: unit\n", "").replace("  priority: high\n", "")
    errors = validate(missing_case_fields)
    if not any("substantive level" in error for error in errors) or not any("substantive priority" in error for error in errors):
        fail("case level and priority omissions were not reported")
    passed("each case requires level and priority")
    print("\nTest Strategy validation completed successfully.")


if __name__ == "__main__":
    main()
