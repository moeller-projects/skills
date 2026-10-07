#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Scrutineer output against the verdict/summary/findings/out-of-scope/risk contract.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stdout when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys

VALID_VERDICTS = {"approve", "request-changes", "comment"}
RANKS = {"blocker": 4, "major": 3, "minor": 2, "nit": 1}


def validate_output(input_text: str) -> list[str]:
    errors: list[str] = []

    verdicts = re.findall(r"^verdict:\s*(\S+)", input_text, re.MULTILINE)
    if len(verdicts) != 1:
        errors.append("expected exactly one 'verdict:' line")
    elif verdicts[0] not in VALID_VERDICTS:
        errors.append(f"invalid verdict: {verdicts[0]} (must be approve, request-changes, or comment)")

    for section in ("summary", "findings", "out-of-scope", "risk"):
        if not re.search(rf"^{section}:", input_text, re.MULTILINE):
            errors.append(f"missing '{section}:' section")

    labels = re.findall(r"\[(blocker|major|minor|nit|BLOCKER|MAJOR|MINOR|NIT)\]", input_text)
    invalid = [label for label in labels if label not in RANKS]
    if invalid:
        invalid_labels = "\n".join(f"[{label}]" for label in invalid)
        errors.append(f"invalid severity label: {invalid_labels} (must be lowercase)")

    severities = re.findall(r"^- \[(blocker|major|minor|nit)\].*", input_text, re.MULTILINE)
    if len(severities) > 1:
        last_rank = 4
        for severity in severities:
            rank = RANKS[severity]
            if rank > last_rank:
                errors.append("findings are not sorted by severity: blocker → major → minor → nit")
                break
            last_rank = rank

    if verdicts and verdicts[0] == "approve":
        if any(sev in {"blocker", "major"} for sev in severities):
            errors.append("verdict is approve but blocker or major findings exist")

    if verdicts and verdicts[0] == "request-changes":
        if severities and not any(sev in {"blocker", "major"} for sev in severities):
            errors.append("verdict is request-changes but no blocker or major finding exists")

    return errors


def main() -> None:
    errors = validate_output(sys.stdin.read())
    if errors:
        sys.stdout.reconfigure(encoding="utf-8")
        print("INVALID output:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
