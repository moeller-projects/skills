#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate Safety Car validator presence, status/severity enforcement, timeline timestamps, and follow-up ownership.
Inputs: Repository working tree containing the Safety Car skill directory.
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


VALID = """status: resolved
severity: SEV2

impact:
- checkout 500s for 18% of requests, 14:07Z-14:31Z

timeline:
- 14:07Z alerts — elevated 5xx
- 14:16Z on-call — rolled back deploy 1f42c

mitigation:
1. rolled back deploy 1f42c

root-cause:
- trigger: deploy 1f42c required a missing config key
- root cause: pipeline does not validate config keys

follow-ups:
- add config validation — owner: platform team

comms:
- status page updated
"""


def main() -> None:
    validator = SKILL_DIR / "scripts" / "validate-output.py"
    if not validator.is_file():
        fail("missing validate-output.py")
    passed("validator exists")

    result = run_validator(validator, VALID)
    if result.returncode != 0 or result.stdout.strip() != "OK":
        fail(f"valid incident unexpectedly failed validation: {result.stdout}{result.stderr}")
    passed("valid incident passes validation")

    bad_status = VALID.replace("status: resolved", "status: fixed")
    result = run_validator(validator, bad_status)
    if result.returncode == 0 or "invalid status" not in result.stdout:
        fail("invalid status not reported")
    passed("invalid status is rejected")

    bad_timeline = VALID.replace("- 14:07Z alerts — elevated 5xx", "- just now alerts — elevated 5xx")
    result = run_validator(validator, bad_timeline)
    if result.returncode == 0 or "missing UTC timestamp" not in result.stdout:
        fail("timeline timestamp failure not reported")
    passed("timeline timestamps are enforced")

    orphan_followup = VALID.replace("add config validation — owner: platform team", "add config validation")
    result = run_validator(validator, orphan_followup)
    if result.returncode == 0 or "missing owner" not in result.stdout:
        fail("ownerless follow-up not reported")
    passed("follow-up ownership is enforced")

    print("\nSafety Car validation completed successfully.")


if __name__ == "__main__":
    main()
