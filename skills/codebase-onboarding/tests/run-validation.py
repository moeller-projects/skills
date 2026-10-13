#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate required Codebase Onboarding skill files and output contract consistency.
Inputs: Repository working tree containing the Codebase Onboarding skill directory.
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


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing {path.name}")


def run_validator(validator: Path, text: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(validator)],
        input=text,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def main() -> None:
    validator = SKILL_DIR / "scripts" / "validate-output.py"
    for required in [
        validator,
        SKILL_DIR / "assets" / "templates" / "output.md",
        SKILL_DIR / "tests" / "validation-checklist.md",
    ]:
        require_file(required)
    passed("codebase-onboarding required files exist")

    valid_contract = """repo_map:
- packages/skill-build — build and packaging logic
- skills — source skills and generated index

entrypoints:
- package.json scripts — validate, build, and pack commands

conventions:
- Versioning — Skills keep matching versions across metadata and SKILL frontmatter

hotspots:
- skills/INDEX.md — generated output changes whenever skill metadata changes

agent_artifacts:
- onboarding summary — use it to orient future agents
"""
    result = run_validator(validator, valid_contract)
    if result.returncode != 0 or result.stdout.strip() != "OK":
        fail(f"valid repo output unexpectedly failed: {result.stdout}{result.stderr}")
    passed("valid repo output passes")

    invalid_contract = """repo_map:
- packages/skill-build

entrypoints:
- package.json scripts — validate commands

conventions:
- Skills keep matching versions across metadata

hotspots:
- skills/INDEX.md — generated metadata output

agent_artifacts:
- onboarding summary — use it for orientation
"""
    result = run_validator(validator, invalid_contract)
    if result.returncode == 0 or "repo_map entries must include area" not in result.stderr:
        fail("invalid repo output unexpectedly passed")
    passed("validator rejects incomplete repo output")

    print("\nCodebase Onboarding validation completed successfully.")


if __name__ == "__main__":
    main()
