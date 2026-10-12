#!/usr/bin/env python3
"""Static contract checks for the debugging skill; run only when authorized."""

import importlib.util
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def load_validator():
    spec = importlib.util.spec_from_file_location("debugging_validator", SKILL_DIR / "scripts" / "validate-output.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_text


def main() -> None:
    required = [
        SKILL_DIR / "SKILL.md", SKILL_DIR / "metadata.json",
        SKILL_DIR / "scripts" / "validate-output.py",
        SKILL_DIR / "tests" / "validation-checklist.md",
        SKILL_DIR / "assets" / "templates" / "output.md",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing required files: " + ", ".join(missing))
    validate = load_validator()
    valid = """status: fixed
root_cause:
- finding: stale field name
- evidence: minimal repro and bisect
repro_steps:
- run the failing test
fix:
- update field name
verification:
- original repro passes
regression_check:
- fixture test passes
open_risks:
- none
"""
    if validate(valid):
        raise SystemExit("valid output rejected")
    invalid = valid.replace("status: fixed", "status: guessing").replace("- evidence: minimal repro and bisect", "- evidence:")
    errors = validate(invalid)
    if not any("status must be" in error for error in errors):
        raise SystemExit("invalid status not rejected")
    if not any("evidence" in error for error in errors):
        raise SystemExit("empty evidence not rejected")
    print("Debugging validation completed successfully.")


if __name__ == "__main__":
    main()
