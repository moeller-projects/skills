#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate PR Review output against the verdict/summary/findings/out-of-scope/risk contract.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stderr when invalid.
Usage: python scripts/validate-output.py < review.txt
       python scripts/validate-output.py --help
Side effects: None.

Requires Python 3.9+, standard library only.

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

    sections = {}
    section_matches = list(re.finditer(r"^([a-z][a-zA-Z_-]*):[ \t\r]*$", input_text, re.MULTILINE))
    for index, match in enumerate(section_matches):
        end = section_matches[index + 1].start() if index + 1 < len(section_matches) else len(input_text)
        sections[match.group(1)] = input_text[match.end():end]
    summary_match = re.search(r"^summary:[ \t]*(\S[^\r\n]*)$", input_text, re.MULTILINE)
    if not summary_match:
        errors.append("missing 'summary:' section")
    for section in ("findings", "out-of-scope", "risk"):
        if section not in sections:
            errors.append(f"missing '{section}:' section")
        elif not sections[section].strip():
            errors.append(f"empty '{section}:' section")
    findings_body = sections.get("findings", "")
    if re.fullmatch(r"\s*-\s*none\s*", findings_body, re.IGNORECASE):
        finding_starts = []
    else:
        finding_starts = list(re.finditer(r"^- \[([^\]]+)\](?P<text>.*)$", findings_body, re.MULTILINE))
        if not finding_starts:
            errors.append("findings must contain '- none' or structured severity findings")
        for match in finding_starts:
            if match.group(1) not in RANKS:
                errors.append(f"invalid severity label: [{match.group(1)}] (must be blocker, major, minor, or nit)")
    severities = [match.group(1) for match in finding_starts if match.group(1) in RANKS]
    for index, finding in enumerate(finding_starts):
        end = finding_starts[index + 1].start() if index + 1 < len(finding_starts) else len(findings_body)
        block = findings_body[finding.start():end]
        if not re.search(r"\b[^ \n:]+:\d+\s*(?:—|-)\s*\S", finding.group("text")):
            errors.append("each finding must include a nonempty issue after its file path and line")
        if not re.search(r"(?im)^\s*why:\s*\S", block):
            errors.append("each finding must include why")
        if not re.search(r"(?im)^\s*suggestion:\s*\S", block):
            errors.append("each finding must include suggestion")

    if len(severities) > 1:
        last_rank = 4
        for severity in severities:
            rank = RANKS[severity]
            if rank > last_rank:
                errors.append("findings are not sorted by severity: blocker → major → minor → nit")
                break
            last_rank = rank

    summary_match = re.search(r"^summary:[ \t]*(\S[^\r\n]*)$", input_text, re.MULTILINE)
    summary = summary_match.group(1).strip() if summary_match else ""
    risk = sections.get("risk", "").strip()
    if not summary or summary.startswith("<"):
        errors.append("summary must be substantive")
    if not risk or risk.startswith("<"):
        errors.append("risk must state residual risk or explicitly say none")
    if any(sev in {"blocker", "major"} for sev in severities):
        if verdicts and verdicts[0] in {"approve", "comment"}:
            errors.append("blocker or major findings require request-changes verdict")
    if verdicts and verdicts[0] == "request-changes":
        if not severities or not any(sev in {"blocker", "major"} for sev in severities):
            errors.append("verdict is request-changes but no blocker or major finding exists")

    return errors


def main() -> None:
    if "--help" in sys.argv[1:]:
        print("Usage: validate-output.py [--help] < review.txt")
        print("Validate PR Review output from stdin.")
        return

    errors = validate_output(sys.stdin.read())
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
