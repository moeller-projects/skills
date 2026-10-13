#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Discovery output against the problem, assumptions, options, recommendation, and next contract.
Inputs: Contract text on stdin.
Outputs: JSON validation result on stdout; diagnostics on stderr when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]

HELP = """Usage: python scripts/validate-output.py < output.txt

Validate Discovery output from stdin. Results are JSON on stdout; diagnostics
are written to stderr.
"""



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
    options_body = ""
    if options_match is not None:
        options_body = options_match.group("body")
        option_lines = re.findall(r"^[0-9]+\.\s*(.*)$", options_body, re.MULTILINE)
        option_count = len(option_lines)
        if any(not line.strip() for line in option_lines):
            errors.append("options must not contain empty numbered options")

    if option_count < 2:
        ruled_out = re.search(
            r"(?ims)^[ \t]*(?:ruled[- ]out alternatives?|alternatives ruled out)\s*:\s*\n(?P<body>.*?)(?=^[a-z][a-zA-Z_-]*:|\Z)",
            input_text,
        )
        alternatives = []
        if ruled_out:
            alternatives = re.findall(r"^[ \t]*-\s*([^:\n—]+?)\s*(?::|—)\s*(\S.*)$", ruled_out.group("body"), re.MULTILINE)
        if option_count != 1 or not alternatives:
            errors.append("options must include at least two numbered options unless ruled-out alternatives are documented with a non-empty reason")
    if option_count == 0:
        errors.append("options must include at least one substantive numbered option")
    return errors


def main() -> None:
    if "--help" in sys.argv[1:]:
        print(HELP, end="")
        return

    errors = validate_text(sys.stdin.read())
    result = {"valid": not errors, "errors": errors}
    print(json.dumps(result))
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
