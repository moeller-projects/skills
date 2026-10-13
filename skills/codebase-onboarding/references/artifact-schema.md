# Artifact Schema

Onboarding artifacts use one canonical sectioned-text format. Every section is required and contains one or more `- ` entries. A genuine absence is represented by exactly `- none`; omitted or empty sections are invalid.

```text
repo_map:
- <area or package> — <one-line responsibility and observed scope>

entrypoints:
- <path or command> — <why it matters and kind: runtime, build, test, or CI>

conventions:
- <observed convention with a concrete source or example>

hotspots:
- <area> — <concrete change risk and reason>

agent_artifacts:
- <artifact> — <how to use it>
```

The validator checks each section locally. It does not accept JSON, global counts, generic filler, or an absence marker mixed with substantive entries.
