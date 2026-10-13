# Agent Skills specification (condensed)

Field constraints below summarize the agentskills.io specification. The bundled
validator checks these field types and limits, manifest synchronization when
`metadata.json` exists, and the resource-layout checks described below; it does
not replace official validation or behavioral evaluation.

## Directory structure

```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional: executable code
├── references/       # Optional: docs loaded into context on demand
├── assets/           # Optional: files used in the output
└── ...               # Any additional files/dirs are permitted
```

Only `SKILL.md` is required. Create optional directories only when used.
`SKILL.md` = YAML frontmatter (`---` fenced) + Markdown body.

## Frontmatter fields

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars; lowercase unicode alphanumerics and `-`; no leading/trailing/consecutive hyphens; must equal parent directory name |
| `description` | Yes | 1-1024 chars; non-empty; what it does + when to use it |
| `license` | No | License name or reference to a bundled license file |
| `compatibility` | No | 1-500 chars; environment requirements (product, packages, network). Most skills don't need it |
| `metadata` | No | Map of string keys to string values; use reasonably unique keys |
| `allowed-tools` | No | Space-separated pre-approved tools, e.g. `Bash(git:*) Read` (experimental) |

No other fields are allowed. Parsing note: official tooling uses strict YAML —
quote values containing `:` and prefer folded blocks (`>`) for long descriptions.

## Body

No format restrictions. Recommended: step-by-step instructions, input/output
examples, edge cases. The whole body loads when the skill activates, so keep it
under ~500 lines / 5,000 tokens; split detail into `references/` files.

## Progressive disclosure (three levels)

1. **Metadata** (~100 tokens, always loaded): name + description.
2. **SKILL.md body** (<5,000 tokens, loaded on activation).
3. **Resources** (loaded on demand; scripts can run without being read).

Implication: the description alone decides triggering; anything needed at
decision time must live there, not in the body.

## File references

Reference bundled files with paths relative to the skill root:
`references/schema.md`, `scripts/extract.py`. Keep references one level deep
from SKILL.md — no reference file should depend on reading another reference
file. For reference files >100 lines, add a table of contents at the top.

## Validation

Official: `skills-ref validate ./my-skill` (from the agentskills/skills-ref
package). The bundled `scripts/validate_skill.py` checks field types, required
values, names, limits, known frontmatter fields, and synchronized manifest
identity/tool declarations. Layout lint includes `rules/`, `tests/`, and `evals/`
as well as scripts, assets, and references. `--strict` treats lint warnings as
failures; `--json` emits diagnostics.

These checks cannot establish trigger precision, truth of instructions,
semantic output completeness, runtime safety, or when a resource should be read.
Review those separately and run authorized behavioral checks.
