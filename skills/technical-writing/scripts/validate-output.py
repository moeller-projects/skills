#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Technical Writing outputs for doc-plan, diff-oriented, and decision-record contracts.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stderr when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
Use --help to print usage without reading or validating input.
"""

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional, Tuple

SKILL_DIR = Path(__file__).resolve().parents[1]


class _HTMLContractParser(HTMLParser):
    """Small structural parser; unlike regex it accepts attributes and nesting."""

    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.attrs: dict[str, list[dict[str, str]]] = {}
        self.styles: list[str] = []
        self.text: list[str] = []
        self.body_text: list[str] = []
        self.external: list[str] = []
        self.in_style = False
        self.in_body = False

    def handle_starttag(self, tag: str, attrs: list[Tuple[str, Optional[str]]]) -> None:
        normalized = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        self.tags.append(tag)
        self.attrs.setdefault(tag, []).append(normalized)
        if tag == "style":
            self.styles.append("")
            self.in_style = True
        if tag == "body":
            self.in_body = True
        if tag in {"link", "script", "img", "iframe", "object", "embed"}:
            resource = normalized.get("src") or normalized.get("href") or normalized.get("data")
            if resource and not resource.startswith("data:"):
                self.external.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "body":
            self.in_body = False
        if tag.lower() == "style":
            self.in_style = False
    def handle_data(self, data: str) -> None:
        self.text.append(data)
        if self.in_body and not self.in_style:
            self.body_text.append(data)
        if self.in_style and self.styles:
            self.styles[-1] += data

def _validate_html_artifact(path: str) -> list[str]:
    errors: list[str] = []
    try:
        source = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        return [f"html artifact cannot be read: {exc}"]
    parser = _HTMLContractParser()
    try:
        parser.feed(source)
        parser.close()
    except Exception as exc:
        return [f"html artifact is not parseable: {exc}"]
    required = {"html", "head", "title", "style", "body"}
    missing = sorted(required - set(parser.tags))
    errors.extend(f"html artifact missing <{tag}> element" for tag in missing)
    html_attrs = parser.attrs.get("html", [{}])[0]
    if "lang" not in html_attrs:
        errors.append("html artifact <html> must declare lang")
    if not any("@" in style and "print" in style.lower() for style in parser.styles):
        errors.append("html artifact style must include print rules")
    if parser.external:
        errors.append("html artifact must be self-contained; external resource found")
    styles = "\n".join(parser.styles)
    if re.search(r"@import\b", styles, re.IGNORECASE):
        errors.append("html artifact style must not use external @import")
    for resource in re.findall(r"url\s*\(\s*[\"']?([^ )\"']+)", styles, re.IGNORECASE):
        if not resource.startswith("data:"):
            errors.append("html artifact style must not reference external resources")
            break
    if not any(part.strip() for part in parser.body_text):
        errors.append("html artifact body must contain substantive text")
    return errors


def _declared_artifact(text: str) -> Optional[str]:
    match = re.search(r"^- artifact:\s*\n^[ \t]+-[ \t]+(.+?)\s*$", text, re.MULTILINE)
    return match.group(1) if match else None


def validate(text: str, html_artifact: Optional[str] = None) -> list[str]:
    """Validate output metadata; validate HTML itself only when explicitly supplied."""
    errors: list[str] = []
    if re.search(r"^decision:", text, re.MULTILINE):
        for field in (r"^  context:", r"^  decision:", r"^  reasoning:", r"^  tradeoffs:", r"^  reuse_scope:"):
            if not re.search(field, text, re.MULTILINE):
                errors.append(f"missing decision field: {field[3:]}")
        if html_artifact:
            errors.append("--html-artifact requires an html output contract")
        return errors

    for section in (r"^doc:", r"^changes:", r"^gaps:"):
        if not re.search(section, text, re.MULTILINE):
            errors.append(f"missing section: {section[1:]}")
    for field, label in ((r"^- purpose:", "purpose"), (r"^- audience:", "audience"),
                         (r"^- structure:", "structure"), (r"^- format:", "format"),
                         (r"^- artifact:", "artifact")):
        if not re.search(field, text, re.MULTILINE):
            errors.append(f"missing doc {label}")
    if re.search(r"^- format:", text, re.MULTILINE):
        html_format = bool(re.search(r"^[ \t]+- type: html", text, re.MULTILINE))
        if not re.search(r"^[ \t]+- type: (markdown|html)", text, re.MULTILINE):
            errors.append("missing format type: markdown|html")
        if html_artifact and not html_format:
            errors.append("--html-artifact requires an html output contract")
        if html_format and html_artifact:
            declared = _declared_artifact(text)
            if not declared:
                errors.append("--html-artifact requires a declared artifact path")
            elif Path(declared).resolve() != Path(html_artifact).resolve():
                errors.append("supplied HTML artifact does not match declared artifact path")
            else:
                errors.extend(_validate_html_artifact(html_artifact))

    for line in re.findall(r"^[ \t]+[0-9]+\..*$", text, re.MULTILINE):
        if not re.search(r"\[(tutorial|how-to|reference|explanation)\]", line):
            errors.append(f"structure entry missing valid mode tag [tutorial|how-to|reference|explanation]: {line}")
    if re.search(r"^--- ", text, re.MULTILINE) and not re.search(r"^reason:", text, re.MULTILINE):
        errors.append("diff output must include reason:")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a technical-writing output contract.")
    parser.add_argument("--html-artifact", help="also parse and validate this actual HTML file")
    args = parser.parse_args()
    errors = validate(sys.stdin.read(), args.html_artifact)
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    scope = "metadata + supplied HTML artifact" if args.html_artifact else "metadata only (HTML artifact not supplied)"
    print(f"OK ({scope})")


if __name__ == "__main__":
    main()


