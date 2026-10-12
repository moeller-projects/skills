#!/usr/bin/env python3
"""Package a skill directory into a distributable .skill file (a zip archive).

Validates the skill first; refuses to package when spec errors exist.
Warnings do not block packaging unless --strict is given.

Usage:
    python3 scripts/package_skill.py <skill-dir> [output-directory] [--strict]

Exit codes:
    0  package created
    1  validation errors (no package created)
    2  usage error
"""

import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skill import validate_skill  # noqa: E402

EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".pytest_cache"}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    if not args:
        print(__doc__)
        sys.exit(2)
    skill_dir = Path(args[0]).resolve()
    out_dir = Path(args[1]).resolve() if len(args) > 1 else Path.cwd()
    if not skill_dir.is_dir():
        print(f"Error: skill directory not found: {skill_dir}")
        sys.exit(2)

    result = validate_skill(skill_dir)
    for e in result["errors"]:
        print(f"ERROR   {e}")
    for w in result["warnings"]:
        print(f"WARNING {w}")
    if result["errors"] or (strict and result["warnings"]):
        print("Packaging aborted — fix the problems above and re-run.")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{skill_dir.name}.skill"
    files = [
        p for p in skill_dir.rglob("*")
        if p.is_file() and not EXCLUDE_DIRS.intersection(p.relative_to(skill_dir).parts)
    ]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(files):
            zf.write(p, arcname=f"{skill_dir.name}/{p.relative_to(skill_dir)}")
    print(f"Packaged {len(files)} file(s) -> {target}")


if __name__ == "__main__":
    main()
