#!/usr/bin/env python3
"""Regenerate the generated catalog sections of README.md and AGENTS.md.

Generated regions are delimited by ``<!-- generated:NAME -->`` and
``<!-- /generated:NAME -->``. The skill table keeps its authored row order
(read from the current block) and regenerates each description from the
skill's ``summary``; new skills are appended alphabetically.

Blocks:
    skill-catalog               README skill table
    readme-validation-runners   README list of skills with a validation runner
    agents-validation-runners   AGENTS.md sentence naming those skills

Usage:
    python skills/skill-forge/scripts/sync_readme.py [--root PATH] [--check] [--json]

Exit codes:
    0  sections written, or already in sync under --check
    1  --check found drift
    2  usage error / missing markers or metadata
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR.parents[2]

BLOCKS = {
    "README.md": ("skill-catalog", "readme-validation-runners"),
    "AGENTS.md": ("agents-validation-runners",),
}


def marker_pattern(name: str) -> re.Pattern:
    return re.compile(
        r"<!-- generated:%s -->(.*?)<!-- /generated:%s -->" % (re.escape(name), re.escape(name)),
        re.DOTALL,
    )


def load_skills(root: Path) -> dict:
    skills = {}
    for skill_dir in sorted(p for p in (root / "skills").iterdir() if p.is_dir()):
        manifest_path = skill_dir / "metadata.json"
        if not manifest_path.is_file():
            raise SystemExit(f"error: missing {manifest_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        skills[skill_dir.name] = {
            "summary": manifest.get("summary", ""),
            "runner": (skill_dir / "tests" / "run-validation.py").is_file(),
        }
    return skills


def ordered_names(current_block: str, skills: dict) -> list[str]:
    order = []
    for name in re.findall(r"\[([a-z0-9-]+)\]\(skills/", current_block):
        if name in skills and name not in order:
            order.append(name)
    for name in sorted(skills):
        if name not in order:
            order.append(name)
    return order


def build_skill_catalog(current_block: str, skills: dict) -> str:
    lines = ["", "| Skill | Use it for |", "| --- | --- |"]
    for name in ordered_names(current_block, skills):
        lines.append(f"| [{name}](skills/{name}/) | {skills[name]['summary']} |")
    lines.append("")
    return "\n".join(lines)


def runner_lists(skills: dict) -> tuple[list[str], list[str]]:
    have = [n for n in sorted(skills) if skills[n]["runner"]]
    have_not = [n for n in sorted(skills) if not skills[n]["runner"]]
    return have, have_not


def build_readme_runners(skills: dict) -> str:
    have, have_not = runner_lists(skills)
    total = len(skills)
    lines = [
        "",
        f"Skills with `tests/run-validation.py` ({len(have)} of {total}):",
        "",
        ", ".join(f"`{n}`" for n in have) + ".",
        "",
        f"Skills without a runner ({len(have_not)}): "
        + ", ".join(f"`{n}`" for n in have_not) + ".",
        "",
    ]
    return "\n".join(lines)


def build_agents_runners(skills: dict) -> str:
    have, _ = runner_lists(skills)
    names = ", ".join(f"`{n}`" for n in have)
    return (
        f"\nSkills with `tests/run-validation.py` are {names}; run one only "
        "when test execution is explicitly authorized.\n"
    )


BUILDERS = {
    "skill-catalog": build_skill_catalog,
    "readme-validation-runners": lambda skills: build_readme_runners(skills),
    "agents-validation-runners": lambda skills: build_agents_runners(skills),
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    if not (root / "skills").is_dir():
        print(f"error: no skills/ directory under {root}", file=sys.stderr)
        return 2
    skills = load_skills(root)

    results = []
    for filename, blocks in BLOCKS.items():
        path = root / filename
        text = path.read_text(encoding="utf-8")
        updated = text
        for name in blocks:
            pattern = marker_pattern(name)
            match = pattern.search(updated)
            if not match:
                results.append({"file": filename, "block": name, "status": "missing-markers"})
                continue
            if name == "skill-catalog":
                content = build_skill_catalog(match.group(1), skills)
            else:
                content = BUILDERS[name](skills)
            replacement = f"<!-- generated:{name} -->{content}<!-- /generated:{name} -->"
            changed = match.group(0) != replacement
            updated = updated[:match.start()] + replacement + updated[match.end():]
            results.append({
                "file": filename,
                "block": name,
                "status": ("drift" if args.check else "written") if changed else "in-sync",
            })
        if updated != text and not args.check:
            with path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(updated)

    bad = [r for r in results if r["status"] not in ("in-sync", "written")]
    if args.json:
        print(json.dumps({"valid": not bad, "check": args.check, "results": results}, indent=2))
    else:
        for r in results:
            print(f"{r['status']:>14}  {r['file']}:{r['block']}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
