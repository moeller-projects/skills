#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Incident Response output against the status/severity/impact/timeline/mitigation/root-cause/follow-ups/comms contract.
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

    sections: dict[str, str] = {}
    section_matches = list(re.finditer(r"^(impact|timeline|mitigation|root-cause|follow-ups|comms):[ \t]*$", input_text, re.MULTILINE))
    for index, match in enumerate(section_matches):
        end = section_matches[index + 1].start() if index + 1 < len(section_matches) else len(input_text)
        sections[match.group(1)] = input_text[match.end():end]
    for section in ("impact", "timeline", "mitigation", "root-cause", "follow-ups", "comms"):
        if section not in sections:
            errors.append(f"missing '{section}:' section")
        elif not sections[section].strip():
            errors.append(f"empty '{section}:' section")

    timeline_body = sections.get("timeline", "")
    for line in timeline_body.splitlines():
        if line.strip() and line.lstrip().startswith("- ") and not re.match(r"^\s*- \d{2}:\d{2}Z\b", line):
            errors.append(f"timeline entry missing UTC timestamp: {line.strip()}")

    followups_body = sections.get("follow-ups", "")
    for line in followups_body.splitlines():
        if line.strip() and line.lstrip().startswith("- ") and "owner:" not in line:
            errors.append(f"follow-up missing owner: {line.strip()}")

    if statuses and statuses[0] == "resolved":
        root_body = sections.get("root-cause", "")
        if not root_body.strip():
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
