#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Test Strategy output against the test-plan, coverage-gaps, cases, and risk contract.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stderr when invalid.
Side effects: None.
Usage: python scripts/validate-output.py [--help]

Requires Python 3.9+, standard library only.
"""

import re
import sys


def validate(input_text: str) -> list[str]:
    errors: list[str] = []
    sections = {}
    matches = list(re.finditer(r"^(test-plan|coverage-gaps|cases|risk):[ \t]*$", input_text, re.MULTILINE))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(input_text)
        sections[match.group(1)] = input_text[match.end():end]
    for section in ("test-plan", "coverage-gaps", "cases", "risk"):
        body = sections.get(section, "")
        if section not in sections:
            errors.append(f"missing section: {section}:")
        elif not body.strip() or re.fullmatch(r"\s*-\s*(none|n/?a|<[^>]+>)\s*", body, re.IGNORECASE):
            errors.append(f"section {section}: must contain substantive content")
    cases = sections.get("cases", "")
    starts = list(re.finditer(r"(?im)^\s*-\s*case:\s*(\S.*)$", cases))
    if not starts:
        errors.append("cases: must contain at least one substantive case")
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(cases)
        block = cases[start.start():end]
        for field in ("given", "when", "then", "level", "priority"):
            if not re.search(rf"(?im)^\s*{field}:\s*\S", block):
                errors.append(f"each case must include substantive {field}")
        level = re.search(r"(?im)^\s*level:\s*(\S+)", block)
        priority = re.search(r"(?im)^\s*priority:\s*(\S+)", block)
        if level and level.group(1).lower() not in {"unit", "integration", "e2e"}:
            errors.append("case level must be unit, integration, or e2e")
        if priority and priority.group(1).lower() not in {"critical", "high", "medium", "low"}:
            errors.append("case priority must be critical, high, medium, or low")

    return errors
def main() -> None:
    if "--help" in sys.argv[1:]:
        print("Usage: python scripts/validate-output.py [--help]")
        print("Validate test-strategy output from stdin.")
        return

    errors = validate(sys.stdin.read())
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
