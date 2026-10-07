#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Delivery Engine task-breakdown output against the required sections and task fields.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stdout when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys


def validate(text: str) -> list[str]:
    errors: list[str] = []

    # Required top-level sections
    for section in (
        "^tasks:",
        "^dependencies:",
        "^risks:",
        "^critical_path:",
        "^unknowns:",
        "^validation:",
    ):
        if re.search(section, text, re.MULTILINE) is None:
            errors.append(f"missing section: {section.removeprefix('^')}")

    # Every task must have a done_when condition
    task_count = len(re.findall(r"^- id: T-[0-9]+", text, re.MULTILINE))
    done_when_count = len(re.findall(r"^[ \t]+done_when:", text, re.MULTILINE))
    if task_count > 0 and done_when_count < task_count:
        errors.append(
            f"every task must have a done_when condition ({done_when_count} found for {task_count} tasks)"
        )

    # Every task must have an estimate or be a spike with a timebox
    estimate_count = len(re.findall(r"^[ \t]+estimate: [SML]", text, re.MULTILINE))
    timebox_count = len(re.findall(r"^[ \t]+timebox:", text, re.MULTILINE))
    if task_count > 0 and estimate_count + timebox_count < task_count:
        errors.append("every task must have an estimate (S/M/L) or a timebox for spikes")

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
