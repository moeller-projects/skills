#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate required Technical Writing skill files and output contract behavior.
Inputs: Repository working tree containing the Technical Writing skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""
import tempfile
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
    passed("technical-writing required files and approval gate exist")

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
    valid_html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Report</title><style>@media print { body { color: black; } }</style></head><body><main>Report body</main></body></html>"""
    invalid_variants = (
        valid_html.replace("<style>", '<link rel="stylesheet" href="https://example.invalid/x.css"><style>'),
        valid_html.replace("@media print { body { color: black; } }", '@import url("https://example.invalid/x.css");'),
        valid_html.replace("@media print { body { color: black; } }", "body { color: black; }"),
        valid_html.replace("<main>Report body</main>", ""),
        valid_html.replace('lang="en"', ""),
    )
    with tempfile.TemporaryDirectory() as directory:
        valid_path = Path(directory) / "valid.html"
        invalid_path = Path(directory) / "invalid.html"
        valid_path.write_text(valid_html, encoding="utf-8")
        artifact_contract = html_doc.replace("weekly-engineering-update.html", str(valid_path))
        if validate(artifact_contract, str(valid_path)):
            fail("valid supplied HTML artifact rejected")
        passed("validator accepts actual full HTML with attributes, style, and print rules")
        mismatch_errors = validate(artifact_contract, str(invalid_path))
        if not any("does not match declared" in error for error in mismatch_errors):
            fail("artifact path mismatch was not rejected")
        passed("validator rejects an artifact different from the declared path")
        for artifact in invalid_variants:
            invalid_path.write_text(artifact, encoding="utf-8")
            declared_contract = html_doc.replace("weekly-engineering-update.html", str(invalid_path))
            if not validate(declared_contract, str(invalid_path)):
                fail("invalid supplied HTML artifact was accepted")
        passed("validator rejects external or incomplete supplied HTML artifacts")
    decision = "decision:\n  context: c\n  decision: d\n  reasoning: r\n  tradeoffs: t\n  reuse_scope: s\n"
    if not any("--html-artifact requires" in error for error in validate(decision, "missing.html")):
        fail("artifact option did not reject non-document contract")
    passed("artifact option rejects non-HTML contract")

    print("\nTechnical Writing validation completed successfully.")


if __name__ == "__main__":
    main()
