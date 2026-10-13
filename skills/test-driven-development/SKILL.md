---
name: test-driven-development
description: Drive implementation with a failing test first, or write regression tests for behavior whose implementation is already handled. Use when implementing a feature, bugfix, refactoring, or behavior change, or for a test-only regression request; distinguish test-only coverage work from implementing the fix. Before writing implementation code, write the test first. Do not use for diagnosing a failure with unknown root cause (use debugging), designing an overall test suite or coverage plan (use test-strategy), or documentation-only and configuration-only changes with no behavior.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Test-Driven Development
  version: "1.1.3"
  summary: Drive behavior implementation with a failing test first, then minimal passing code and refactoring; use for feature, bugfix, and behavior-change tests.
---

# Test-Driven Development

## Purpose

Prove every behavior change with a test that was watched failing and then passing. A test never seen failing may test nothing; implementation written before its test has no executable specification.


## Workflow

1. Use the existing observable/public boundary by default: tests live where behavior can be observed without reaching inside. Name the seam and its rationale before writing the test. Ask the user only when seam placement is genuinely uncertain, because unnecessary confirmation delays a testable behavior slice.
2. Restate the required behavior as a testable assertion and pick the smallest next behavior slice.
3. RED: write the test first. Before running it, verify explicit authorization for test execution exists in the current request; test permission does not authorize implicit restore or build.
4. GREEN: write the minimal implementation that passes. Before running it, independently verify explicit authorization for test execution and any restore/build required by the command. If restore or build is not authorized, use existing prerequisites or record the exact gap.
5. REFACTOR: only cleanup that keeps the suite green, rerunning after each step when each required operation is explicitly authorized. Without authorization, record refactoring as unverified rather than claiming the suite is green.
6. Keep the test with the change. Repeat the cycle per behavior slice until the request is covered.


## Output Contract

Return exactly these fields per behavior slice:

```text
status: verified|unverified|red|blocked
cycle:
- behavior: <the behavior slice under test>
  red: <authorized test command and the observed failing output, or "unverified: run not authorized or unavailable">
  green: <minimal implementation change and the observed passing output, or "unverified: run not authorized or unavailable">
  refactor: <cleanup made, or "none">
open_risks:
- <untested edge or follow-up slice, or "none">
```

`status: verified` requires both the failing and passing runs to have been observed from authorized commands. `status: red` is reserved for an observed failing run when implementation is not yet complete. `status: unverified` means implementation work is complete but required runs were not authorized or available; it MUST NOT claim `green`. `status: blocked` is reserved for a prerequisite other than authorization that prevents the requested work. `green` in a cycle is reserved for an observed passing run.

## Handoffs

- Hand off failures with unknown root cause to `debugging`; return here with the confirmed cause.
- Hand off suite-level strategy, coverage planning, and flaky-test reduction to `test-strategy`.
- Hand off seam-placement and module-shape questions to `codebase-design`.
- Test-quality doctrine, including behavior-over-implementation guidance, belongs to `test-strategy`; consult it when choosing assertions and seams.
- Hand off final done-or-passing claims to `verification-before-completion`, which owns the completion evidence gate.
- Hand off commit boundaries and history planning for the finished slices to `git-workflow`.

## Error Handling

1. If the new test passes immediately, the behavior already exists or the test is wrong; investigate before writing any implementation.
2. If explicit authorization is absent, or the test command is unavailable, report `status: unverified`, state the exact verification gap, and continue implementation when the requested code change is otherwise actionable. Do not claim an observed RED or GREEN run.
3. If a failure cannot be reproduced as a failing test, hand off to `debugging` rather than guessing at a fix.
4. If the minimal pass tempts a hard-coded or fake implementation, note it in `open_risks` and add the next behavior slice that forces the general case.

## Validation Checklist

- [ ] Seams were named before the first test was written, with user input when placement was genuinely uncertain.
- [ ] The test was written before the implementation.
- [ ] The failing run was observed on the intended assertion, or the exact unauthorized/unavailable verification gap was recorded.
- [ ] The implementation is the minimal change that turns the test green; if it was not run, status remains unverified.
- [ ] No functionality was added beyond what a test demands.
- [ ] In-loop refactoring stayed green when authorized; otherwise its verification gap was recorded. Substantial redesign was deferred to review.
- [ ] The test ships together with the change.
- [ ] Exceptions (prototype, docs-only) were stated explicitly, not silently skipped.
