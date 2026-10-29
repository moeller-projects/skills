#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate required Discovery files and output contract behavior.
Outputs: PASS lines to stdout; FAIL diagnostics to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True

SKILL_DIR = Path(__file__).resolve().parents[1]

HELP = """Usage: python tests/run-validation.py

Validate the Discovery skill files and output contract. This command executes
the validation checks; use --help to print this usage without executing them.
"""


def passed(message: str) -> None:
    print(f"PASS: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing {path.name}")


def main() -> None:
    if "--help" in sys.argv[1:]:
        print(HELP, end="")
        return
    validator_path = SKILL_DIR / "scripts" / "validate-output.py"
    for required in [
        validator_path,
        SKILL_DIR / "assets" / "templates" / "output.md",
        SKILL_DIR / "tests" / "validation-checklist.md",
    ]:
        require_file(required)
    passed("discovery required files exist")

    spec = importlib.util.spec_from_file_location("validate_output", validator_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load validator at {validator_path}")
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    validate_text = validator.validate_text
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
    single_option = valid_output.replace(
        "2. Use a managed push service.\n",
        "",
    ).replace(
        "recommendation:\n",
        "ruled-out alternatives:\n- Managed push service — rejected because the vendor cannot meet residency requirements.\n\nrecommendation:\n",
    )
    if validate_text(single_option):
        fail("single viable option with ruled-out alternatives unexpectedly failed")
    passed("single-option fast path requires and accepts ruled-out alternatives")

    single_without_ruling_out = valid_output.replace("2. Use a managed push service.\n", "")
    if not any("at least two numbered options" in error for error in validate_text(single_without_ruling_out)):
        fail("single option without ruled-out alternatives not reported")
    passed("single option without ruled-out alternatives is rejected")

    bare_alternative = single_option.replace(
        "Managed push service — rejected because the vendor cannot meet residency requirements.",
        "Managed push service",
    )
    if not any("at least two numbered options" in error for error in validate_text(bare_alternative)):
        fail("bare ruled-out alternative without explanation not reported")
    passed("single-option ruling requires a separated explanation")

    whitespace_heading_output = valid_output.replace("options:\n", "options:  \n")
    if validate_text(whitespace_heading_output):
        fail("valid options heading with trailing spaces unexpectedly failed")
    passed("validator accepts trailing whitespace after options heading")

    print("\nDiscovery validation completed successfully.")


if __name__ == "__main__":
    main()
