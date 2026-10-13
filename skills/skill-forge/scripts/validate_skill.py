#!/usr/bin/env python3
"""Validate an Agent Skill against the agentskills spec plus production-grade lint.

Checks frontmatter constraints and repository manifest synchronization, then
adds production lint for resource discovery and layout. This is static
validation, not proof of activation accuracy, script safety, or output quality.

Usage:
    python3 scripts/validate_skill.py <skill-dir> [--json] [--strict]

Exit codes:
    0  valid (warnings may still be present)
    1  spec validation errors found
    2  usage error / skill directory not found

Options:
    --json    Emit a JSON report on stdout instead of human-readable text.
    --strict  Treat warnings as errors (exit 1 if any warning exists).
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
SKILL_MD_SOFT_LINE_LIMIT = 500  # progressive-disclosure guidance

ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}

RESOURCE_DIRS = ("references", "reference", "scripts", "assets", "rules", "tests", "evals")

# Files that add clutter without helping the agent at runtime.
FORBIDDEN_FILES = {
    "README.md", "readme.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md", "CONTRIBUTING.md",
}

WHEN_PATTERN = re.compile(
    r"\buse\b.{0,80}\b(when|if)\b|\btrigger", re.IGNORECASE | re.DOTALL
)


# ---------------------------------------------------------------- frontmatter

def parse_frontmatter(content):
    """Parse YAML frontmatter. Returns (metadata dict, body str).

    Uses PyYAML when available. The fallback intentionally accepts only the
    string/mapping subset this validator needs and rejects syntax it cannot
    represent safely.
    """
    if not content.startswith("---"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md frontmatter not properly closed with ---")
    raw, body = parts[1], parts[2].strip()
    try:
        import yaml  # type: ignore
        metadata = yaml.safe_load(raw)
    except ImportError:
        metadata = _minimal_yaml(raw)
    except Exception as e:
        raise ValueError(f"Invalid YAML in frontmatter: {e}")
    if not isinstance(metadata, dict):
        raise ValueError("SKILL.md frontmatter must be a YAML mapping")
    return metadata, body


def _minimal_yaml(raw):
    """Parse the supported string/mapping subset, rejecting other YAML types."""
    data, lines, i = {}, raw.splitlines(), 0

    def scalar(value, line_no):
        value = value.strip()
        if not value:
            raise ValueError(f"Unsupported empty YAML value on line {line_no}")
        if value.startswith(("[", "{", "- ")) or value in {
            "true", "false", "null", "~"
        } or re.fullmatch(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", value):
            raise ValueError(
                f"Unsupported YAML type/syntax on line {line_no}; "
                "install PyYAML for non-string frontmatter values"
            )
        if value[0] in "\"'":
            quote = value[0]
            if len(value) < 2 or value[-1] != quote:
                raise ValueError(f"Unsupported quoted YAML value on line {line_no}")
            if quote == '"':
                try:
                    return json.loads(value)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Unsupported escaped quoted YAML value on line {line_no}; "
                        "install PyYAML for YAML escape decoding"
                    ) from exc
            return value[1:-1].replace("''", "'")
        if value.startswith(("[", "{", "- ")) or value in {
            "true", "false", "null", "~"
        } or re.fullmatch(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", value):
            raise ValueError(
                f"Unsupported YAML type/syntax on line {line_no}; "
                "install PyYAML for non-string frontmatter values"
            )
        return value

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line[0].isspace():
            raise ValueError(f"Unexpected indentation on line {i + 1}")
        m = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not m:
            raise ValueError(
                f"Unsupported YAML syntax on line {i + 1}; "
                "install PyYAML for this frontmatter shape"
            )
        key, val = m.group(1), m.group(2) or ""
        if val in (">", "|", ">-", "|-"):
            block, i = [], i + 1
            while i < len(lines) and (
                lines[i].startswith((" ", "\t")) or not lines[i].strip()
            ):
                block.append(lines[i].strip())
                i += 1
            data[key] = (" " if val.startswith(">") else "\n").join(
                b for b in block if b
            ).strip()
            continue
        if val == "":
            nested, i = {}, i + 1
            while i < len(lines) and lines[i].startswith((" ", "\t")):
                nm = re.match(r"^\s+([A-Za-z0-9_-]+):(?:\s*(.*))?$", lines[i])
                if not nm or not (nm.group(2) or "").strip():
                    raise ValueError(
                        f"Unsupported nested YAML syntax on line {i + 1}; "
                        "only scalar metadata values are supported"
                    )
                nested[nm.group(1)] = scalar(nm.group(2), i + 1)
                i += 1
            if not nested:
                raise ValueError(f"Unsupported empty mapping on line {i}")
            data[key] = nested
            continue
        data[key] = scalar(val, i + 1)
        i += 1
    return data




# ------------------------------------------------------------------ spec rules

def check_name(name, dir_name):
    errors = []
    if not isinstance(name, str) or not name.strip():
        return ["Field 'name' must be a non-empty string"]
    name = unicodedata.normalize("NFKC", name)
    if len(name) > MAX_SKILL_NAME_LENGTH:
        errors.append(f"Skill name exceeds {MAX_SKILL_NAME_LENGTH} chars ({len(name)})")
    if name != name.lower():
        errors.append(f"Skill name '{name}' must be lowercase")
    if name.startswith("-") or name.endswith("-"):
        errors.append("Skill name cannot start or end with a hyphen")
    if "--" in name:
        errors.append("Skill name cannot contain consecutive hyphens")
    if not all(c.isalnum() or c == "-" for c in name):
        errors.append(
            f"Skill name '{name}' contains invalid characters; "
            "only letters, digits, and hyphens are allowed"
        )
    if dir_name is not None and unicodedata.normalize("NFKC", dir_name) != name:
        errors.append(f"Directory name '{dir_name}' must match skill name '{name}'")
    return errors


def check_description(desc, user_invoked=False):
    errors, warnings = [], []
    if not isinstance(desc, str) or not desc.strip():
        return ["Field 'description' must be a non-empty string"], warnings
    if len(desc) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"Description exceeds {MAX_DESCRIPTION_LENGTH} chars ({len(desc)})"
        )
    if len(desc.strip()) < 50:
        warnings.append(
            "Description is very short (<50 chars); it must say what the skill "
            "does AND when to use it"
        )
    if not user_invoked and not WHEN_PATTERN.search(desc):
        warnings.append(
            "Description lacks a 'Use when...' trigger clause; agents decide "
            "activation from the description alone"
        )
    return errors, warnings


def check_metadata_fields(metadata):
    """Validate optional frontmatter types without relying on a YAML parser."""
    errors = []
    extra = metadata.get("metadata")
    if "metadata" in metadata:
        if not isinstance(extra, dict) or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in extra.items()
        ):
            errors.append("Field 'metadata' must be a mapping of strings to strings")
        elif extra.get("invocation", "model") not in {"model", "user"}:
            errors.append("metadata.invocation must be model or user")
    if "allowed-tools" in metadata:
        tools = metadata["allowed-tools"]
        if not isinstance(tools, str) or not tools.strip():
            errors.append("Field 'allowed-tools' must be a non-empty space-separated string")
    if "license" in metadata and not isinstance(metadata["license"], str):
        errors.append("Field 'license' must be a string")
    return errors


def check_manifest(skill_dir, metadata):
    """Compare repository metadata only when a manifest is bundled."""
    manifest_path = skill_dir / "metadata.json"
    if not manifest_path.exists():
        return []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Cannot read metadata.json: {exc}"]
    if not isinstance(manifest, dict):
        return ["metadata.json must be a JSON object"]
    errors = []
    extra = metadata.get("metadata")
    extra = extra if isinstance(extra, dict) else {}
    for field, expected in (
        ("name", metadata.get("name")),
        ("title", extra.get("title")),
        ("version", extra.get("version")),
        ("summary", extra.get("summary")),
        ("invocation", extra.get("invocation", "model")),
    ):
        actual = manifest.get(field, "model" if field == "invocation" else None)
        if field != "invocation" and (
            not isinstance(expected, str) or not expected.strip()
            or not isinstance(actual, str) or not actual.strip()
        ):
            errors.append(f"{field} must be a non-empty string in frontmatter and metadata.json")
        elif actual != expected:
            errors.append(f"metadata.json {field} does not match SKILL.md")
    tools = metadata.get("allowed-tools", "")
    expected_tools = tools.split() if isinstance(tools, str) else []
    if manifest.get("allowed_tools", []) != expected_tools:
        errors.append("metadata.json allowed_tools does not match SKILL.md allowed-tools")
    activation = manifest.get("activation")
    if activation is not None:
        if not isinstance(activation, dict):
            errors.append("metadata.json activation must be an object")
        else:
            for field in ("use_when", "avoid_when"):
                values = activation.get(field)
                if not isinstance(values, list) or not values or not all(
                    isinstance(value, str) and value.strip() for value in values
                ):
                    errors.append(f"metadata.json activation.{field} must be a non-empty string array")
    return errors


# ------------------------------------------------------------------- linting

def lint_structure(skill_dir, metadata, body):
    errors = []
    warnings = []
    lines = body.splitlines()
    if len(lines) > SKILL_MD_SOFT_LINE_LIMIT:
        warnings.append(
            f"SKILL.md body is {len(lines)} lines (>{SKILL_MD_SOFT_LINE_LIMIT}); "
            "move detailed material into references/ files"
        )

    extra = set(metadata) - ALLOWED_FIELDS
    if extra:
        errors.append(
            "Unexpected frontmatter fields: "
            + ", ".join(sorted(extra))
            + f" (allowed: {', '.join(sorted(ALLOWED_FIELDS))})"
        )

    SKIP_DIRS = {"__pycache__", ".git", "node_modules"}

    def skipped(path):
        return bool(SKIP_DIRS.intersection(path.relative_to(skill_dir).parts))

    for p in sorted(skill_dir.rglob("*")):
        if p.is_file() and not skipped(p) and p.name in FORBIDDEN_FILES:
            warnings.append(
                f"Remove '{p.relative_to(skill_dir)}'; skills must not contain "
                "README/CHANGELOG-style docs"
            )

    # Relative links to bundled files must exist; bundled references must be
    # discoverable (linked from SKILL.md) and at most one level deep.
    skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    for sub in RESOURCE_DIRS:
        d = skill_dir / sub
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*")):
            if not f.is_file() or skipped(f) or f.suffix.lower() == ".skill":
                continue
            rel = f.relative_to(skill_dir).as_posix()
            if rel not in skill_md_text:
                warnings.append(
                    f"'{rel}' is not referenced from SKILL.md; the agent may "
                    "never discover it"
                )
            if sub.startswith("reference") and len(f.relative_to(d).parts) > 1:
                warnings.append(
                    f"'{rel}' is nested deeper than one level under {sub}/; "
                    "keep reference files one level deep"
                )

    resource_prefixes = "|".join(re.escape(sub) for sub in RESOURCE_DIRS)
    for m in re.finditer(rf"\([ \t]*((?:{resource_prefixes})/[^()]+)\)", skill_md_text):
        target = m.group(1).split()[0].split("#")[0].strip("`").rstrip("/")
        if target and not (skill_dir / target).exists():
            warnings.append(f"SKILL.md links to missing file: {target}")

    todo_hits = len(re.findall(r"\[TODO:|\bTODO:", skill_md_text))
    if todo_hits:
        warnings.append(
            f"SKILL.md still contains {todo_hits} TODO placeholder(s); "
            "replace them before shipping"
        )

    abs_paths = re.findall(r"(?<![\w./-])/(?:Users|home|mnt|tmp)/[\w./-]+", skill_md_text)
    if abs_paths:
        warnings.append(
            "SKILL.md contains absolute paths ("
            + ", ".join(sorted(set(abs_paths))[:3])
            + "); use paths relative to the skill root"
        )
    return errors, warnings


# ---------------------------------------------------------------------- main

def validate_skill(skill_dir):
    """Returns dict with 'errors' and 'warnings' lists."""
    skill_dir = Path(skill_dir)
    if not skill_dir.is_dir():
        return {"errors": [f"Skill directory not found: {skill_dir}"], "warnings": []}
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {"errors": ["Missing required file: SKILL.md"], "warnings": []}
    try:
        metadata, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as e:
        return {"errors": [str(e)], "warnings": []}

    errors, warnings = [], []
    for field in ("name", "description"):
        if field not in metadata:
            errors.append(f"Missing required field in frontmatter: {field}")
    if "name" in metadata:
        errors += check_name(metadata["name"], skill_dir.name)
    if "description" in metadata:
        extra = metadata.get("metadata")
        user_invoked = (
            isinstance(extra, dict) and extra.get("invocation") == "user"
        )
        e, w = check_description(metadata["description"], user_invoked)
        errors += e
        warnings += w
    errors += check_metadata_fields(metadata)
    errors += check_manifest(skill_dir, metadata)
    if "compatibility" in metadata:
        c = metadata["compatibility"]
        if not isinstance(c, str) or not c.strip():
            errors.append("Field 'compatibility' must be a non-empty string")
        elif len(c) > MAX_COMPATIBILITY_LENGTH:
            errors.append(
                f"Compatibility exceeds {MAX_COMPATIBILITY_LENGTH} chars ({len(c)})"
            )
    structure_errors, structure_warnings = lint_structure(
        skill_dir, metadata, body
    )
    errors += structure_errors
    warnings += structure_warnings
    return {"errors": errors, "warnings": warnings}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if "--help" in flags or "-h" in sys.argv:
        print("Usage: python scripts/validate_skill.py <skill-dir> [--json] [--strict]")
        sys.exit(0)
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    result = validate_skill(args[0])
    if "--json" in flags:
        result["valid"] = not result["errors"]
        print(json.dumps(result, indent=2))
    else:
        for e in result["errors"]:
            print(f"ERROR   {e}", file=sys.stderr)
        for w in result["warnings"]:
            print(f"WARNING {w}", file=sys.stderr)
        if not result["errors"] and not result["warnings"]:
            print("OK: frontmatter, bundled manifest, and checked resource layout are valid")
        elif not result["errors"]:
            print(f"VALID with {len(result['warnings'])} warning(s)")
        else:
            print(f"INVALID: {len(result['errors'])} error(s)", file=sys.stderr)
    sys.exit(1 if result["errors"] or ("--strict" in flags and result["warnings"]) else 0)


if __name__ == "__main__":
    main()
