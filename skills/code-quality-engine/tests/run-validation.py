#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate Code Quality Engine validator presence and severity ordering behavior.
Inputs: Repository working tree containing the Code Quality Engine skill directory.
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

    valid = """findings:
- [critical] src/auth.ts:12 — null dereference on token
  why: crashes request handling
  fix: guard missing token before access
- [high] src/cache.ts:88 — stale entry can leak data
  fix: invalidate cache on write

patch-plan:
1. src/auth.ts — add null guard
2. src/cache.ts — invalidate cache after mutation

risk:
- cache invalidation may reduce hit rate
"""
    result = run_validator(validator, valid)
    if result.returncode != 0 or result.stdout.strip() != "OK":
        fail(f"sorted findings unexpectedly failed validation: {result.stdout}{result.stderr}")
    passed("sorted findings pass validation")

    invalid = """findings:
- [low] src/log.ts:5 — message is noisy
  fix: lower log level
- [critical] src/auth.ts:12 — null dereference on token
  fix: guard missing token before access

patch-plan:
1. src/log.ts — lower log level
2. src/auth.ts — add null guard

risk:
- minor churn
"""
    result = run_validator(validator, invalid)
    if result.returncode == 0 or "findings are not sorted by severity" not in result.stdout:
        fail("severity ordering failure not reported")
    passed("severity ordering is enforced")

    print("\nCode Quality Engine validation completed successfully.")


if __name__ == "__main__":
    main()
