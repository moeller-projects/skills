#!/usr/bin/env python3
"""Repository-wide lint for the Agent Skills catalog.

Checks run per skill and across the tree:

- frontmatter fields, manifest sync, and resource discovery (delegated to
  ``validate_skill.py`` so the rules live in one place)
- required catalog keys: ``license``, ``compatibility``, ``metadata.title``,
  ``version``, ``summary``, and the manifest's ``invocation``, ``type``,
  ``risk_level``
- every bundled file is linked from ``SKILL.md`` with a use condition
- resource list items live under a resource section heading
- backticked skill references resolve to a real skill
- duplicate and near-duplicate prose lines within a file
- a blank line before every ``##`` heading and opening code fence

Known defects are recorded in a baseline file (``repo_lint_baseline.json`` at
the repository root by default) so the linter can run clean while they are
fixed one by one. Findings
that match the baseline are reported as ``known`` and do not fail the run;
anything new fails. Regenerate the baseline only with ``--update-baseline``.

This is static validation. A clean report does not prove behavioral
correctness or activation accuracy.

Usage:
    python skills/skill-forge/scripts/repo_lint.py [--root PATH] [--json]
        [--baseline PATH] [--no-baseline] [--update-baseline] [--only CHECK]

Exit codes:
    0  no new findings (known findings may remain)
    1  new findings found
    2  usage error / root not found
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR.parents[2]
DEFAULT_BASELINE = DEFAULT_ROOT / "repo_lint_baseline.json"

sys.path.insert(0, str(SCRIPT_DIR))
import validate_skill  # noqa: E402  (same directory)

RESOURCE_DIRS = ("references", "reference", "scripts", "assets", "rules", "tests", "evals")
SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".baseline"}

# A resource bullet is placed correctly when the nearest heading above it is
# plausibly about resources rather than an unrelated content section.
RESOURCE_SECTION_TOKENS = (
    "asset", "reference", "rule", "script", "resource", "detail", "example",
    "schema", "input", "test", "workflow", "handling",
)
CONDITION_RE = re.compile(
    r"\b(when|before|if|for|after|during|only|read|run|use|see|consult|"
    r"check|apply|follow|audit|invoke|execute|validate|load|call)\b",
    re.IGNORECASE,
)
KEBAB_RE = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")
RESOURCE_BULLET_RE = re.compile(
    r"^\s*[-*]\s+`((?:%s)/[^`*]+)`" % "|".join(re.escape(d) for d in RESOURCE_DIRS)
)
SKILL_REF_PHRASE_RE = re.compile(
    r"hand(?:s|ed)?\s+off\s+to|accepts?\s+work\s+from|consults?\b|"
    r"delegate[sd]?\s+to|route[sd]?\s+to|hand\s+to|composes?\b",
    re.IGNORECASE,
)
# Bidirectional handoffs are intentional in this catalog (each direction names
# a different transition). New mutual references outside this set warn.
INTENTIONAL_CYCLES = {
    frozenset({"azure-devops", "spec-writing"}),
    frozenset({"branch-integration", "git-workflow"}),
    frozenset({"code-review", "codebase-onboarding"}),
    frozenset({"code-review", "test-strategy"}),
    frozenset({"codebase-design", "domain-modeling"}),
    frozenset({"codebase-design", "test-driven-development"}),
    frozenset({"codebase-onboarding", "technical-writing"}),
    frozenset({"codebase-onboarding", "test-strategy"}),
    frozenset({"debugging", "test-driven-development"}),
    frozenset({"gh-stack", "git-workflow"}),
    frozenset({"git-workflow", "git-worktrees"}),
    frozenset({"git-worktrees", "plan-execution"}),
    frozenset({"pr-review", "review-response"}),
    frozenset({"spec-writing", "task-planning"}),
}
INVOKE_RE = re.compile(
    r"\b(invoke[sd]?|start[s]?|execute[sd]?|call[s]?|automatically|trigger[s]?)\b",
    re.IGNORECASE,
)

TOC_LINE_RE = re.compile(r"^\s*[-*]\s+\[")
KEY_VALUE_LINE_RE = re.compile(r"^\s*[-*]?\s*[A-Za-z_][A-Za-z0-9_]*\s*:")
LINK_ONLY_LINE_RE = re.compile(r"^\s*\[[^\]]+\]\([^)]+\)\.?$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def posix(path: Path) -> str:
    return path.as_posix()


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def blank_frontmatter(text: str) -> str:
    """Replace the YAML frontmatter with blank lines, preserving line numbers."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                for j in range(i + 1):
                    lines[j] = ""
                break
    return "\n".join(lines)


