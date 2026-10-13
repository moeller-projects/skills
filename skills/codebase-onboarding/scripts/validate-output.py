#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Codebase Onboarding output against the repo-map, entrypoint, convention, hotspot, and artifact contract.
Inputs: Contract text on stdin. Use --help for the stdin format and exit status.
Outputs: "OK" on stdout when valid; diagnostics on stderr and exit status 1 when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys


SECTIONS = ("repo_map", "entrypoints", "conventions", "hotspots", "agent_artifacts")


def _sections(text: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    matches = list(re.finditer(r"^(repo_map|entrypoints|conventions|hotspots|agent_artifacts):[ \t]*\r?$", text, re.MULTILINE))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        found[match.group(1)] = [line.strip()[2:].strip() for line in text[match.end():end].splitlines() if line.strip().startswith("- ")]
    return found


def main() -> None:
    if "--help" in sys.argv[1:]:
        print("Usage: python scripts/validate-output.py < onboarding-artifact.txt")
        print("Reads the canonical sectioned-text onboarding contract from stdin.")
        print("Each section must contain substantive entries or an explicit 'none' marker.")
        return

    sections = _sections(sys.stdin.buffer.read().decode("utf-8"))
    errors: list[str] = [f"missing section: {name}" for name in SECTIONS if name not in sections]
    for name in SECTIONS:
        entries = sections.get(name, [])
        if not entries:
            errors.append(f"section must contain an entry or explicit none: {name}")
            continue
        if len(entries) == 1 and entries[0].lower() in {"none", "n/a", "not found"}:
            continue
        for entry in entries:
            lowered = entry.lower()
            if lowered in {"none", "n/a", "not found"}:
                errors.append(f"{name} mixes an absence marker with substantive entries")
                continue
            if re.search(r"<[^>]+>", entry):
                errors.append(f"{name} contains an unresolved placeholder")
                continue
            if name == "repo_map" and " — " not in entry:
                errors.append("repo_map entries must include area and one-line description separated by ' — '")
            elif name == "entrypoints" and " — " not in entry:
                errors.append("entrypoints entries must include path and why it matters separated by ' — '")
            elif name == "conventions" and not entry.strip():
                errors.append("conventions entries must contain substantive observed content")
            elif name == "hotspots" and " — " not in entry:
                errors.append("hotspots entries must include area and concrete reason separated by ' — '")
            elif name == "agent_artifacts" and " — " not in entry:
                errors.append("agent_artifacts entries must include artifact and how to use it separated by ' — '")
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
