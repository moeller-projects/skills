# Rule: Frontier Rounds

> Impact: high

## Description

Interview the user in rounds driven by a design tree: every open decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are already settled — the questions askable now without guessing at unheard answers.

## Apply When

- The problem stays vague after restatement, or alignment must be reached before options can be generated.

## Checks

- Each round asks the whole frontier, numbered, one decision per question.
- Every question carries a recommended answer, worded so "yes" accepts it.
- A question depending on another question still open this round belongs to a later round.
- Facts from the environment (filesystem, docs, tools) are looked up by the agent, never requested from the user; only decisions go to the user.
- The interview ends when the frontier is empty — nothing left silently assumed — and the user confirms shared understanding before anything is acted on.

## Anti-Pattern

Asking one question at a time with no recommendation, asking the user for facts the agent could look up, or generating options while load-bearing decisions are still open.
