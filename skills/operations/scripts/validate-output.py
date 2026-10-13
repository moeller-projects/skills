#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Operations output against the risk/plan/checks/rollback/security contract.
Inputs: Contract text on stdin. Use --help for the stdin contract and exit status.
Outputs: A JSON validation result on stdout; diagnostics are included in the JSON result and no incidental text is written.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import json
import re
import sys


def validate(input_text: str) -> list[str]:
    input_text = input_text.replace("\r\n", "\n").replace("\r", "\n")
    errors = []

    sections = {}
    matches = list(re.finditer(r"^(risk|plan|checks|rollback|security):[ \t]*$", input_text, re.MULTILINE))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(input_text)
        sections[match.group(1)] = input_text[match.end():end]
    for section in ("risk", "plan", "checks", "rollback", "security"):
        if section not in sections:
            errors.append(f"missing section: {section}:")
        elif not sections[section].strip():
            errors.append(f"empty section: {section}:")

    plan = sections.get("plan", "")
    blocked = bool(re.search(r"\bBLOCKED\b", plan, re.IGNORECASE))
    if blocked and not re.search(r"(?im)^\s*(?:ABORT|status:\s*blocked\b)", plan):
        errors.append("plan is BLOCKED but has no explicit abort/status representation")

    # Approval is attached to each destructive numbered step, not inferred from
    # an unrelated production mention elsewhere in the artifact.
    steps = list(re.finditer(r"(?m)^\s*(\d+)[.)]\s+(.*?)(?=^\s*\d+[.)]\s+|\Z)", plan, re.DOTALL))
    if not steps and not blocked:
        errors.append("plan must contain numbered executable steps or an explicit BLOCKED abort")
    if not blocked and re.search(r"(?m)^[-*][ \t]+\S", plan):
        errors.append("plan items must be numbered steps with local approval")
    destructive = re.compile(r"\b(delete|destroy|overwrite|drain|scale\s+to\s+zero|drop|truncate|migrate|rollback)\b", re.IGNORECASE)
    approval = re.compile(r"\b(?:human approval required|approved by [A-Za-z][A-Za-z .'-]+|approval recorded)\b", re.IGNORECASE)
    actionable = False
    for step in steps:
        body = step.group(0)
        requires_approval = destructive.search(body) or re.search(r"\bproduction\b", body, re.IGNORECASE)
        if requires_approval:
            actionable = True
            if not approval.search(body):
                errors.append(f"destructive or production plan step {step.group(1)} lacks affirmative step-specific approval")

    rollback = sections.get("rollback", "")
    rollback_is_none = bool(re.fullmatch(r"\s*[-*]?\s*(?:N/A|none)(?:[ \t]+[—-][ \t]+[^\r\n]+)?\s*", rollback, re.IGNORECASE))
    if actionable and rollback_is_none:
        errors.append("actionable destructive or production step requires preserved rollback artifact and recovery context")
    if rollback.strip() and not rollback_is_none:
        if not re.search(r"\b(namespace|context|cluster|environment)\b", rollback, re.IGNORECASE):
            errors.append("rollback must identify the target namespace/context")
        if not re.search(r"\b(?:artifact|preserve|backup)\b", rollback, re.IGNORECASE):
            errors.append("rollback must identify a preserved artifact")
        if not re.search(r"\b(?:recovery|recover|verify|verification|health)\b", rollback, re.IGNORECASE):
            errors.append("rollback must include a recovery check")

    return errors


def main() -> None:
    if "--help" in sys.argv[1:]:
        print("Usage: python scripts/validate-output.py < operational-plan.txt")
        print("Reads the risk, plan, checks, rollback, and security sections from stdin.")
        print("Prints a JSON result to stdout and exits 0 when valid or 1 when invalid.")
        return

    input_text = sys.stdin.buffer.read().decode("utf-8")
    errors = validate(input_text)
    result = {"valid": not errors, "errors": errors}
    print(json.dumps(result))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
