#!/usr/bin/env python3
"""Static validation fixtures for the Git Workflow skill.

Run only when test execution is explicitly authorized.
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
namespace = {"__name__": "validator"}
source = (SKILL_DIR / "scripts" / "validate-output.py").read_text(encoding="utf-8")
exec(compile(source, str(SKILL_DIR / "scripts" / "validate-output.py"), "exec"), namespace)
validate = namespace["validate"]

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
    print("Git Workflow validation completed successfully.")


if __name__ == "__main__":
    main()
