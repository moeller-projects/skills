#!/usr/bin/env python3
"""Validate the debugging output contract from stdin using only the standard library."""

import re
import sys

STATUSES = {"reproduced", "hypothesized", "confirmed", "fixed"}
REQUIRED = (
    "status:",
    "root_cause:",
    "repro_steps:",
    "fix:",
    "verification:",
    "regression_check:",
    "open_risks:",
)


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}[ \t]*\r?\n(?P<body>.*?)(?=^[a-z_]+:|\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group("body") if match else ""


def validate_text(text: str) -> list[str]:
    errors: list[str] = []
    for heading in REQUIRED:
        if re.search(rf"^{re.escape(heading)}", text, re.MULTILINE) is None:
            errors.append(f"missing section: {heading}")

    status = re.search(r"^status:[ \t]*([^\r\n]+)", text, re.MULTILINE)
    if status is None or status.group(1).strip() not in STATUSES:
        errors.append("status must be one of: reproduced, hypothesized, confirmed, fixed")

    for heading in ("root_cause:", "repro_steps:", "fix:", "verification:", "regression_check:", "open_risks:"):
        if not _section(text, heading).strip():
            errors.append(f"section must be non-empty: {heading}")

    if re.search(r"^root_cause:\s*$", text, re.MULTILINE):
        if not re.search(r"^[ \t-]*evidence:[ \t]*\S", _section(text, "root_cause:"), re.MULTILINE):
            errors.append("root_cause must include non-empty evidence")
    return errors


def main() -> None:
    if "--help" in sys.argv:
        print("Usage: validate-output.py < diagnosis.txt")
        return
    errors = validate_text(sys.stdin.read())
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)
    print("OK")


if __name__ == "__main__":
    main()
