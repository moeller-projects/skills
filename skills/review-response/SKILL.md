---
name: review-response
description: Handle incoming code review feedback with technical verification instead of performative agreement. Use when you received PR review comments, change requests, or feedback on code you produced, before implementing any suggestion — especially when feedback seems unclear or technically questionable. Restate, verify against the codebase, then accept with a fix or push back with technical reasoning. Do not use for performing a review of someone else's code (use pr-review or code-review), feedback that reports a failure with unknown root cause (use debugging), or feedback that requires new behavior (use test-driven-development).
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Review Response
  version: "1.0.3"
  summary: Verify review feedback against the codebase, then implement or push back with technical reasoning; gate tests on explicit authorization and report unrun verification honestly.
---

# Review Response

## Purpose

Turn review feedback into verified, correctly-scoped changes. Technical correctness outranks social comfort: no performative agreement, no blind implementation, no gratitude phrases — actions and technical reasoning carry the response.


## Workflow

1. Read the complete feedback without reacting. Do not start implementing mid-read.
2. Restate each item as a technical requirement in your own words. If any item is unclear, stop and ask about it before implementing anything — items may be related, and partial understanding produces wrong implementations.
3. Verify each item against codebase reality: is it technically correct for this codebase, does it break existing behavior, is there a reason the code is as it is, does it hold across supported platforms and versions?
4. Evaluate scope: if a suggestion proposes "proper" infrastructure, check actual usage first — unused endpoints and unrequested features are YAGNI candidates to raise, not build.
5. Respond per item: implement what is correct, ask about what is unclear, push back with technical reasoning on what is wrong.
6. Implement accepted items one at a time, in order: blocking issues (breaks, security) first, then simple fixes, then complex refactoring. Run an individual test for each fix and check for regressions only when the user explicitly authorizes that covered operation; otherwise apply the fix, record that tests were not run because authorization is missing, and hand off the completion claim to `verification-before-completion`.
7. When replying to inline review threads on a forge, reply inside the comment thread, not as a new top-level comment.

## Output Contract

Return exactly these fields:

```text
feedback_items:
- item: <the review point, restated as a technical requirement>
  verdict: accepted|clarification-needed|declined
  evidence: <codebase observation or question supporting the verdict>
  action: <fix applied with observed test result when authorized, or fix applied with tests not run and the precise authorization gap; question asked, or pushback reasoning>
regressions:
- <checks run across the touched area, or "none">
open_risks:
- <items deferred or unresolved, or "none">
```

Every item MUST have a verdict; `accepted` requires an applied change and an action that records either an observed test result from explicitly authorized execution or that tests were not run because authorization was not provided. An unrun test MUST NOT be presented as verified. Never report an item accepted without the applied fix and an honest test status.

## Handoffs

- Hand off failures with unknown root cause surfaced by feedback to `debugging`.
- Hand off accepted behavior changes to `test-driven-development`.
- Hand off completion claims after all items are handled to `verification-before-completion`.
- Hand off performing a review of others' code to `pr-review`.

## Error Handling

1. If a suggestion cannot be verified with available evidence, say so and name what would settle it; ask whether to investigate, ask the reviewer, or proceed.
2. If a suggestion conflicts with the user's prior architectural decisions, stop and discuss with the user before implementing or declining.
3. If you pushed back and verification proves you wrong, correct factually in one line — state what you checked and what it showed — and implement; no apology, no defense of the earlier position.
4. If feedback items are batched ("fix 1-6") and some are unclear, name exactly which items you understand and which need clarification; implement nothing until the unclear ones are resolved.

## Validation Checklist

- [ ] All feedback was read before any implementation started.
- [ ] Every item was restated as a technical requirement or asked about.
- [ ] Every accepted item was verified against the codebase before implementation.
- [ ] No response contains performative agreement or gratitude phrases.
- [ ] Pushback cites technical reasoning: what breaks, what context is missing, or what usage check failed.
- [ ] Fixes were applied one at a time; each was individually tested when explicitly authorized, or explicitly marked tests not run with the authorization gap.
- [ ] Unclear batched items blocked implementation until clarified.
