#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Doc Engine outputs for doc-plan, diff-oriented, and decision-record contracts.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stdout when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def validate(text: str) -> list[str]:
    errors: list[str] = []

    if re.search(r"^decision:", text, re.MULTILINE):
        for field in (r"^  context:", r"^  decision:", r"^  reasoning:", r"^  tradeoffs:", r"^  reuse_scope:"):
            if not re.search(field, text, re.MULTILINE):
                errors.append(f"missing decision field: {field[3:]}")
    else:
        for section in (r"^doc:", r"^changes:", r"^gaps:"):
            if not re.search(section, text, re.MULTILINE):
                errors.append(f"missing section: {section[1:]}")

        if not re.search(r"^- purpose:", text, re.MULTILINE):
            errors.append("missing doc purpose")
        if not re.search(r"^- audience:", text, re.MULTILINE):
            errors.append("missing doc audience")
        if not re.search(r"^- structure:", text, re.MULTILINE):
            errors.append("missing doc structure")

        if re.search(r"^- format:", text, re.MULTILINE):
            if not re.search(r"type: (markdown|html)", text, re.MULTILINE):
                errors.append("missing format type: markdown|html")
            if not re.search(r"^[ \t]*- artifact:", text, re.MULTILINE):
                errors.append("missing artifact field")
            if re.search(r"type: html", text, re.MULTILINE):
                if re.search(r"<html>|<head>|<style>|<body>", text, re.MULTILINE):
                    for token in ("<html>", "<head>", "<style>", "<body>", "print"):
                        if token not in text:
                            errors.append(f"missing html validation token: {token}")
                    if re.search(r"<link[^>]+stylesheet|<script[^>]+src=", text, re.MULTILINE):
                        errors.append("html output must avoid external stylesheet/script dependencies")

        structure_lines = re.findall(r"^[ \t]+[0-9]+\..*$", text, re.MULTILINE)
        for line in structure_lines:
            if not re.search(r"\[(tutorial|how-to|reference|explanation)\]", line):
                errors.append(f"structure entry missing valid mode tag [tutorial|how-to|reference|explanation]: {line}")

        if re.search(r"^--- ", text, re.MULTILINE) and not re.search(r"^reason:", text, re.MULTILINE):
            errors.append("diff output must include reason:")

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