def strip_code_fences(text: str) -> str:
    """Drop fenced code blocks so code samples are not linted as prose."""
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def make_key(check: str, file: str, ident: str) -> str:
    return f"{check}|{file}|{ident}"


class Report:
    def __init__(self) -> None:
        self.findings: list[dict] = []

    def add(self, check: str, skill: str, file: str, message: str,
            line: int | None = None, ident: str | None = None,
            severity: str = "error") -> None:
        key = make_key(check, file, ident if ident is not None else str(line))
        self.findings.append({
            "check": check,
            "skill": skill,
            "file": file,
            "line": line,
            "message": message,
            "key": key,
            "severity": severity,
        })


def load_frontmatter(skill_md: Path):
    try:
        return validate_skill.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return None, None


# ------------------------------------------------------------------- checks

def check_validate_skill(report: Report, root: Path, skill_dir: Path) -> None:
    """Delegate spec + manifest + discovery checks to validate_skill.py."""
    result = validate_skill.validate_skill(skill_dir)
    rel = posix(skill_dir.relative_to(root) / "SKILL.md")
    for message in result["errors"]:
        report.add("validate-skill-error", skill_dir.name, rel, message,
                   ident=norm(message))
    for message in result["warnings"]:
        report.add("validate-skill-warning", skill_dir.name, rel, message,
                   ident=norm(message))


def check_required_keys(report: Report, root: Path, skill_dir: Path,
                        frontmatter: dict, manifest: dict | None) -> None:
    rel = posix(skill_dir.relative_to(root) / "SKILL.md")
    for field in ("license", "compatibility"):
        value = frontmatter.get(field)
        if not isinstance(value, str) or not value.strip():
            report.add("required-key", skill_dir.name, rel,
                       f"frontmatter is missing required '{field}'", ident=field)
    extra = frontmatter.get("metadata")
    extra = extra if isinstance(extra, dict) else {}
    for field in ("title", "version", "summary"):
        value = extra.get(field)
        if not isinstance(value, str) or not value.strip():
            report.add("required-key", skill_dir.name, rel,
                       f"frontmatter metadata is missing required '{field}'",
                       ident=f"metadata.{field}")
    if manifest is None:
        report.add("required-key", skill_dir.name,
                   posix(skill_dir.relative_to(root) / "metadata.json"),
                   "metadata.json is missing", ident="metadata.json")
        return
    manifest_rel = posix(skill_dir.relative_to(root) / "metadata.json")
    for field in ("invocation", "type", "risk_level"):
        value = manifest.get(field)
        if not isinstance(value, str) or not value.strip():
            report.add("required-key", skill_dir.name, manifest_rel,
                       f"metadata.json is missing required '{field}'", ident=field)


def iter_bundled_files(skill_dir: Path):
    for sub in RESOURCE_DIRS:
        d = skill_dir / sub
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*")):
            if not f.is_file() or f.suffix.lower() == ".skill":
                continue
            if SKIP_DIRS.intersection(f.relative_to(skill_dir).parts):
                continue
            yield f


def block_text(lines: list[str], index: int) -> str:
    """Join the contiguous non-blank block containing ``index`` (0-based)."""
    start = index
    while start > 0 and lines[start - 1].strip():
        start -= 1
    end = index
    while end + 1 < len(lines) and lines[end + 1].strip():
        end += 1
    return " ".join(lines[start:end + 1])


