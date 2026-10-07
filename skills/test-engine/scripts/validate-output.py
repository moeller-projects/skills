#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Test Engine output against the test-plan, coverage-gaps, cases, and risk contract.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stdout when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys


def validate(input_text: str) -> list[str]:
    errors: list[str] = []
    for section in ("^test-plan:", "^coverage-gaps:", "^cases:", "^risk:"):
        if re.search(section, input_text, re.MULTILINE) is None:
            errors.append(f"missing section: {section.removeprefix('^')}")

    if re.search(r"given .+ when .+ then .+", input_text, re.IGNORECASE) is None:
        given_count = len(re.findall(r"^[ \t]+given:", input_text, re.MULTILINE))
        when_count = len(re.findall(r"^[ \t]+when:", input_text, re.MULTILINE))
        then_count = len(re.findall(r"^[ \t]+then:", input_text, re.MULTILINE))
        if given_count < 1 or when_count < 1 or then_count < 1:
            errors.append("test cases must use GIVEN/WHEN/THEN")
    return errors


def main() -> None:
    errors = validate(sys.stdin.read())
    if errors:
        print("INVALID output:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
