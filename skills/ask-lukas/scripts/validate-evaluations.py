#!/usr/bin/env python3
"""Validate captured fresh-model responses against catalog behavioral cases.

This checks decisions reported by a model, not whether actions actually ran.
Run evaluations only with explicit evaluation/test authorization. Expected
answers must never be included in the model prompt.
"""

import argparse
import json
import sys
from pathlib import Path

CASE_PATH = Path(__file__).resolve().parents[1] / "evals" / "evals.json"
LIST_FIELDS = ("executions", "mutations", "user_invocations", "decisions")


def validate_responses(cases, responses):
    errors = []
    if not isinstance(responses, list):
        return ["responses must be a JSON array"], 0
    expected = {case["id"]: case for case in cases}
    seen = set()
    passed = 0
    for row in responses:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            errors.append("each response needs a string id and response object")
            continue
        identity = row["id"]
        if identity not in expected or identity in seen:
            errors.append(f"{identity}: unknown or duplicate case")
            continue
        seen.add(identity)
        response = row.get("response")
        if not isinstance(response, dict):
            errors.append(f"{identity}: response must be an object")
            continue
        before = len(errors)
        for field in LIST_FIELDS:
            value = response.get(field)
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                errors.append(f"{identity}: {field} must be a string array")
        if not isinstance(response.get("rationale"), str) or not response["rationale"].strip():
            errors.append(f"{identity}: rationale must explain the decision")
        criterion = expected[identity]["expected"]
        routes = criterion["route"] if isinstance(criterion["route"], list) else [criterion["route"]]
        if response.get("route") not in routes:
            errors.append(f"{identity}: route must be one of {routes}, got {response.get('route')}")
        for field in ("executions", "mutations", "user_invocations"):
            if field in criterion and response.get(field) != criterion[field]:
                errors.append(f"{identity}: {field} must be {criterion[field]}")
        # No case permits starting another human-invoked orchestrator implicitly.
        if response.get("user_invocations"):
            errors.append(f"{identity}: user-invoked recommendations must not be automatic invocations")
        decisions = response.get("decisions", [])
        if isinstance(decisions, list):
            for decision in criterion.get("required_decisions", []):
                if decision not in decisions:
                    errors.append(f"{identity}: missing behavioral decision {decision}")
        if len(errors) == before:
            passed += 1
    for identity in sorted(set(expected) - seen):
        errors.append(f"{identity}: missing response")
    return errors, passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path, help="JSON array of {id, response} from actual fresh-model runs")
    parser.add_argument("--cases", type=Path, default=CASE_PATH)
    args = parser.parse_args()
    try:
        cases = json.loads(args.cases.read_text(encoding="utf-8"))["cases"]
        responses = json.loads(args.responses.read_text(encoding="utf-8"))
        errors, passed = validate_responses(cases, responses)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}))
        return 1
    print(json.dumps({"valid": not errors, "passed": passed, "total": len(cases), "scope": "reported model decisions only; no action execution verified", "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
