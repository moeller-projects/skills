#!/usr/bin/env python3
"""Validate the debugging output contract from stdin using only the standard library."""

import json
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
    match = re.search(
        rf"^{re.escape(heading)}[ \t]*\r?\n(?P<body>.*?)(?=^[a-z_]+:|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group("body") if match else ""


def _field(body: str, name: str) -> str:
    match = re.search(rf"^[ \t-]*{re.escape(name)}:[ \t]*(\S.*)$", body, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _meaningful_list(body: str) -> bool:
    entries = [line.strip()[2:].strip() for line in body.splitlines() if line.strip().startswith("- ")]
    return bool(entries) and all(entry or entry.lower() in {"none", "not run", "not applied"} for entry in entries)


def validate_text(text: str) -> list[str]:
    errors: list[str] = []
    for heading in REQUIRED:
        if re.search(rf"^{re.escape(heading)}", text, re.MULTILINE) is None:
            errors.append(f"missing section: {heading}")

    status = re.search(r"^status:[ \t]*([^\r\n]+)", text, re.MULTILINE)
    status_value = status.group(1).strip() if status else ""
    if status_value not in STATUSES:
        errors.append("status must be one of: reproduced, hypothesized, confirmed, fixed")

    for heading in ("root_cause:", "repro_steps:", "fix:", "verification:", "regression_check:", "open_risks:"):
        body = _section(text, heading)
        if not body.strip():
            errors.append(f"section must be non-empty: {heading}")
        elif heading != "root_cause:" and not _meaningful_list(body):
            errors.append(f"section must contain meaningful list entries: {heading}")

    root = _section(text, "root_cause:")
    if root:
        for field in ("finding", "evidence"):
            if not _field(root, field):
                errors.append(f"root_cause must include non-empty {field}")
    if status_value in {"confirmed", "fixed"} and not _field(root, "evidence"):
        errors.append(f"{status_value} requires evidence establishing the causal claim")
    return errors


def main() -> None:
    if "--help" in sys.argv:
        print("Usage: validate-output.py < diagnosis.txt")
        print("Validate the debugging output contract; diagnostics go to stderr.")
        return
    errors = validate_text(sys.stdin.read())
    result = {"valid": not errors, "errors": errors}
    print(json.dumps(result, sort_keys=True))
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
