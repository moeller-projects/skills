#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Spec Engine freeform spec and OpenSpec proposal outputs.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stdout when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys
from pathlib import Path


BANNED_WORDS = (
    "should", "might", "maybe", "as needed", "where appropriate", "etc",
    "and so on", "user-friendly", "better", "faster", "seamless", "intuitive",
)


def section(text: str, name: str) -> str:
    lines = text.splitlines()
    result = []
    active = False
    for line in lines:
        if line == f"{name}:":
            active = True
            continue
        if active and re.search(r"^[A-Za-z_][A-Za-z0-9_-]*:$", line):
            break
        if active:
            result.append(line)
    return "\n".join(result)


def spec_subsection(spec: str, name: str) -> str:
    lines = spec.splitlines()
    result = []
    active = False
    for line in lines:
        if re.search(rf"^- {re.escape(name)}:$", line):
            active = True
            continue
        if active and re.search(r"^- [A-Za-z_]+:$", line):
            break
        if active:
            result.append(line)
    return "\n".join(result)


def openspec_proposal_section(text: str) -> str:
    lines = text.splitlines()
    result = []
    active = False
    for line in lines:
        if line == "openspec_proposal:":
            active = True
            continue
        if active and re.search(r"^[^\s].*:\s*$", line):
            break
        if active:
            result.append(line)
    return "\n".join(result)


def named_block(text: str, name: str) -> str:
    lines = text.splitlines()
    result = []
    active = False
    for line in lines:
        if line == f"{name}:":
            active = True
            continue
        if active and re.search(r"^[^\s].*:\s*$", line):
            break
        if active:
            result.append(line)
    return "\n".join(result)


def field_value(proposal: str, field: str) -> str:
    match = re.search(rf"^  {re.escape(field)}:\s*(.*)$", proposal, re.MULTILINE)
    return match.group(1) if match else ""


def delta_paths(proposal: str) -> list[str]:
    lines = proposal.splitlines()
    result = []
    active = False
    for line in lines:
        if line == "  delta_spec_files:":
            active = True
            continue
        if active and re.match(r"^  [a-zA-Z0-9_-]+:", line):
            break
        if active and re.match(r"^  - ", line):
            result.append(line[4:])
            continue
        if active and re.match(r"^  ", line):
            continue
        if active:
            break
    return result


def validate_delta(path: str, block: str, errors: list[str]) -> None:
    current = ""
    has_header = False
    has_requirement_header = False
    requirement = None
    requirement_section = ""
    normative = False
    scenarios = 0

    def flush() -> None:
        nonlocal requirement, requirement_section, normative, scenarios
        if requirement is not None and requirement_section in ("ADDED", "MODIFIED"):
            if not normative:
                errors.append(f"OpenSpec delta spec {path}: requirement \"{requirement}\" in {requirement_section} must include SHALL or MUST")
            if scenarios < 1:
                errors.append(f"OpenSpec delta spec {path}: requirement \"{requirement}\" in {requirement_section} must include at least one #### Scenario:")
        requirement = None
        requirement_section = ""
        normative = False
        scenarios = 0

    for line in block.splitlines():
        match = re.match(r"^## (ADDED|MODIFIED|REMOVED|RENAMED) Requirements$", line)
        if match:
            flush()
            has_header = True
            current = match.group(1)
            continue
        if line.startswith("### Requirement:"):
            flush()
            has_requirement_header = True
            requirement_section = current
            requirement = re.sub(r"^### Requirement:\s*", "", line)
            continue
        if requirement is not None:
            if re.match(r"^#### Scenario:", line):
                scenarios += 1
            elif requirement_section in ("ADDED", "MODIFIED") and re.search(r"(^|[^A-Za-z0-9_-])(SHALL|MUST)($|[^A-Za-z0-9_-])", line):
                normative = True
    flush()
    if not has_header:
        errors.append(f"OpenSpec delta spec {path}: must include at least one delta section header")
    if not has_requirement_header:
        errors.append(f"OpenSpec delta spec {path}: must include at least one ### Requirement: entry")


