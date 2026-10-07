#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Safety Car output against the status/severity/impact/timeline/mitigation/root-cause/follow-ups/comms contract.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stdout when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys

VALID_STATUSES = {"investigating", "mitigated", "monitoring", "resolved"}
VALID_SEVERITIES = {"SEV1", "SEV2", "SEV3"}


def validate_output(input_text: str) -> list[str]:
    errors: list[str] = []

    statuses = re.findall(r"^status:\s*(\S+)", input_text, re.MULTILINE)
    if len(statuses) != 1:
        errors.append("expected exactly one 'status:' line")
    elif statuses[0] not in VALID_STATUSES:
        errors.append(f"invalid status: {statuses[0]} (must be investigating, mitigated, monitoring, or resolved)")

    severities = re.findall(r"^severity:\s*(\S+)", input_text, re.MULTILINE)
    if len(severities) != 1:
        errors.append("expected exactly one 'severity:' line")
    elif severities[0] not in VALID_SEVERITIES:
        errors.append(f"invalid severity: {severities[0]} (must be SEV1, SEV2, or SEV3)")

    for section in ("impact", "timeline", "mitigation", "root-cause", "follow-ups", "comms"):
        if not re.search(rf"^{section}:", input_text, re.MULTILINE):
            errors.append(f"missing '{section}:' section")

    timeline_block = re.search(r"^timeline:\n((?:- .*\n?)*)", input_text, re.MULTILINE)
    if timeline_block and timeline_block.group(1).strip():
        for line in timeline_block.group(1).strip().splitlines():
            if not re.match(r"^- \d{2}:\d{2}Z\b", line):
                errors.append(f"timeline entry missing UTC timestamp: {line.strip()}")
                break

    followups_block = re.search(r"^follow-ups:\n((?:- .*\n?)*)", input_text, re.MULTILINE)
    if followups_block and followups_block.group(1).strip():
        for line in followups_block.group(1).strip().splitlines():
            if "owner:" not in line:
                errors.append(f"follow-up missing owner: {line.strip()}")
                break

    if statuses and statuses[0] == "resolved":
        root_block = re.search(r"^root-cause:\n((?:- .*\n?)*)", input_text, re.MULTILINE)
        if not root_block or not root_block.group(1).strip():
            errors.append("resolved incident must state a root cause or explicitly say unknown")

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
