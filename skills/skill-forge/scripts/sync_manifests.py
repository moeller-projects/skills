#!/usr/bin/env python3
"""Generate metadata.json manifests from SKILL.md frontmatter and catalog.json.

SKILL.md frontmatter is canonical for ``name``, ``title``, ``version``,
``summary``, ``invocation``, ``compatibility``, and ``allowed-tools``.
``catalog.json`` at the repository root supplies the catalog-only block:
``type``, ``risk_level``, ``requires_network``, and ``maintainer``.

The manifest does not carry ``activation``: ``use_when``/``avoid_when``
restate the description, which already carries the triggering burden. The
manifest ``compatibility`` is the harness list when the frontmatter value is a
plain comma-separated list of tokens, and the default harness list otherwise
(for example, when the frontmatter states a runtime requirement instead).

Usage:
    python skills/skill-forge/scripts/sync_manifests.py [--root PATH]
        [--catalog PATH] [--check] [--json]

Exit codes:
    0  manifests written, or already in sync under --check
    1  --check found drift
    2  usage error / missing catalog or skill
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR.parents[2]
DEFAULT_CATALOG = DEFAULT_ROOT / "catalog.json"

sys.path.insert(0, str(SCRIPT_DIR))
import validate_skill  # noqa: E402  (same directory)

DEFAULT_COMPATIBILITY = ["chatgpt", "codex", "claude-code", "cursor", "opencode"]
CATALOG_FIELDS = ("type", "risk_level", "requires_network", "maintainer")
TOKEN_RE = re.compile(r"^[a-z][a-z0-9-]*$")
KEBAB_RE = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")
# Composition verbs mark a primitive a skill depends on, as opposed to a
# handoff to a neighbouring skill. Only composed primitives go into `requires`.
COMPOSE_RE = re.compile(
    r"\b(use|uses|using|consult|consults|apply|applies|follow|follows|"
    r"belongs to|owned by|owns|composes)\b",
    re.IGNORECASE,
)


def load_invocations(root: Path) -> dict[str, str]:
    """Map each skill name to its invocation class (default model)."""
    invocations = {}
    for skill_dir in sorted(p for p in (root / "skills").iterdir() if p.is_dir()):
        frontmatter, _ = validate_skill.parse_frontmatter(
            (skill_dir / "SKILL.md").read_text(encoding="utf-8"))
        extra = frontmatter.get("metadata")
        extra = extra if isinstance(extra, dict) else {}
        invocations[skill_dir.name] = extra.get("invocation", "model")
    return invocations


def handoff_requires(skill_dir: Path, invocations: dict[str, str]) -> list[str]:
    """Model-invoked primitives this skill composes (Handoffs composition lines)."""
    refs = []
    in_handoffs = False
    for line in (skill_dir / "SKILL.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_handoffs = line[3:].strip().lower() == "handoffs"
        if not in_handoffs or not COMPOSE_RE.search(line):
            continue
        for token in KEBAB_RE.findall(line):
            if token != skill_dir.name and invocations.get(token) == "model" and token not in refs:
                refs.append(token)
    return sorted(refs)


def compatibility_list(value: object) -> list[str]:
    if isinstance(value, str):
        parts = [part.strip() for part in value.split(",")]
        if parts and all(TOKEN_RE.match(part) for part in parts):
            return parts
    return list(DEFAULT_COMPATIBILITY)


def build_manifest(skill_dir: Path, catalog_block: dict,
                   invocations: dict[str, str]) -> dict:
    frontmatter, _ = validate_skill.parse_frontmatter(
        (skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    extra = frontmatter.get("metadata")
    extra = extra if isinstance(extra, dict) else {}
    invocation = extra.get("invocation", "model")
    if invocation not in ("model", "user"):
        raise ValueError(f"{skill_dir.name}: metadata.invocation must be model or user")
    manifest = {
        "name": frontmatter.get("name", skill_dir.name),
        "title": extra.get("title", ""),
        "version": extra.get("version", ""),
        "summary": extra.get("summary", ""),
        "invocation": invocation,
        "compatibility": compatibility_list(frontmatter.get("compatibility")),
    }
    tools = frontmatter.get("allowed-tools")
    if isinstance(tools, str) and tools.split():
        manifest["allowed_tools"] = tools.split()
    manifest["requires"] = handoff_requires(skill_dir, invocations)
    for field in CATALOG_FIELDS:
        manifest[field] = catalog_block[field]
    return manifest


def manifest_text(manifest: dict) -> str:
    return json.dumps(manifest, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--check", action="store_true",
                        help="fail on drift instead of writing manifests")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    if not (root / "skills").is_dir():
        print(f"error: no skills/ directory under {root}", file=sys.stderr)
        return 2
    if not args.catalog.is_file():
        print(f"error: catalog not found: {args.catalog}", file=sys.stderr)
        return 2
    catalog = json.loads(args.catalog.read_text(encoding="utf-8")).get("skills", {})
    invocations = load_invocations(root)

    skill_dirs = sorted(p for p in (root / "skills").iterdir() if p.is_dir())
    names = {p.name for p in skill_dirs}
    missing = names - set(catalog)
    extra = set(catalog) - names
    if missing or extra:
        print(f"error: catalog mismatch; missing={sorted(missing)} extra={sorted(extra)}",
              file=sys.stderr)
        return 2

    results = []
    for skill_dir in skill_dirs:
        try:
            manifest = build_manifest(skill_dir, catalog[skill_dir.name], invocations)
        except (OSError, ValueError) as exc:
            results.append({"skill": skill_dir.name, "status": "error", "detail": str(exc)})
            continue
        manifest_path = skill_dir / "metadata.json"
        desired = manifest_text(manifest)
        current = manifest_path.read_text(encoding="utf-8") if manifest_path.is_file() else ""
        if current.replace("\r\n", "\n") == desired:
            results.append({"skill": skill_dir.name, "status": "in-sync"})
        elif args.check:
            results.append({"skill": skill_dir.name, "status": "drift"})
        else:
            manifest_path.write_text(desired, encoding="utf-8")
            results.append({"skill": skill_dir.name, "status": "written"})

    drifted = [r for r in results if r["status"] in ("drift", "error")]
    if args.json:
        print(json.dumps({"valid": not drifted, "check": args.check,
                          "results": results}, indent=2))
    else:
        for r in results:
            print(f"{r['status']:>8}  {r['skill']}" + (
                f": {r['detail']}" if r.get("detail") else ""))
        print(f"{len(results)} manifest(s); {len(drifted)} need attention")
    return 1 if drifted else 0


if __name__ == "__main__":
    sys.exit(main())
