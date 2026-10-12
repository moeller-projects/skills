#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate PR Review validator presence, severity ordering, and verdict consistency behavior.
Inputs: Repository working tree containing the PR Review skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

import subprocess
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


def passed(message: str) -> None:
    print(f"PASS: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def run_validator(validator: Path, input_text: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(validator)],
        input=input_text,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def main() -> None:
    validator = SKILL_DIR / "scripts" / "validate-output.py"
    if not validator.is_file():
        fail("missing validate-output.py")
    passed("validator exists")

    valid = """verdict: request-changes
summary: adds discount logic; division by zero unguarded

findings:
- [blocker] src/discount.ts:14 — division by zero
  why: NaN totals
  suggestion: guard itemCount
- [nit] src/discount.ts:3 — abbreviated name
  why: consistency
  suggestion: rename to percentage

out-of-scope:
- legacy pricing uses floats

risk:
- one-time price change on re-render
"""
    result = run_validator(validator, valid)
    if result.returncode != 0 or result.stdout.strip() != "OK":
        fail(f"valid review unexpectedly failed validation: {result.stdout}{result.stderr}")
    label_outside_findings = valid.replace(
        "summary: adds discount logic; division by zero unguarded",
        "summary: [BLOCKER] adds discount logic; division by zero unguarded",
    )
    result = run_validator(validator, label_outside_findings)
    if result.returncode != 0 or result.stdout.strip() != "OK":
        fail("severity labels outside findings were incorrectly rejected")
    passed("severity labels are scoped to findings")

    passed("valid review passes validation")

    unsorted = """verdict: request-changes
summary: findings out of order

findings:
- [nit] src/a.ts:1 — trivial
  why: taste
  suggestion: rename
- [blocker] src/b.ts:2 — defect
  why: data loss
  suggestion: guard

out-of-scope:
- none

risk:
- none
"""
    result = run_validator(validator, unsorted)
    if result.returncode == 0 or "not sorted by severity" not in result.stdout:
        fail("severity ordering failure not reported")
    passed("severity ordering is enforced")

    bad_verdict = """verdict: approve
summary: approve with open blocker

findings:
- [blocker] src/auth.ts:9 — session not revoked
  why: hijacked session survives
  suggestion: revoke sessions

out-of-scope:
- none

risk:
- none
"""
    result = run_validator(validator, bad_verdict)
    if result.returncode == 0 or "verdict is approve but blocker or major findings exist" not in result.stdout:
        fail("verdict/findings inconsistency not reported")
    passed("verdict consistency is enforced")
    empty_request_changes = """verdict: request-changes
summary: no findings

findings:

out-of-scope:
- none

risk:
- none
"""
    result = run_validator(validator, empty_request_changes)
    if result.returncode == 0 or "no blocker or major finding exists" not in result.stdout:
        fail("request-changes without findings not reported")
    passed("request-changes requires a blocker or major finding")

    incomplete_finding = valid.replace("  why: NaN totals\n", "").replace("  suggestion: guard itemCount\n", "")
    result = run_validator(validator, incomplete_finding)
    if result.returncode == 0 or "each finding must include why" not in result.stdout or "each finding must include suggestion" not in result.stdout:
        fail("incomplete finding quality not reported")
    passed("finding quality fields are enforced")

    print("\nPR Review validation completed successfully.")


if __name__ == "__main__":
    main()
