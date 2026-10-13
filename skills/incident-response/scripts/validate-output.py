#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Incident Response output against the status/severity/impact/timeline/mitigation/root-cause/follow-ups/comms contract.
Inputs: Contract text on stdin. Use --help for the stdin contract and exit behavior.
Outputs: "OK" on stdout when valid; diagnostics on stderr and exit status 1 when invalid.
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

    root_body = sections.get("root-cause", "")
    if statuses and statuses[0] == "resolved" and not root_body.strip():
        errors.append("resolved incident must state a root cause or explicitly say unknown")
    if statuses and statuses[0] == "resolved" and re.search(r"\bunknown\b", root_body, re.IGNORECASE):
        errors.append("unknown root cause cannot be marked resolved; use monitoring")
    if statuses and statuses[0] == "monitoring" and re.search(r"\bunknown\b", root_body, re.IGNORECASE):
        if not re.search(r"(?i)\bmonitor(?:ing)?\b.*\b(?:until|baseline|threshold|alert|symptom)\b|\b(?:until|baseline|threshold|alert|symptom)\b.*\bmonitor(?:ing)?\b", input_text):
            errors.append("monitoring status must state the monitoring rule")
        if not re.search(r"\binvestigat\w*.*\b(owner|team|on-call)\b|\b(owner|team|on-call)\b.*\binvestigat\w*", followups_body, re.IGNORECASE):
            errors.append("unknown root cause requires an owned investigation follow-up")
    return errors


def main() -> None:
    if "--help" in sys.argv[1:]:
        print("Usage: python scripts/validate-output.py < incident-artifact.txt")
        print("Reads the status, severity, impact, timeline, mitigation, root-cause, follow-ups, and comms sections from stdin.")
        print("On valid input prints OK and exits 0; invalid-input diagnostics go to stderr and exit 1.")
        return

    errors = validate_output(sys.stdin.read())
    if errors:
        sys.stderr.reconfigure(encoding="utf-8")
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
