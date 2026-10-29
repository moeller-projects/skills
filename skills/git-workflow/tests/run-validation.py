#!/usr/bin/env python3
"""Static validation fixtures for the Git Workflow skill.

Run only when test execution is explicitly authorized.
"""

import importlib.util
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location(
    "git_workflow_validator", SKILL_DIR / "scripts" / "validate-output.py"
)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load Git Workflow validator")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
validate = validator.validate

VALID = """context:
- goal: split parser work
- publication: private
- collaborators: none
branch_strategy:
- branch: feat/parser-tokenizer
- parent_or_base: main
- choice: rebase
- rationale: private linear cleanup
commit_plan:
- commit: implementation
  message: feat(parser): add quoted token support
  breaking_footer: none
- commit: parser tests
  message: test(parser): cover quoted token support
  breaking_footer: none
operations:
- id: O-01
  command: git status --short
  rationale: inspect state
  risk: safe
  confirmation: not_required
  blast_radius: none; read-only
  rollback: not_applicable
- id: O-02
  command: git rebase -i main
  rationale: split private commits
  risk: destructive
  confirmation: REQUIRED: confirm private branch
  blast_radius: rewrites local branch commits
  rollback: git reset --hard rescue/parser
safety_notes:
- never rewrite shared history
rollback:
- checkpoint: rescue/parser
- command: git reset --hard rescue/parser
- limits: later work needs reflog
"""


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    required = [SKILL_DIR / "SKILL.md", SKILL_DIR / "metadata.json", SKILL_DIR / "scripts" / "validate-output.py"]
    required += [SKILL_DIR / "tests" / "validation-checklist.md", SKILL_DIR / "assets" / "templates" / "output.md"]
    for path in required:
        if not path.is_file():
            fail(f"missing {path}")
    if validate(VALID):
        fail("valid output unexpectedly rejected")
    print("PASS: valid contract")
    invalid = VALID.replace("confirmation: REQUIRED: confirm private branch", "confirmation: not_required").replace("rollback: git reset --hard rescue/parser", "rollback: not_applicable", 1)
    errors = validate(invalid)
    if not any("destructive operation requires confirmation" in error for error in errors):
        fail("destructive confirmation failure not reported")
    if not any("destructive operation requires an exact rollback" in error for error in errors):
        fail("destructive rollback failure not reported")
    print("PASS: destructive safety is enforced")

    malformed_commit = VALID.replace(
        "  message: test(parser): cover quoted token support\n  breaking_footer: none",
        "  message: malformed message\n  breaking_footer: none",
        1,
    )
    if malformed_commit == VALID:
        fail("later commit fixture mutation did not apply")
    if not any("commit 2 message must use" in error for error in validate(malformed_commit)):
        fail("malformed later commit message was accepted")
    unknown_id = VALID.replace("- id: O-02", "- id: XYZ")
    if not any("unknown or out-of-order operation id" in error for error in validate(unknown_id)):
        fail("unknown operation id was accepted")
    missing_id = VALID.replace("- id: O-02", "- command: git status --short")
    if not any("malformed or unparseable items" in error for error in validate(missing_id)):
        fail("missing operation id was accepted")
    empty_safety = VALID.replace("safety_notes:\n- never rewrite shared history", "safety_notes:\nrollback:")
    if not any("empty section: safety_notes:" in error for error in validate(empty_safety)):
        fail("empty safety section was accepted")
    heading_only_plan = VALID.replace("commit_plan:\n- commit: implementation\n  message: feat(parser): add quoted token support\n  breaking_footer: none\n- commit: parser tests\n  message: test(parser): cover quoted token support\n  breaking_footer: none", "commit_plan:\n")
    if not any("empty section: commit_plan:" in error for error in validate(heading_only_plan)):
        fail("heading-only commit plan was accepted")
    print("PASS: commit and operation item validation is enforced")
    print("Git Workflow validation completed successfully.")


if __name__ == "__main__":
    main()
