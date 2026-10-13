#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Code Review output against the findings/patch-plan/risk contract.
Inputs: Contract text on stdin. Use --help for the stdin contract and exit behavior.
Outputs: "OK" on stdout when valid; diagnostics on stderr and exit status 1 when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"^{re.escape(heading)}[ \t]*\r?\n(?P<body>.*?)(?=^[a-z][a-z-]*:|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group("body") if match else ""


def _nonempty_lines(body: str) -> list[str]:
    return [line.strip() for line in body.splitlines() if line.strip()]


def validate_output(input_text: str) -> list[str]:
    errors: list[str] = []
    findings = _section(input_text, "findings:")
    patch_plan = _section(input_text, "patch-plan:")
    risk = _section(input_text, "risk:")

    for heading, body in (("findings:", findings), ("patch-plan:", patch_plan), ("risk:", risk)):
        if not body.strip():
            errors.append(f"section must be non-empty: {heading}")
    if not findings.strip():
        return errors

    finding_lines = [line for line in findings.splitlines() if line.strip()]
    none_findings = len(finding_lines) == 1 and finding_lines[0].strip().lower() in {
        "- none", "none", "- [none]"
    }
    if none_findings:
        patch_items = _nonempty_lines(patch_plan)
        if not any(re.match(r"^\s*\d+[.)]\s+\S+", line) for line in patch_items):
            if not any(re.match(r"^-\s+(?:none|no patch(?:es)?(?: needed)?|not applicable)\b", line, re.I) for line in patch_items):
                errors.append("patch-plan must contain ordered steps or an explicit no-action marker")
        if not any(re.match(r"^\s*-\s+\S+", line) for line in _nonempty_lines(risk)):
            errors.append("risk must contain an explicit residual-risk or none item")
        return errors

    severities = []
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    malformed_entry = False
    for raw in finding_lines:
        line = raw.strip()
        if line.startswith("- ["):
            match = re.match(r"^- \[(critical|high|medium|low)\] ([^:]+:\d+) — (.+)$", line)
            if not match:
                malformed_entry = True
                continue
            if current:
                entries.append(current)
            current = {
                "severity": match.group(1),
                "location": match.group(2),
                "issue": match.group(3).strip(),
                "why": "",
                "fix": "",
            }
            severities.append(match.group(1))
            continue
        if current and line.startswith("why:"):
            current["why"] = line[4:].strip()
        elif current and line.startswith("fix:"):
            current["fix"] = line[4:].strip()
        elif current:
            malformed_entry = True
    if current:
        entries.append(current)
    if malformed_entry:
        errors.append("each finding entry must use a valid header and only why:/fix: detail fields")
    if not entries:
        errors.append("each finding must include severity, file:line location, and issue")
        return errors

    for entry in entries:
        location = entry["location"]
        if not entry["issue"]:
            errors.append(f"finding at {location} has an empty issue")
        if not entry["why"]:
            errors.append(f"finding at {location} must include a meaningful why")
        if not entry["fix"]:
            errors.append(f"finding at {location} must include a meaningful fix")

    ranks = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    if any(ranks[value] > ranks[severities[index - 1]] for index, value in enumerate(severities) if index):
        errors.append("findings are not sorted by severity: critical → high → medium → low")
    if not any(re.match(r"^\s*[-\d].+", line) for line in _nonempty_lines(patch_plan)):
        errors.append("patch-plan must contain meaningful ordered steps")
    return errors


def main() -> None:
    if "--help" in sys.argv[1:]:
        print("Usage: python scripts/validate-output.py < contract.txt")
        print("Reads the contract from stdin; prints OK to stdout on success.")
        print("On invalid input, diagnostics go to stderr and the process exits 1.")
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
