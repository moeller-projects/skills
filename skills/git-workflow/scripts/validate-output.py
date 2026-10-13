#!/usr/bin/env python3
"""Validate a Git Workflow output contract from stdin."""

import json
import re
import sys

SECTIONS = ("context:", "branch_strategy:", "commit_plan:", "operations:", "safety_notes:", "rollback:")
DESTRUCTIVE = ("reset --hard", "rebase", "push --force", "push -f")


def _value(block: str, field: str) -> str:
    match = re.search(rf"^[ \t]*(?:-[ \t]+)?{re.escape(field)}:[ \t]*([^\r\n]*)$", block, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _section(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}[ \t]*\n(?P<body>.*?)(?=^[a-z_]+:[ \t]*$|\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group("body") if match else ""


def _require_fields(errors: list[str], block: str, label: str, fields: tuple[str, ...]) -> None:
    for field in fields:
        if not _value(block, field):
            errors.append(f"{label} missing {field}")


def _items(block: str) -> list[str]:
    starts = list(re.finditer(r"(?m)^- ", block))
    return [
        block[start.start():starts[index + 1].start() if index + 1 < len(starts) else len(block)]
        for index, start in enumerate(starts)
    ]


def validate(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    errors: list[str] = []
    for section in SECTIONS:
        if re.search(rf"^{re.escape(section)}\s*$", text, re.MULTILINE) is None:
            errors.append(f"missing section: {section}")
        elif not _section(text, section).strip():
            errors.append(f"empty section: {section}")

    _require_fields(errors, _section(text, "context:"), "context", ("goal", "publication", "collaborators"))
    _require_fields(errors, _section(text, "branch_strategy:"), "branch_strategy", ("branch", "parent_or_base", "choice", "rationale"))

    commit_block = _section(text, "commit_plan:")
    commits = _items(commit_block)
    if not commits:
        errors.append("commit_plan must contain at least one '- commit:' item")
    for index, block in enumerate(commits, 1):
        label = f"commit {index}"
        _require_fields(errors, block, label, ("commit", "message", "breaking_footer"))
        message = _value(block, "message")
        if message and not re.match(r"^[a-z]+(?:\([^)]+\))?!?: [a-z][^\n.]*$", message):
            errors.append(f"{label} message must use type(scope): imperative description without a trailing period")
        footer = _value(block, "breaking_footer")
        if not footer or (footer.lower() != "none" and not footer.startswith("BREAKING CHANGE:")):
            errors.append(f"{label} breaking_footer must be none or start with BREAKING CHANGE:")

    operations_block = _section(text, "operations:")
    operation_headers = re.findall(r"(?m)^- id: (\S+)\s*$", operations_block)
    blocks = _items(operations_block)
    if not blocks:
        errors.append("operations must contain at least one '- id: O-NN' item")
    if len(blocks) != len(operation_headers):
        errors.append("operations contains malformed or unparseable items")
    if re.search(r"(?m)^- (?!id:\s*)\S", operations_block):
        errors.append("operations contains malformed or unparseable items")
    for index, block in enumerate(blocks, 1):
        label = f"operation {index}"
        operation_id = _value(block, "id")
        expected = f"O-{index:02d}"
        if operation_id != expected:
            errors.append(f"{label} id must be {expected}; unknown or out-of-order operation id: {operation_id or '<missing>'}")
        _require_fields(errors, block, label, ("command", "rationale", "risk", "confirmation", "blast_radius", "rollback"))
        command = _value(block, "command")
        risk = _value(block, "risk")
        confirmation = _value(block, "confirmation")
        blast = _value(block, "blast_radius")
        rollback = _value(block, "rollback")
        if any(token in command.lower() for token in DESTRUCTIVE):
            if risk != "destructive":
                errors.append(f"{label} unsafe history command must use risk: destructive")
            if not confirmation.startswith("REQUIRED:"):
                errors.append(f"{label} destructive operation requires confirmation: REQUIRED: ...")
            if not blast:
                errors.append(f"{label} destructive operation requires blast_radius")
            if not rollback or rollback.lower() == "not_applicable":
                errors.append(f"{label} destructive operation requires an exact rollback command")

    return errors


def main() -> None:
    if "--help" in sys.argv[1:]:
        print("Usage: validate-output.py < plan.txt\nValidate Git Workflow output contract mechanics.")
        return
    errors = validate(sys.stdin.read())
    result = {"valid": not errors, "errors": errors}
    print(json.dumps(result))
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
