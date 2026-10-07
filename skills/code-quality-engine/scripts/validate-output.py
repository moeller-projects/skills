#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Code Quality Engine output against the findings/patch-plan/risk contract.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stdout when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys


def validate_output(input_text: str) -> list[str]:
    errors: list[str] = []

    if not re.search(r"^findings:", input_text, re.MULTILINE):
        errors.append("missing 'findings:' section")
    if not re.search(r"^patch-plan:", input_text, re.MULTILINE):
        errors.append("missing 'patch-plan:' section")
    if not re.search(r"^risk:", input_text, re.MULTILINE):
        errors.append("missing 'risk:' section")

    labels = re.findall(r"\[(critical|high|medium|low|CRITICAL|HIGH|MEDIUM|LOW)\]", input_text)
    invalid = [label for label in labels if label not in {"critical", "high", "medium", "low"}]
    if invalid:
        invalid_labels = "\n".join(f"[{label}]" for label in invalid)
        errors.append(f"invalid severity label: {invalid_labels} (must be lowercase)")
    severities = re.findall(r"^- \[(critical|high|medium|low)\].*", input_text, re.MULTILINE)
    if len(severities) > 1:
        ranks = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        last_rank = 4
        for severity in severities:
            rank = ranks[severity]
            if rank > last_rank:
                errors.append("findings are not sorted by severity: critical → high → medium → low")
                break
            last_rank = rank

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
