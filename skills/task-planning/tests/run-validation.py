#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate required Task Planning skill files and delivery plan output checks.
Inputs: Repository working tree containing the Task Planning skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
validator_source = (SKILL_DIR / "scripts" / "validate-output.py").read_text(encoding="utf-8")
validator_namespace: dict[str, object] = {"__name__": "delivery_validator"}
exec(compile(validator_source, str(SKILL_DIR / "scripts" / "validate-output.py"), "exec"), validator_namespace)
validate = validator_namespace["validate"]


def passed(message: str) -> None:
    print(f"PASS: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing {path.name}")


def assert_valid(plan: str, message: str) -> None:
    if validate(plan):
        fail(message)


def assert_invalid(plan: str, expected: str, message: str) -> None:
    errors = validate(plan)
    if not errors or expected not in "\n".join(errors):
        fail(message)


def main() -> None:
    validator = SKILL_DIR / "scripts" / "validate-output.py"
    for required in [
        validator,
        SKILL_DIR / "assets" / "templates" / "output.md",
        SKILL_DIR / "tests" / "validation-checklist.md",
    ]:
        require_file(required)
    passed("task-planning required files exist")

    assert_valid(
        """tasks:
- id: T-01
  title: Add reset token table
  estimate: S
  estimate_reliability: high
  depends_on: []
  done_when: Migration runs cleanly in staging.

- id: T-02
  title: Implement reset endpoint
  estimate: M
  estimate_reliability: high
  depends_on: [T-01]
  done_when: Endpoint returns 200 and stores hashed token. Unit tests pass.

dependencies:
- T-01 → T-02: token table must exist before endpoint writes tokens

risks:
- Token expiry not enforced at DB level — low / medium

critical_path:
- T-01 → T-02

unknowns: none

validation:
- Run full reset flow in staging end-to-end.
""",
        "valid delivery plan unexpectedly failed",
    )
    passed("valid delivery plan passes")

    assert_invalid(
        """tasks:
- id: T-01
  title: Add reset token table
  estimate: S
  estimate_reliability: high
  depends_on: []

done_when: misplaced
dependencies:
- none

risks:
- none

critical_path:
- T-01

unknowns: none

validation:
- Run staging smoke test.
""",
        "done_when",
        "missing done_when failure not reported",
    )
    passed("validator rejects tasks without done_when")

    assert_invalid(
        """tasks:
- id: T-01
  title: Add reset token table
  estimate: S
  estimate_reliability: high
  depends_on: []
  done_when: Migration runs in staging.

dependencies:
- none

risks:
- none

critical_path:
- T-01

validation:
- Run staging smoke test.
""",
        "unknowns",
        "missing unknowns section failure not reported",
    )
    passed("validator rejects plans without explicit unknowns section")

    assert_valid(
        """tasks:
- id: T-01
  title: Spike — audit REST endpoints for GraphQL migration
  timebox: 2 days
  estimate_reliability: low
  depends_on: []
  done_when: Schema candidates documented; U-01 resolved.

dependencies:
- none

risks:
- Schema design has wide blast radius — high / high

critical_path:
- T-01

unknowns:
- U-01: Target GraphQL schema undefined — owner: tech lead

validation:
- Re-run task-planning after spike resolves U-01.
""",
        "spike with timebox unexpectedly failed",
    )
    passed("spike with timebox passes without S/M/L estimate")

    assert_invalid(
        """tasks:
- id: T-01
  title: Ship a vertical reset slice
  estimate: S
  estimate_reliability: high
  depends_on: [T-99]
  done_when: User can request and confirm a reset.

dependencies:
- T-01 → T-99: invalid dependency
risks:
- none
critical_path:
- T-01 → T-99
unknowns: none
validation:
- Run the reset flow.
""",
        "unknown task T-99",
        "unknown dependency failure not reported",
    )
    passed("validator rejects unknown task references")

    assert_invalid(
        """tasks:
- id: T-01
  title: Ship a vertical reset slice
  estimate: S
  estimate_reliability: high
  depends_on: []
  done_when: User can request and confirm a reset.
dependencies:
- none
risks:
- none
critical_path:
- schema review
unknowns: none
validation:
- Run the reset flow.
""",
        "critical_path must list planned task ids",
        "non-task critical path failure not reported",
    )
    passed("validator rejects non-task critical path entries")

    assert_invalid(
        """tasks:
- id: T-01
  title: Ship first vertical slice
  estimate: S
  estimate_reliability: high
  depends_on: [T-02]
  done_when: First slice is verified.
- id: T-02
  title: Ship second vertical slice
  estimate: S
  estimate_reliability: high
  depends_on: [T-01]
  done_when: Second slice is verified.
dependencies:
- T-01 ↔ T-02: circular dependency
risks:
- none
critical_path:
- T-01 → T-02
unknowns: none
validation:
- Run both slices.
""",
        "dependency graph contains a cycle",
        "dependency cycle failure not reported",
    )
    passed("validator rejects dependency cycles")

    assert_invalid(
        """tasks:
- id: T-01
  title: Ship a vertical slice
  estimate: S
  estimate_reliability: high
  depends_on: []
  done_when: Slice is verified.
dependencies:
- T-01 → T-99: unknown edge
risks:
- none
critical_path:
- T-01
unknowns: none
validation:
- Verify the slice.
""",
        "dependencies section references unknown task",
        "unknown dependencies-section edge failure not reported",
    )
    passed("validator rejects unknown dependencies-section edges")

    assert_invalid(
        """tasks:
- id: T-01
  title: Ship prerequisite slice
  estimate: S
  estimate_reliability: high
  depends_on: []
  done_when: Prerequisite is verified.
- id: T-02
  title: Ship dependent slice
  estimate: S
  estimate_reliability: high
  depends_on: [T-01]
  done_when: Dependent slice is verified.
dependencies:
- T-02 → T-01: contradictory direction
risks:
- none
critical_path:
- T-01 → T-02
unknowns: none
validation:
- Verify both slices.
""",
        "contradicts",
        "contradictory dependencies-section edge failure not reported",
    )
    passed("validator rejects contradictory dependencies-section edges")
    print("\nTask Planning validation completed successfully.")


if __name__ == "__main__":
    main()
