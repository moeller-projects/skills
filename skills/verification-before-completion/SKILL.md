---
name: verification-before-completion
description: Verify before claiming completion. Use when about to claim that work is complete, fixed, passing, or working, before committing, before creating pull requests, or before reporting status to the user. Run covered verification only when the user explicitly authorizes that operation; otherwise report unverified status with the precise verification gap. Evidence before assertions always. Do not use for proposing plans or hypotheses that make no completion claim, or for diagnosing an unknown failure (use debugging).
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Verification Before Completion
  version: "1.0.3"
  summary: Back every completion, fixed, or passing claim with fresh verification evidence, or an honest unverified status when execution is not authorized; use before reporting completion or success.
---

# Verification Before Completion

## Purpose

Ensure every claim that work is complete, fixed, or passing is backed by fresh, observed verification evidence — never by intent, code inspection, memory, or output from before the last change.


## Workflow

1. Name the exact claim you are about to make and the command that would prove it: the project's test suite, build, linter, or the original reproduction.
2. Check whether the user explicitly authorized that covered operation in the current conversation. Run the command fresh, in this turn, after the final change, only when authorized. If it is not authorized, do not run it; report `status: unverified` and name the exact verification gap.
3. Read the actual output when a command runs. Confirm the exit code and the expected success markers; a truncated, partial, or misread run is not evidence.
4. If verification fails, or the command cannot run, downgrade the claim and state the blocker. Never claim success because the change "should" work.
5. Only then report status, citing the command that was run and its observed result, or the missing authorization and resulting gap.

## Output Contract

Return exactly these fields:

```text
status: verified|unverified|failed
claim: <the completion or success claim being made>
evidence:
- command: <exact verification command run>
  result: <exit code and key observed output>
gaps:
- <what could not be verified, or "none">
```

`status` MUST be one of the three listed values. `evidence` MUST be non-empty when `status` is `verified`. A `verified` status requires the command to have been run after the final change, in the current turn.

## Handoffs

- Hand off failures whose root cause is unknown to `debugging`.
- Hand off missing or inadequate coverage revealed during verification to `test-strategy`.
- Hand off verified work that needs commit, branch, or history planning to `git-workflow`.

## Error Handling

1. If the verification command or environment is unavailable, report `status: unverified`, state the exact missing prerequisite, and propose the closest runnable alternative.
2. If the user has not explicitly authorized the covered verification operation, do not run it; report `status: unverified`, state that authorization is missing, and identify the exact unobserved evidence.
3. If results are flaky, rerun only when the user explicitly authorized the covered operation, and report the flakiness explicitly; do not claim `verified` from a single green run of a flaky check.
4. If only part of the claim can be verified, claim only that part and list the rest under `gaps`.

## Validation Checklist

- [ ] The exact claim is named before any status is reported.
- [ ] The verification command was run fresh in the current turn, after the final change.
- [ ] Exit code and actual output were read, not assumed.
- [ ] No success claim rests on intent, inspection, memory, or stale output.
- [ ] Failures, blockers, and partial verification downgrade the status and appear in `gaps`.
- [ ] The reported status cites the command and its observed result.
