# Doc Engine — Validation Checklist

Run this checklist before accepting a documentation output as complete.

## Trigger Check

- [ ] Task involves writing or improving documentation, README, AGENTS.md, or developer guides.
- [ ] Task is NOT exclusively code implementation with no documentation component.

## Structure Check

- [ ] Purpose is stated in one sentence.
- [ ] Audience is identified with role and knowledge level.
- [ ] Document structure is defined before prose is written.

## Accuracy Check

- [ ] Every command is exact and verified.
- [ ] Every file path is accurate.
- [ ] Every workflow step can be executed without modification.

## Completeness Check

- [ ] All gaps are listed explicitly in the `gaps:` section.
- [ ] No gaps are silently omitted.
- [ ] Existing content is preserved; changes are presented as diffs, not full replacements.

## Error Format

```text
error: <what went wrong during documentation>
gap: <missing information that blocked completion>
recovery: <action taken — e.g., asked clarifying question, produced skeleton with TODOs>
```
