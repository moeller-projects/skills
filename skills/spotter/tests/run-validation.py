#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate required Spotter files and output contract behavior.
Inputs: Repository working tree containing the Spotter skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

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


def main() -> None:
    validator_path = SKILL_DIR / "scripts" / "validate-output.py"
    for required in [
        validator_path,
        SKILL_DIR / "assets" / "templates" / "output.md",
        SKILL_DIR / "tests" / "validation-checklist.md",
    ]:
        require_file(required)
    passed("spotter required files exist")

    namespace: dict[str, object] = {"__name__": "validate_output", "__file__": str(validator_path)}
    exec(validator_path.read_text(encoding="utf-8"), namespace)
    validate_text = namespace["validate_text"]
    valid_output = """problem:
- Need a rollout plan for adding real-time notifications.

assumptions:
- WebSocket infrastructure can be reused.

options:
1. Extend the existing WebSocket service.
2. Use a managed push service.

recommendation:
- Start with the managed push service to reduce operational load.

next:
- Confirm notification volume and budget constraints.
"""
    if validate_text(valid_output):
        fail("valid thinking output unexpectedly failed")
    passed("valid thinking output passes")

    invalid_output = """problem:
- Need a rollout plan for adding real-time notifications.

assumptions:
- WebSocket infrastructure can be reused.

options:
1. Extend the existing WebSocket service.

next:
- Confirm notification volume and budget constraints.
"""
    errors = validate_text(invalid_output)
    if "missing section: recommendation:" not in errors:
        fail("missing recommendation failure not reported")
    passed("validator rejects incomplete thinking output")

    crlf_output = valid_output.replace("\n", "\r\n")
    if validate_text(crlf_output):
        fail("valid CRLF thinking output unexpectedly failed")
    passed("validator accepts CRLF thinking output")

    whitespace_heading_output = valid_output.replace("options:\n", "options:  \n")
    if validate_text(whitespace_heading_output):
        fail("valid options heading with trailing spaces unexpectedly failed")
    passed("validator accepts trailing whitespace after options heading")

    print("\nSpotter validation completed successfully.")


if __name__ == "__main__":
    main()
