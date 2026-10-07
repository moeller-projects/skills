#!/usr/bin/env python3
"""run-validation.py

Purpose: Validate Spec Engine required files, guidance overlap, and output validator behavior.
Inputs: Repository working tree containing the Spec Engine skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
validate_output = {"__name__": "validate_output"}
exec((SCRIPTS_DIR / "validate-output.py").read_text(encoding="utf-8"), validate_output)


def passed(message: str) -> None:
    print(f"PASS: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(text: str, expected: bool, message: str) -> None:
    actual = not validate_output["validate"](text)
    if actual != expected:
        fail(message)


VALID_SPEC = """spec:
- goal: Let customers reset their password securely.
- scope:
  - IN: self-service password reset for existing accounts
  - OUT: account recovery by phone support
- requirements:
  - REQ-01: The system sends a reset link to the verified account email address.
  - REQ-02: The reset link expires after 15 minutes.
- acceptance_criteria:
  - AC-01 (REQ-01): GIVEN a verified account WHEN the user requests a reset THEN the system emails a one-time reset link.
  - AC-02 (REQ-02): GIVEN a valid reset link WHEN 15 minutes elapse THEN the link is rejected.

risk_tier: Medium

quality_gates:
- [ ] Security review completed

open_questions:
- OQ-01: Which email provider owns the send quota? — owner: platform-team — due: sprint-24
"""

VALID_OPENSPEC = """output_format: openspec
openspec_proposal:
  path: proposals/
  change_path: openspec/changes/add-password-reset-flow/
  metadata_file: .openspec.yaml
  proposal_file: proposal.md
  delta_spec_files:
  - specs/auth/spec.md

proposal.md:
## Why
Reset flows are required for account recovery.
## What Changes
- Add reset-link capability with expiring token validation.
## Capabilities
- New: auth-reset-flow
## Impact
- Auth service, email service, and integration tests.

specs/auth/spec.md:
## ADDED Requirements
### Requirement: Password reset link delivery
The system MUST deliver reset links to verified account emails.

#### Scenario: Reset link sent
- **WHEN** a verified user requests password reset
- **THEN** the system sends a reset email with a one-time link
"""


def main() -> None:
    for required in (
        SCRIPTS_DIR / "validate-output.py",
        SKILL_DIR / "assets" / "templates" / "output.md",
        SKILL_DIR / "tests" / "validation-checklist.md",
    ):
        if not required.is_file():
            fail(f"missing {required.name}")
    skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for needle, message in (
        ("ado-gateway handoff JSON", "spec-engine ado-gateway handoff use-when entry missing"),
        ("pure OpenSpec governance with no spec-authoring step", "spec-engine OpenSpec governance avoid-when entry missing"),
        ("output_format=openspec", "spec-engine openspec output_format workflow entry missing"),
    ):
        if needle not in skill_text:
            fail(message)
    passed("spec-engine required files and overlap guard exist")

    check(VALID_SPEC, True, "valid spec output unexpectedly failed")
    passed("valid spec output passes")

    invalid = VALID_SPEC.replace("  - OUT: account recovery by phone support\n", "").replace(
        "The system sends a reset link", "The system should, where appropriate, send a reset link"
    ).replace(
        "GIVEN a verified account WHEN the user requests a reset THEN the system emails a one-time reset link.",
        "user can reset password",
    )
    errors = validate_output["validate"](invalid)
    for needle, message in (
        ("missing OUT scope entry", "missing OUT scope failure not reported"),
        ("requirements must be testable", "vague requirement failure not reported"),
        ("acceptance criteria must use AC-XX (REQ-XX)", "AC traceability failure not reported"),
    ):
        if not any(needle in error for error in errors):
            fail(message)
    passed("validator rejects incomplete or vague spec output")

    missing_req = VALID_SPEC.replace("REQ-02: The reset link expires after 15 minutes.", "REQ-99: The reset link expires after 15 minutes.")
    if not any("acceptance criteria must reference an existing REQ-XX item" in error for error in validate_output["validate"](missing_req)):
        fail("missing REQ reference failure not reported")
    passed("validator enforces AC to REQ traceability")

    duplicate = VALID_SPEC.replace("  - REQ-02:", "  - REQ-01:")
    if not any("requirements must use unique REQ-XX identifiers" in error for error in validate_output["validate"](duplicate)):
        fail("duplicate REQ failure not reported")
    passed("validator rejects duplicate REQ identifiers")

    invalid_risk = VALID_SPEC.replace("risk_tier: Medium", "risk_tier: Unknown")
    if not any("risk_tier must be one of" in error for error in validate_output["validate"](invalid_risk)):
        fail("invalid risk_tier failure not reported")
    passed("validator rejects invalid risk_tier values")

    check(VALID_OPENSPEC, True, "valid openspec output unexpectedly failed")
    passed("valid openspec output passes")

    scenario_only_normative = VALID_OPENSPEC.replace(
        "The system MUST deliver reset links to verified account emails.",
        "The system delivers reset links to verified account emails.",
    ).replace(
        "#### Scenario: Reset link sent",
        "#### Scenario: User MUST receive reset link",
    )
    errors = validate_output["validate"](scenario_only_normative)
    if not any("must include SHALL or MUST" in error for error in errors):
        fail("normative language in a scenario heading incorrectly satisfied its requirement")
    passed("validator requires normative language in the requirement body")

    openspec_invalid = VALID_OPENSPEC.replace("metadata_file: .openspec.yaml", "metadata_file: change.yaml").replace(
        "## Capabilities\n- New: auth-reset-flow\n", ""
    ).replace("## Impact\n- Auth service, email service, and integration tests.\n\nspecs/auth/spec.md:\n## ADDED Requirements\n", "specs/auth/spec.md:\n")
    errors = validate_output["validate"](openspec_invalid)
    for needle, message in (
        ("metadata_file: .openspec.yaml", "openspec metadata_file failure not reported"),
        ("must not emit change.yaml", "openspec change.yaml failure not reported"),
        ("proposal.md missing section: ## Capabilities", "openspec capabilities section failure not reported"),
        ("must include at least one delta section header", "openspec delta header failure not reported"),
    ):
        if not any(needle in error for error in errors):
            fail(message)
    passed("validator rejects invalid openspec output")

    structure_invalid = VALID_OPENSPEC.replace("  change_path:", "change_path:").replace("  metadata_file:", "metadata_file:").replace("  proposal_file:", "proposal_file:").replace("  delta_spec_files:", "delta_spec_files:")
    errors = validate_output["validate"](structure_invalid)
    for needle, message in (
        ("missing openspec_proposal.change_path", "openspec nested change_path failure not reported"),
        ("missing openspec_proposal.metadata_file", "openspec nested metadata_file failure not reported"),
    ):
        if not any(needle in error for error in errors):
            fail(message)
    passed("validator enforces openspec_proposal nested structure")

    no_normative = VALID_OPENSPEC.replace("MUST", "SHOULD")
    if not any("must include SHALL or MUST" in error for error in validate_output["validate"](no_normative)):
        fail("openspec SHALL/MUST failure not reported")
    passed("validator enforces SHALL/MUST for openspec ADDED/MODIFIED requirements")
    print("\nSpec Engine validation completed successfully.")


if __name__ == "__main__":
    main()
