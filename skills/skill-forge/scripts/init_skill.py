#!/usr/bin/env python3
"""Initialize a new Agent Skill directory with a spec-compliant SKILL.md template.

Usage:
    python3 scripts/init_skill.py <skill-name> --path <output-directory>

Example:
    python3 scripts/init_skill.py pdf-form-filler --path ./skills

Creates <output-directory>/<skill-name>/ containing SKILL.md with placeholder
TODOs. Resource directories (scripts/, references/, assets/) are NOT created —
add only the ones the skill actually needs.
"""

import json
import re
import sys
from pathlib import Path

HELP = "Usage: python scripts/init_skill.py <skill-name> --path <output-directory>"

SKILL_TEMPLATE = """---
name: {skill_name}
description: "TODO: What the skill does + when to use it. Include specific trigger contexts: file types, task verbs, and situations where the user does not name the domain directly. Max 1024 chars."
metadata:
  title: "{skill_title}"
  version: "1.0.0"
  summary: "TODO: Summarize this skill's capability."
  invocation: "model"
---

# {skill_title}

## Overview

[TODO: 1-2 sentences. What capability does this skill add?]

## Workflow

[TODO: Numbered steps the agent follows. Calibrate specificity to fragility:
exact commands for brittle operations, judgment-based guidance for flexible
ones. Reference bundled resources with paths relative to the skill root, e.g.
`scripts/do_thing.py` or `references/schema.md`, and state WHEN to read each
reference file.]

## Gotchas

[TODO: Concrete, non-obvious failure modes and their fixes — the corrections a
user would otherwise have to give. Delete this section if none.]
"""

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print(HELP)
        sys.exit(0)
    if len(args) != 3 or args[1] != "--path":
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    name, out_dir = args[0], Path(args[2])
    if not NAME_RE.match(name) or len(name) > 64:
        print(
            f"Error: '{name}' is not a valid skill name. Use 1-64 lowercase "
            "letters, digits, and single hyphens (no leading/trailing/double "
            "hyphens).",
            file=sys.stderr,
        )
        sys.exit(2)
    skill_dir = out_dir / name
    if skill_dir.exists():
        print(f"Error: directory already exists: {skill_dir}", file=sys.stderr)
        sys.exit(2)
    skill_dir.mkdir(parents=True)
    title = name.replace("-", " ").title()
    (skill_dir / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(skill_name=name, skill_title=title)
    )
    (skill_dir / "metadata.json").write_text(json.dumps({
        "name": name,
        "title": title,
        "version": "1.0.0",
        "summary": "TODO: Summarize this skill's capability.",
        "invocation": "model",
    }, indent=2) + "\n")
    print(json.dumps({
        "status": "created",
        "skill_dir": str(skill_dir),
        "files": ["SKILL.md", "metadata.json"],
        "next": "replace every [TODO] section",
    }))


if __name__ == "__main__":
    main()
