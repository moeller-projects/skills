#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate required Doc Engine skill files and output contract behavior.
Inputs: Repository working tree containing the Doc Engine skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
validator_source = (SKILL_DIR / "scripts" / "validate-output.py").read_text(encoding="utf-8")
validator_namespace: dict[str, object] = {"__file__": str(SKILL_DIR / "scripts" / "validate-output.py")}
exec(compile(validator_source, str(SKILL_DIR / "scripts" / "validate-output.py"), "exec"), validator_namespace)
validate = validator_namespace["validate"]


def passed(message: str) -> None:
    print(f"PASS: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    validator = SKILL_DIR / "scripts" / "validate-output.py"
    for required in [
        validator,
        SKILL_DIR / "assets" / "templates" / "output.md",
        SKILL_DIR / "tests" / "validation-checklist.md",
    ]:
        if not required.is_file():
            fail(f"missing {required.name}")
    if "explicit approval" not in (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"):
        fail("overwrite approval gate missing")
    passed("doc-engine required files and approval gate exist")

    valid_doc = """doc:
- purpose: Help contributors run the skill build workflow correctly.
- audience: engineer unfamiliar with the repository layout.
- structure:
  1. Setup [tutorial] — install dependencies and prerequisites
  2. Validation [how-to] — explain validation and packaging commands
- format:
  - type: markdown
  - reason: repository-maintained developer documentation
- artifact:
  - README.md

changes:
- README.md — add setup and validation workflow notes

gaps:
- Need confirmed CI screenshots for the release section
"""
    if validate(valid_doc):
        fail("valid doc output rejected")
    passed("valid doc output passes")

    untagged_doc = """doc:
- purpose: Help contributors run the skill build workflow correctly.
- audience: engineer unfamiliar with the repository layout.
- structure:
  1. Setup — install dependencies and prerequisites
  2. Validation — explain validation and packaging commands

changes:
- README.md — add setup notes

gaps:
- None
"""
    untagged_errors = validate(untagged_doc)
    if not untagged_errors:
        fail("untagged structure entries unexpectedly passed")
    if not any("structure entry missing valid mode tag" in error for error in untagged_errors):
        fail("missing mode tag failure not reported")
    passed("validator rejects structure entries without mode tags")

    invalid_doc = """doc:
- purpose: Help contributors run the skill build workflow correctly.
- structure:
  1. Setup [tutorial] — install dependencies and prerequisites

changes:
- README.md — add setup notes

gaps:
- None
"""
    invalid_errors = validate(invalid_doc)
    if not invalid_errors:
        fail("invalid doc output unexpectedly passed")
    if "missing doc audience" not in invalid_errors:
        fail("missing audience failure not reported")
    passed("validator rejects incomplete doc output")

    html_doc = """doc:
- purpose: Help stakeholders review progress and risks.
- audience: product leadership, unfamiliar with repo implementation details.
- structure:
  1. Executive summary [explanation] — concise status for stakeholders
  2. Risks and blockers [reference] — current issues and mitigation
- format:
  - type: html
  - reason: read-only stakeholder communication artifact
- artifact:
  - weekly-engineering-update.html

changes:
- weekly-engineering-update.html — add standalone stakeholder report

gaps:
- None
"""
    if validate(html_doc):
        fail("html output contract rejected")
    passed("validator accepts html output contract")

    print("\nDoc Engine validation completed successfully.")


if __name__ == "__main__":
    main()