def check_resource_links(report: Report, root: Path, skill_dir: Path,
                         body: str) -> None:
    skill_md = posix(skill_dir.relative_to(root) / "SKILL.md")
    lines = body.splitlines()
    for f in iter_bundled_files(skill_dir):
        rel = f.relative_to(skill_dir).as_posix()
        hits = [i for i, line in enumerate(lines) if rel in line]
        if not hits:
            # validate_skill already warns about this; keep one finding only.
            continue
        if not any(CONDITION_RE.search(block_text(lines, i)) for i in hits):
            report.add("missing-use-condition", skill_dir.name, skill_md,
                       f"'{rel}' is linked without a use condition",
                       line=hits[0] + 1, ident=rel)


def check_resource_sections(report: Report, root: Path, skill_dir: Path,
                            body: str) -> None:
    skill_md = posix(skill_dir.relative_to(root) / "SKILL.md")
    heading = None
    for i, line in enumerate(body.splitlines(), 1):
        if line.startswith("## "):
            heading = line[3:].strip()
        match = RESOURCE_BULLET_RE.match(line)
        if not match:
            continue
        target = match.group(1)
        heading_norm = (heading or "").lower()
        if heading and any(t in heading_norm for t in RESOURCE_SECTION_TOKENS):
            continue
        report.add("resource-section", skill_dir.name, skill_md,
                   f"'{target}' sits under {heading!r}, not a resource section",
                   line=i, ident=target)


def check_dangling_skills(report: Report, root: Path, skills: set[str]) -> None:
    for path in sorted(root.glob("skills/*/*.md")) + sorted(root.glob("skills/*/*/*.md")):
        rel = posix(path.relative_to(root))
        lines = path.read_text(encoding="utf-8").splitlines()
        in_handoffs = False
        for i, line in enumerate(lines, 1):
            if line.startswith("## "):
                in_handoffs = line[3:].strip().lower() == "handoffs"
            if not in_handoffs and not SKILL_REF_PHRASE_RE.search(line):
                continue
            for match in KEBAB_RE.finditer(line):
                token = match.group(1)
                if token not in skills:
                    report.add("dangling-skill", path.parent.name, rel,
                               f"skill reference '{token}' does not match a skill directory",
                               line=i, ident=token)


def duplicate_candidates(text: str):
    """Prose lines worth comparing, excluding structure and link-only lines."""
    for i, line in enumerate(strip_code_fences(text).splitlines(), 1):
        stripped = line.strip()
        if len(stripped) < 40 or stripped.startswith("|"):
            continue
        if TOC_LINE_RE.match(line) or KEY_VALUE_LINE_RE.match(line):
            continue
        if LINK_ONLY_LINE_RE.match(line):
            continue
        yield i, stripped


def check_duplicates(report: Report, root: Path, skill_dir: Path) -> None:
    """Duplicate and near-duplicate prose lines in SKILL.md, rules, references."""
    skill_md = skill_dir / "SKILL.md"
    targets = [(skill_md, blank_frontmatter(skill_md.read_text(encoding="utf-8")))]
    for sub in ("rules", "references"):
        d = skill_dir / sub
        if d.is_dir():
            targets += [(p, p.read_text(encoding="utf-8"))
                        for p in sorted(d.rglob("*.md"))]
    for path, text in targets:
        if not path.is_file():
            continue
        rel = posix(path.relative_to(root))
        candidates = list(duplicate_candidates(text))

        seen: dict[str, int] = {}
        for i, line in candidates:
            n = norm(line)
            if n in seen:
                report.add("duplicate-line", skill_dir.name, rel,
                           f"line repeats line {seen[n]}: {n[:70]}",
                           line=i, ident=n)
            else:
                seen[n] = i

        for a in range(len(candidates)):
            for b in range(a + 1, min(a + 9, len(candidates))):
                ia, la = candidates[a]
                ib, lb = candidates[b]
                na, nb = norm(la), norm(lb)
                if na == nb or len(na) < 50 or len(nb) < 50:
                    continue
                prefix = 0
                for ca, cb in zip(na, nb):
                    if ca != cb:
                        break
                    prefix += 1
                ratio = difflib.SequenceMatcher(None, na, nb).ratio()
                if prefix >= 40 or (prefix >= 15 and ratio >= 0.90):
                    ident = f"{na[:60]}~{nb[:60]}"
                    report.add("near-duplicate", skill_dir.name, rel,
                               f"lines {ia} and {ib} are near-duplicates: {na[:60]}",
                               line=ib, ident=ident)


