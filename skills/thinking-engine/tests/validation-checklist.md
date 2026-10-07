# Thinking Engine — Validation Checklist

Run this checklist before accepting a thinking-engine output as complete.

## Trigger Check

- [ ] Problem is vague, underspecified, or requires option comparison before implementation.
- [ ] Task is NOT exclusively implementation where the approach is already decided.

## Problem Statement Check

- [ ] Problem is restated in one sentence.
- [ ] Constraints are listed.
- [ ] Success bar is defined (how "done" is measured).

## Assumptions Check

- [ ] Assumptions are audited before options are generated.
- [ ] Each assumption has a risk level if it turns out to be wrong.
- [ ] No option is built on an unaudited assumption.

## Options Check

- [ ] At least 2 materially different options are generated (unless only 1 is viable).
- [ ] If only 1 option is viable: alternatives ruled out are listed with explicit reasons.
- [ ] Each option has pros, cons, and cost.

## Recommendation Check

- [ ] One option is selected with an explicit reason.
- [ ] Blind spots in the recommendation are listed.
- [ ] Open questions that block the recommendation are listed.

## Error Format

```text
error: <what went wrong during analysis>
assumption-violated: <which assumption turned out to be wrong>
recovery: <action taken — e.g., returned to problem restatement step>
```
