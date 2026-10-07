# Happy-Path Example — Spec Engine

## Scenario

Product manager says: "We need a user password reset flow via email."

## Input Context

- Web app with existing user accounts stored in Postgres.
- Email service: SendGrid, already integrated.
- Audience: end users who have forgotten their password.
- No existing reset flow.

## Expected Output

```text
spec:
- goal: allow authenticated users to reset their password via a time-limited email link
- scope:
  - IN: request reset link, send email, validate token, set new password
  - OUT: social login recovery, admin-initiated reset, SMS recovery
- requirements:
  - REQ-01: system sends a password reset email within 60 seconds of a valid reset request
  - REQ-02: reset token expires after 15 minutes and is single-use
  - REQ-03: new password must meet existing password policy (min 8 chars, 1 uppercase, 1 digit)
  - REQ-04: reset link is invalidated after successful use
- acceptance_criteria:
  - AC-01 (REQ-01): GIVEN a registered email is submitted WHEN reset is requested THEN an email arrives within 60 seconds
  - AC-02 (REQ-02): GIVEN a reset token WHEN 16 minutes have elapsed THEN the link returns a 410 Gone response
  - AC-03 (REQ-02): GIVEN a reset token was used once WHEN used again THEN the link returns a 410 Gone response
  - AC-04 (REQ-03): GIVEN a new password of 7 characters WHEN submitted THEN validation rejects it with a clear error
  - AC-05 (REQ-04): GIVEN a successful reset WHEN the same link is clicked THEN it returns 410 Gone

quality_gates:
- [ ] Security review: token generation uses cryptographically secure random bytes (not UUID v4)
- [ ] Rate limiting: reset endpoint is rate-limited to prevent enumeration

risk_tier: Medium

open_questions:
- OQ-01: what should happen for unregistered emails? — owner: PM — due: sprint planning
```

## Why This Is Correct

- Goal is one sentence and outcome-focused.
- Scope explicitly excludes alternatives so there is no ambiguity.
- All requirements are testable (no "should" or vague language).
- All AC follow GIVEN/WHEN/THEN.
- Security gates are explicit.
- Open question is flagged rather than resolved by assumption.

## OpenSpec Serialization (same spec, different output_format)

```text
output_format: openspec
openspec_proposal:
  path: proposals/
  change_path: openspec/changes/add-password-reset-flow/
  metadata_file: .openspec.yaml
  proposal_file: proposal.md
  delta_spec_files:
  - specs/auth/spec.md

.openspec.yaml:
  schema: spec-driven
  created: 2026-05-14

proposal.md:
## Why
Password reset is required for account recovery.

## What Changes
- Add reset-link request, token validation, and password update flow.

## Capabilities
- auth-password-reset

## Impact
- Auth service, email delivery, and integration tests.

specs/auth/spec.md:
## ADDED Requirements
### Requirement: Password reset via emailed link
The system MUST let a registered user request a password reset email with a time-limited single-use link.

#### Scenario: Password reset email sent
- **WHEN** a registered user requests a password reset
- **THEN** the system sends a reset email with a single-use link
```