def handoff_refs(skill_dir: Path, skills: set[str], meta: dict) -> list[str]:
    """Model-invoked skills in this skill's Handoffs section, excluding itself.

    User-invoked skills are omitted: they never fire automatically, so a
    reference to one cannot form an automatic handoff loop.
    """
    refs, in_handoffs = [], False
    for line in (skill_dir / "SKILL.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_handoffs = line[3:].strip().lower() == "handoffs"
        if not in_handoffs:
            continue
        for token in KEBAB_RE.findall(line):
            if (token in skills and token != skill_dir.name
                    and meta.get(token, {}).get("invocation", "model") == "model"
                    and token not in refs):
                refs.append(token)
    return refs


def check_graph(report: Report, root: Path, skills: set[str], meta: dict) -> None:
    """Handoff-graph checks: reachability, user-invoked references, cycles."""
    router = root / "skills" / "ask-lukas" / "SKILL.md"
    router_text = router.read_text(encoding="utf-8") if router.is_file() else ""
    router_rel = posix(router.relative_to(root))
    for name in sorted(skills):
        if name == "ask-lukas" or meta.get(name, {}).get("invocation", "model") != "model":
            continue
        if f"`{name}`" not in router_text:
            report.add("graph-unreachable", name, router_rel,
                       f"model-invoked skill '{name}' is not reachable from the ask-lukas router",
                       ident=name)

    for skill_dir in sorted(p for p in (root / "skills").iterdir() if p.is_dir()):
        rel = posix((skill_dir / "SKILL.md").relative_to(root))
        in_handoffs = False
        for i, line in enumerate((skill_dir / "SKILL.md").read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("## "):
                in_handoffs = line[3:].strip().lower() == "handoffs"
            if not in_handoffs:
                continue
            for token in KEBAB_RE.findall(line):
                if meta.get(token, {}).get("invocation") == "user" and INVOKE_RE.search(line):
                    report.add("graph-user-invoked-handoff", skill_dir.name, rel,
                               f"Handoffs invokes user-invoked '{token}'; recommend it instead",
                               line=i, ident=token, severity="warning")

    handoffs = {d.name: handoff_refs(d, skills, meta)
                for d in sorted(p for p in (root / "skills").iterdir() if p.is_dir())}
    seen_pairs = set()
    for a in sorted(skills):
        for b in handoffs.get(a, []):
            pair = frozenset({a, b})
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            if pair in INTENTIONAL_CYCLES:
                continue
            if a in handoffs.get(b, []):
                report.add("graph-cycle", a,
                           posix((root / "skills" / a / "SKILL.md").relative_to(root)),
                           f"mutual handoff between '{a}' and '{b}'",
                           ident="~".join(sorted(pair)), severity="warning")


def check_spacing(report: Report, root: Path, skill_dir: Path) -> None:
    targets = [skill_dir / "SKILL.md"]
    for sub in ("rules", "references"):
        d = skill_dir / sub
        if d.is_dir():
            targets += sorted(d.rglob("*.md"))
    for path in targets:
        if not path.is_file():
            continue
        rel = posix(path.relative_to(root))
        lines = path.read_text(encoding="utf-8").splitlines()
        in_fence = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(("```", "~~~")):
                if not in_fence and i > 0 and lines[i - 1].strip() and path.name == "SKILL.md":
                    report.add("fence-spacing", skill_dir.name, rel,
                               "no blank line before opening code fence",
                               line=i + 1, ident=str(i + 1))
                in_fence = not in_fence
                continue
            if in_fence or i == 0:
                continue
            if line.startswith("## ") and lines[i - 1].strip():
                report.add("heading-spacing", skill_dir.name, rel,
                           f"no blank line before heading {line.strip()!r}",
                           line=i + 1, ident=norm(line))


# -------------------------------------------------------------------- driver

def lint(root: Path, only: set[str] | None) -> Report:
    report = Report()
    skills = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    meta: dict = {}

    def wanted(check: str) -> bool:
        return only is None or check in only

    for skill_dir in sorted(p for p in (root / "skills").iterdir() if p.is_dir()):
        if wanted("validate-skill-error") or wanted("validate-skill-warning"):
            check_validate_skill(report, root, skill_dir)
        frontmatter, body = load_frontmatter(skill_dir / "SKILL.md")
        manifest = None
        manifest_path = skill_dir / "metadata.json"
        if manifest_path.is_file():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                manifest = None
        meta[skill_dir.name] = {
            "invocation": (manifest or {}).get("invocation", "model"),
            "requires": (manifest or {}).get("requires", []),
        }
        if frontmatter is None or body is None:
            continue
        if wanted("required-key"):
            check_required_keys(report, root, skill_dir, frontmatter, manifest)
        raw = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        if wanted("missing-use-condition"):
            check_resource_links(report, root, skill_dir, raw)
        if wanted("resource-section"):
            check_resource_sections(report, root, skill_dir, raw)
        if wanted("duplicate-line") or wanted("near-duplicate"):
            check_duplicates(report, root, skill_dir)
        if wanted("heading-spacing") or wanted("fence-spacing"):
            check_spacing(report, root, skill_dir)

    if wanted("dangling-skill"):
        check_dangling_skills(report, root, skills)
    if wanted("graph-unreachable") or wanted("graph-user-invoked-handoff") or wanted("graph-cycle"):
        check_graph(report, root, skills, meta)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                        help="repository root containing skills/ (default: repo root)")
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE,
                        help="baseline file of known findings")
    parser.add_argument("--no-baseline", action="store_true",
                        help="ignore the baseline and fail on every finding")
    parser.add_argument("--update-baseline", action="store_true",
                        help="rewrite the baseline with the current findings")
    parser.add_argument("--only", action="append", default=None,
                        help="run only the named check (repeatable)")
    args = parser.parse_args()

    root = args.root.resolve()
    if not (root / "skills").is_dir():
        print(f"error: no skills/ directory under {root}", file=sys.stderr)
        return 2

    report = lint(root, set(args.only) if args.only else None)

    known: dict[str, str] = {}
    if not args.no_baseline and args.baseline.is_file():
        try:
            data = json.loads(args.baseline.read_text(encoding="utf-8"))
            known = data.get("findings", data) if isinstance(data, dict) else {}
            if not isinstance(known, dict):
                known = {}
        except (OSError, ValueError) as exc:
            print(f"warning: cannot read baseline: {exc}", file=sys.stderr)

    if args.update_baseline:
        errors = [f for f in report.findings if f.get("severity", "error") == "error"]
        payload = {
            "note": "Known repo-lint errors. Fix the defect, then rerun "
                    "with --update-baseline to shrink this list.",
            "findings": {f["key"]: f["message"] for f in errors},
        }
        args.baseline.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")
        print(f"wrote {len(report.findings)} finding(s) to {args.baseline}")
        return 0

    for finding in report.findings:
        finding["status"] = "known" if finding["key"] in known else "new"

    new = [f for f in report.findings if f["status"] == "new"]
    new_errors = [f for f in new if f.get("severity", "error") == "error"]
    known_count = len(report.findings) - len(new)

    if args.json:
        print(json.dumps({
            "valid": not new_errors,
            "root": posix(root),
            "baseline": None if args.no_baseline else posix(args.baseline),
            "summary": {"new": len(new_errors), "new_warnings": len(new) - len(new_errors),
                        "known": known_count, "total": len(report.findings)},
            "findings": report.findings,
        }, indent=2))
    else:
        for finding in report.findings:
            marker = "KNOWN" if finding["status"] == "known" else "NEW  "
            severity = finding.get("severity", "error")
            location = finding["file"]
            if finding["line"]:
                location += f":{finding['line']}"
            print(f"{marker} {severity.upper():7} [{finding['check']}] {location}: {finding['message']}")
        print(f"{len(new_errors)} new error(s), {len(new) - len(new_errors)} new warning(s), "
              f"{known_count} known finding(s)")
        if new_errors:
            print("repo lint failed: fix the new findings or update the baseline",
                  file=sys.stderr)
    return 1 if new_errors else 0


if __name__ == "__main__":
    sys.exit(main())
