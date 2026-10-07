#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Ops Engine output against the risk/plan/checks/rollback/security contract.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stderr when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys


def validate(input_text: str) -> list[str]:
    errors = []

    # Check required sections
    for section in ("^risk:", "^plan:", "^checks:", "^rollback:", "^security:"):
        if re.search(section, input_text, re.MULTILINE) is None:
            errors.append(f"missing section: {section[1:]}")

    # Check that ABORT is present if plan status is BLOCKED
    if re.search(r"^plan:.*BLOCKED", input_text, re.MULTILINE | re.IGNORECASE):
        if re.search(r"ABORT", input_text, re.IGNORECASE) is None:
            errors.append("plan is BLOCKED but no ABORT statement found")

    # Check that human approval is mentioned when production is referenced
    if re.search(r"production", input_text, re.IGNORECASE) is not None:
        if re.search(r"human approval|approval required", input_text, re.IGNORECASE) is None:
            errors.append("production step found but no human approval gate")

    return errors


def main() -> None:
    input_text = sys.stdin.buffer.read().decode("utf-8")
    errors = validate(input_text)
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    print("OK")


if __name__ == "__main__":
    main()
