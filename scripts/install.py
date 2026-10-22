#!/usr/bin/env python3
"""Install skills, together with the model-invoked primitives they require.

Reads each skill's generated ``metadata.json`` ``requires`` list (the
model-invoked primitives the skill composes, from Handoffs composition lines)
and copies the transitive closure. This replaces the README's manual "copy the
primitives named in Handoffs" step.

Dry-run by default: prints the plan and writes nothing. Pass ``--apply`` to
copy. ``--harness pi`` adds ``disable-model-invocation: true`` to the installed
frontmatter of user-invoked skills; ``generic`` copies them unchanged (the
"User-invoked only:" description prefix is the fallback on harnesses with no
such mechanism).

Usage:
    python scripts/install.py --dest DIR [--skill NAME ...] [--harness generic|pi]
        [--apply] [--force] [--json]

Exit codes:
    0  plan printed, or install completed
    1  a destination already exists and --force was not given
    2  usage error / unknown skill / missing metadata
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR.parent
SKIP_DIRS = {"__pycache__", ".git", ".baseline"}
SKIP_SUFFIXES = {".skill", ".pyc"}
HARNESSES = ("generic", "pi")
USER_INVOKED_FIELD = "disable-model-invocation: true"


def load_skills(root: Path) -> dict:
    skills = {}
    for skill_dir in sorted(p for p in (root / "skills").iterdir() if p.is_dir()):
        manifest_path = skill_dir / "metadata.json"
        if not manifest_path.is_file():
            raise SystemExit(f"error: missing {manifest_path}; run sync_manifests.py first")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        requires = manifest.get("requires", [])
        if not isinstance(requires, list):
            raise SystemExit(f"error: {manifest_path} requires must be a list")
        skills[skill_dir.name] = {
            "dir": skill_dir,
            "invocation": manifest.get("invocation", "model"),
            "requires": requires,
        }
    return skills


def closure(names: list[str], skills: dict) -> list[str]:
    ordered, seen = [], set()
    stack = list(names)
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        if name not in skills:
            raise SystemExit(f"error: unknown skill '{name}'")
        seen.add(name)
        ordered.append(name)
        stack.extend(skills[name]["requires"])
    return sorted(ordered)


def overlay(text: str, harness: str, invocation: str) -> str:
    if harness != "pi" or invocation != "user" or USER_INVOKED_FIELD in text:
        return text
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        lines.insert(1, USER_INVOKED_FIELD + "\n")
    return "".join(lines)


def copy_skill(name: str, skills: dict, dest: Path, harness: str, force: bool) -> None:
    source = skills[name]["dir"]
    target = dest / name
    if target.exists():
        if not force:
            raise SystemExit(f"error: {target} exists; pass --force to overwrite")
        shutil.rmtree(target)
    for path in sorted(source.rglob("*")):
        if SKIP_DIRS.intersection(path.relative_to(source).parts):
            continue
        if path.suffix in SKIP_SUFFIXES:
            continue
        relative = path.relative_to(source)
        if path.is_dir():
            (target / relative).mkdir(parents=True, exist_ok=True)
            continue
        (target / relative).parent.mkdir(parents=True, exist_ok=True)
        if relative.as_posix() == "SKILL.md":
            text = path.read_text(encoding="utf-8")
            (target / relative).write_text(
                overlay(text, harness, skills[name]["invocation"]), encoding="utf-8")
        else:
            shutil.copy2(path, target / relative)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--dest", type=Path, required=True,
                        help="destination skills directory")
    parser.add_argument("--skill", action="append", default=None,
                        help="skill to install (repeatable; default: all)")
    parser.add_argument("--harness", choices=HARNESSES, default="generic")
    parser.add_argument("--apply", action="store_true",
                        help="write the files (default: dry run)")
    parser.add_argument("--force", action="store_true",
                        help="overwrite an existing destination skill")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    if not (root / "skills").is_dir():
        print(f"error: no skills/ directory under {root}", file=sys.stderr)
        return 2
    skills = load_skills(root)
    requested = args.skill or sorted(skills)
    names = closure(requested, skills)

    results = []
    for name in names:
        target = args.dest.resolve() / name
        status = "would-write" if not args.apply else "written"
        if target.exists() and not args.force:
            status = "exists"
        results.append({"skill": name, "invocation": skills[name]["invocation"],
                        "target": str(target), "status": status})

    blocked = [r for r in results if r["status"] == "exists"]
    if args.json:
        print(json.dumps({"apply": args.apply, "harness": args.harness,
                          "dest": str(args.dest.resolve()), "results": results},
                         indent=2))
    else:
        verb = "Install" if args.apply else "Would install"
        print(f"{verb} {len(results)} skill(s) to {args.dest.resolve()} (harness: {args.harness})")
        for r in results:
            print(f"  {r['status']:>11}  {r['skill']} ({r['invocation']}-invoked)")
        if not args.apply:
            print("dry run; pass --apply to write")

    if blocked:
        print("destination already exists; pass --force to overwrite", file=sys.stderr)
        return 1
    if args.apply:
        for r in results:
            copy_skill(r["skill"], skills, args.dest.resolve(), args.harness, args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
