#!/usr/bin/env python3
"""Validate a Git Workflow output contract from stdin."""

import re
import sys

SECTIONS = ("context:", "branch_strategy:", "commit_plan:", "operations:", "safety_notes:", "rollback:")
DESTRUCTIVE = ("reset --hard", "rebase", "push --force", "push -f")


def _value(block: str, field: str) -> str:
    match = re.search(rf"^  {re.escape(field)}:\s*(.*?)\s*$", block, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _section(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}\s*$\n(?P<body>.*?)(?=^[a-z_]+:\s*$|\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group("body") if match else ""


def _require_fields(errors: list[str], block: str, label: str, fields: tuple[str, ...]) -> None:
    for field in fields:
        if not _value(block, field):
            errors.append(f"{label} missing {field}")

def validate(text: str) -> list[str]:
    errors: list[str] = []
    for section in SECTIONS:
        if re.search(rf"^{re.escape(section)}\s*$", text, re.MULTILINE) is None:
            errors.append(f"missing section: {section}")

    _require_fields(errors, _section(text, "context:"), "context", ("goal", "publication", "collaborators"))
    _require_fields(errors, _section(text, "branch_strategy:"), "branch_strategy", ("branch", "parent_or_base", "choice", "rationale"))
    _require_fields(errors, _section(text, "commit_plan:"), "commit_plan", ("commit", "message", "breaking_footer"))

    operations_match = re.search(r"^operations:\s*$\n(?P<body>.*?)(?=^[a-z_]+:\s*$|\Z)", text, re.MULTILINE | re.DOTALL)
    blocks = re.findall(r"(?ms)^- id: O-[0-9]+\n.*?(?=^- id: O-[0-9]+\n|\Z)", operations_match.group("body")) if operations_match else []
    if not blocks:
        errors.append("operations must contain at least one '- id: O-NN' item")
    for index, block in enumerate(blocks, 1):
        label = f"operation {index}"
        _require_fields(errors, block, label, ("command", "rationale", "risk", "confirmation", "blast_radius", "rollback"))
        command = _value(block, "command")
        risk = _value(block, "risk")
        confirmation = _value(block, "confirmation")
        blast = _value(block, "blast_radius")
        rollback = _value(block, "rollback")
        if risk not in {"safe", "cautious", "destructive"}:
            errors.append(f"{label} risk must be safe, cautious, or destructive")
        if any(token in command.lower() for token in DESTRUCTIVE):
            if not confirmation.startswith("REQUIRED:"):
                errors.append(f"{label} destructive operation requires confirmation: REQUIRED: ...")
            if not blast:
                errors.append(f"{label} destructive operation requires blast_radius")
            if not rollback or rollback.lower() == "not_applicable":
                errors.append(f"{label} destructive operation requires an exact rollback command")

    commit_block = _section(text, "commit_plan:")
    message = _value(commit_block, "message")
    if message and not re.match(r"^[a-z]+(?:\([^)]+\))?!?: [a-z][^\n.]*$", message):
        errors.append("commit message must use type(scope): imperative description without a trailing period")
    footer = _value(commit_block, "breaking_footer")
    if not footer or (footer.lower() != "none" and not footer.startswith("BREAKING CHANGE:")):
        errors.append("breaking_footer must be none or start with BREAKING CHANGE:")

    rollback_block = _section(text, "rollback:")
    _require_fields(errors, rollback_block, "rollback", ("checkpoint", "command", "limits"))
    return errors


def main() -> None:
    if "--help" in sys.argv[1:]:
        print("Usage: validate-output.py < plan.txt\nValidate Git Workflow output contract mechanics.")
        return
    errors = validate(sys.stdin.read())
    if errors:
        print("INVALID output:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)
    print("OK")


if __name__ == "__main__":
    main()
