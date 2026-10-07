# Thinking Engine — Output Template

## Default (problem + assumptions + options + recommendation + next)

```text
problem:
- restatement: <one sentence restating the core problem>
- constraints: <known constraints>
- success-bar: <how "done" is defined>

assumptions:
- <assumption> — risk: low|medium|high if wrong

options:
1. <option name>: <one-sentence description>
   pros: <concrete advantages>
   cons: <concrete disadvantages>
   cost: low|medium|high

recommendation:
- choice: <option name>
- reason: <why this option wins given constraints and tradeoffs>
- blind-spots: <what this recommendation might miss>

next:
- <first concrete action>
- open: <unresolved question that must be answered before proceeding>
```

## Single-Option Fast Path (same sections)

```text
problem:
- restatement: <one sentence>
- constraints: <why only one path is viable>
- success-bar: <how to judge the decision>

assumptions:
- <assumption> — risk: low|medium|high if wrong

options:
1. <only viable option>: <why it still fits the constraints>

recommendation:
- choice: <only viable option>
- reason: <why alternatives were ruled out>
- blind-spots: <what still needs watching>

next:
- <first action>
- open: <one open question if any>
```

## Rules

- State assumptions before options; options built on unaudited assumptions are unreliable.
- Generate at least 2 materially different options unless only one is viable.
- State blind spots explicitly; do not omit risks to make the recommendation look cleaner.
- Open questions must block or gate the recommendation; list them last.