def validate_freeform(text: str, errors: list[str]) -> None:
    for name in ("spec", "quality_gates", "open_questions", "risk_tier"):
        if not re.search(rf"^{re.escape(name)}:", text, re.MULTILINE):
            errors.append(f"missing section: {name}:")
    spec = section(text, "spec")
    questions = section(text, "open_questions")
    match = re.search(r"^risk_tier:\s*(.*)$", text, re.MULTILINE)
    risk = match.group(1) if match else ""
    if risk and not re.search(r"^(Low|Medium|High|Critical)$", risk):
        errors.append("risk_tier must be one of: Low, Medium, High, Critical")
    if spec:
        scope = spec_subsection(spec, "scope")
        requirements = spec_subsection(spec, "requirements")
        acceptance = spec_subsection(spec, "acceptance_criteria")
        if not re.search(r"^[ \t]*- IN:", scope, re.MULTILINE):
            errors.append("missing IN scope entry")
        if not re.search(r"^[ \t]*- OUT:", scope, re.MULTILINE):
            errors.append("missing OUT scope entry")
        req_ids = re.findall(r"^[ \t]*- (REQ-[0-9][0-9]*):.*$", requirements, re.MULTILINE)
        if not req_ids:
            errors.append("requirements must include at least one REQ-XX item")
        banned = r"\b(?:" + "|".join(re.escape(word) for word in BANNED_WORDS) + r")\b"
        if re.search(banned, requirements, re.IGNORECASE):
            errors.append("requirements must be testable; found vague language in requirements")
        if len(req_ids) != len(set(req_ids)):
            errors.append("requirements must use unique REQ-XX identifiers")
        ac_lines = re.findall(r"^[ \t]*- AC-.*$", acceptance, re.MULTILINE)
        if not ac_lines:
            errors.append("acceptance criteria must include at least one AC-XX item")
        else:
            pattern = re.compile(r"^[ \t]*-[ \t]+(AC-[0-9][0-9]*)[ \t]+\((REQ-[0-9][0-9]*)\)[ \t]*:[ \t]+GIVEN[ \t]+.+[ \t]+WHEN[ \t]+.+[ \t]+THEN[ \t]+.+$")
            for line in ac_lines:
                match = pattern.match(line)
                if not match:
                    errors.append("acceptance criteria must use AC-XX (REQ-XX): GIVEN ... WHEN ... THEN ... format")
                elif match.group(2) not in req_ids:
                    errors.append("acceptance criteria must reference an existing REQ-XX item")
    if re.search(r"^[ \t]*- OQ-", questions, re.MULTILINE):
        for line in re.findall(r"^[ \t]*- OQ-.*$", questions, re.MULTILINE):
            if not re.match(r"^[ \t]*-[ \t]OQ-[0-9][0-9]*:.*[ \t]—[ \t]owner:\ .+[ \t]—[ \t]due:\ .+$", line):
                errors.append("open questions must include OQ-XX with owner and due date")
                break


def validate_openspec(text: str, errors: list[str]) -> None:
    if not re.search(r"^output_format:[ \t]*openspec$", text, re.MULTILINE):
        errors.append("OpenSpec output must set output_format: openspec")
    if not re.search(r"^openspec_proposal:$", text, re.MULTILINE):
        errors.append("OpenSpec output missing openspec_proposal")
    proposal = openspec_proposal_section(text)
    for field in ("path", "change_path", "metadata_file", "proposal_file", "delta_spec_files"):
        if not re.search(rf"^  {field}:", proposal, re.MULTILINE):
            errors.append(f"OpenSpec output missing openspec_proposal.{field}")
    if not re.search(r"^  metadata_file:[ \t]*\.openspec\.yaml$", proposal, re.MULTILINE):
        errors.append("OpenSpec output must use metadata_file: .openspec.yaml")
    if re.search(r"change\.yaml", proposal):
        errors.append("OpenSpec output must not emit change.yaml for v1.3.1")
    proposal_file = field_value(proposal, "proposal_file")
    if proposal_file:
        block = named_block(text, proposal_file)
        if not block:
            errors.append(f"OpenSpec output missing block: {proposal_file}")
        else:
            for header in ("## Why", "## What Changes", "## Capabilities", "## Impact"):
                if header not in block:
                    errors.append(f"OpenSpec {proposal_file} missing section: {header}")
    paths = delta_paths(proposal)
    if not paths:
        errors.append("OpenSpec output must include at least one openspec_proposal.delta_spec_files entry")
    for path in paths:
        block = named_block(text, path)
        if not block:
            errors.append(f"OpenSpec output missing block: {path}")
        else:
            validate_delta(path, block, errors)


def validate(text: str) -> list[str]:
    errors: list[str] = []
    if re.search(r"^output_format:[ \t]*openspec$", text, re.MULTILINE):
        validate_openspec(text, errors)
    else:
        validate_freeform(text, errors)
    return errors


def main() -> None:
    errors = validate(sys.stdin.read())
    if errors:
        print("INVALID output:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)
    print("OK")


if __name__ == "__main__":
    main()
