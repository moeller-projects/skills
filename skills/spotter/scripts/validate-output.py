#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Spotter output against the problem, assumptions, options, recommendation, and next contract.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stderr when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def validate_text(input_text: str) -> list[str]:
    errors: list[str] = []
    for section in ("problem:", "assumptions:", "options:", "recommendation:", "next:"):
        if re.search(rf"^{re.escape(section)}", input_text, re.MULTILINE) is None:
            errors.append(f"missing section: {section}")

    options_match = re.search(
        r"^options:[ \t]*\r?\n(?P<body>.*?)(?=^[a-z][a-zA-Z_-]*:|\Z)",
        input_text,
        re.MULTILINE | re.DOTALL,
    )
    option_count = 0
    if options_match is not None:
        option_count = len(re.findall(r"^[0-9]+\.", options_match.group("body"), re.MULTILINE))
    if option_count < 1:
        errors.append("options must include at least one numbered option")
    return errors


def main() -> None:
    errors = validate_text(sys.stdin.read())
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
