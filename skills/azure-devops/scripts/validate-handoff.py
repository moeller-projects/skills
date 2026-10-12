#!/usr/bin/env python3
"""validate-handoff.py
Purpose: Read a contract JSON from stdin, validate it against the shared schema, and write it unchanged.
Inputs: Contract JSON on stdin.
Outputs: Valid contract JSON on stdout; structured ERROR output on stderr on validation failure.
Side effects: Reads the shared JSON schema only.
Requires Python 3.9+, standard library only. Run with: python scripts/validate-handoff.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def type_matches(value: Any, expected: str) -> bool:
    actual = type_name(value)
    if expected == "number":
        return actual in {"integer", "number"}
    return actual == expected


def walk(value: Any, node: Dict[str, Any], path: List[str]) -> None:
    if "const" in node and value != node["const"]:
        raise ValueError(path, f"expected constant {node['const']!r}, got {value!r}")
    if "enum" in node and value not in node["enum"]:
        raise ValueError(path, f"expected one of {node['enum']!r}, got {value!r}")
    if "type" in node:
        expected = node["type"]
        expected_types = expected if isinstance(expected, list) else [expected]
        if not any(type_matches(value, item) for item in expected_types):
            raise ValueError(path, f"expected type {expected_types!r}, got {type_name(value)!r}")
    if type_name(value) == "object":
        for key in node.get("required", []):
            if key not in value:
                raise ValueError(path, f"missing required property {key!r}")
        properties = node.get("properties", {})
        if node.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise ValueError(path, f"unexpected properties {extra!r}")
        for key, child in properties.items():
            if key in value:
                walk(value[key], child, path + [key])
    if type_name(value) == "array" and "items" in node:
        for index, item in enumerate(value):
            walk(item, node["items"], path + [str(index)])


def main() -> int:
    schema_path = Path(__file__).resolve().parent.parent / "assets" / "schemas" / "ado-openspec-handoff.schema.json"
    raw = sys.stdin.read()
    instance = json.loads(raw)
    with schema_path.open(encoding="utf-8") as fh:
        schema = json.load(fh)
    try:
        walk(instance, schema, [])
    except ValueError as err:
        path, message = err.args
        location = " → ".join(path) or "(root)"
        print("ERROR:", file=sys.stderr)
        print("code: NORMALIZATION_FAILED", file=sys.stderr)
        print("stage: emit", file=sys.stderr)
        print(f"message: Schema validation failed at {location}: {message}", file=sys.stderr)
        print("recovery: Check the emitted contract against assets/schemas/ado-openspec-handoff.schema.json", file=sys.stderr)
        return 1
    sys.stdout.write(raw)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
