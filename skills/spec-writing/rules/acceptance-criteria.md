# Rule: Acceptance Criteria

> Impact: high

## Description

Write acceptance criteria that prove the requirement is complete, observable, and ready for testing or review. Every acceptance criterion is expressed as a behavior in GIVEN/WHEN/THEN form so it maps directly to a test.

## Apply When

- A requirement needs validation or sign-off conditions.

## Checks

- Every criterion is written in GIVEN/WHEN/THEN form: GIVEN a starting state, WHEN an action or event, THEN an observable, checkable outcome.
- Each criterion is testable and maps back to a specific requirement.
- Edge conditions and negative paths get their own GIVEN/WHEN/THEN — they are not folded into a happy-path criterion.
- The THEN states an observable outcome, not an implementation detail ("the API returns 409", not "the service calls the dedupe method").
- Independent outcomes are split into separate criteria rather than chained with "and then ... and then".

## Anti-Pattern

Using acceptance criteria as a restatement of the requirement with no verification detail, or writing prose criteria with no GIVEN/WHEN/THEN structure so there is no clear state, trigger, or checkable outcome.

Example:

- ❌ `AC-01 (REQ-01): The user can reset their password and it should work.`
- ✅ `AC-01 (REQ-01): GIVEN a registered user with a valid reset token WHEN they submit a new password meeting the policy THEN the password is updated and the token is invalidated.`
- ✅ (negative) `AC-02 (REQ-01): GIVEN an expired reset token WHEN the user submits a new password THEN the request is rejected with a 'token expired' error and the password is unchanged.`
