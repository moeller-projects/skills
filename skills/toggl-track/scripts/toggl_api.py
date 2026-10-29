#!/usr/bin/env python3
"""Make one authenticated JSON request to a Toggl Track API endpoint.

The caller must choose the service host and endpoint from Toggl's OpenAPI contract.
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SERVICES = {
    "core": "https://api.track.toggl.com/api/v9",
    # Reports OpenAPI paths already include /reports/api/v3.
    "reports": "https://api.track.toggl.com",
    "webhooks": "https://api.track.toggl.com/webhooks/api/v1",
}
MUTATING = {"POST", "PUT", "PATCH", "DELETE"}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service", choices=sorted(SERVICES), help="API service")
    parser.add_argument("method", choices=("GET", "POST", "PUT", "PATCH", "DELETE"))
    parser.add_argument("path", help="Path relative to the service base URL")
    parser.add_argument("--query", action="append", default=[], metavar="KEY=VALUE",
                        help="Query parameter; may be repeated")
    parser.add_argument("--body", help="JSON request body; omit when no body is required")
    parser.add_argument("--allow-mutation", action="store_true",
                        help="Required for POST, PUT, PATCH, and DELETE requests")
    parser.add_argument("--timeout", type=float, default=30, help="Request timeout in seconds (default: 30)")
    return parser.parse_args()


def main():
    args = parse_args()
    token = os.environ.get("TOGGL_API_TOKEN")
    if not token:
        print("error: set TOGGL_API_TOKEN in the environment; do not pass the token as an argument", file=sys.stderr)
        return 2
    if args.method in MUTATING and not args.allow_mutation:
        print("error: this request can change remote data; obtain confirmation, then pass --allow-mutation", file=sys.stderr)
        return 2
    if args.timeout <= 0:
        print("error: timeout must be greater than zero", file=sys.stderr)
        return 2

    path = args.path.lstrip("/")
    if ".." in path.split("/") or "#" in path:
        print("error: path must be a relative API path without traversal or fragments", file=sys.stderr)
        return 2
    query = urllib.parse.urlencode([parse_query(item) for item in args.query])
    url = SERVICES[args.service] + "/" + path
    if query:
        url += "?" + query

    body = None
    headers = {"Accept": "application/json"}
    if args.body is not None:
        try:
            body = json.dumps(json.loads(args.body)).encode("utf-8")
        except (ValueError, TypeError) as exc:
            print(f"error: --body must contain valid JSON: {exc}", file=sys.stderr)
            return 2
        headers["Content-Type"] = "application/json"

    # Toggl API-token Basic auth uses the token as username and literal
    # "api_token" as password.
    credentials = base64.b64encode(f"{token}:api_token".encode("utf-8")).decode("ascii")
    headers["Authorization"] = "Basic " + credentials
    request = urllib.request.Request(url, data=body, headers=headers, method=args.method)
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            payload = response.read()
            if payload:
                sys.stdout.buffer.write(payload)
                if not payload.endswith(b"\n"):
                    sys.stdout.buffer.write(b"\n")
            return 0
    except urllib.error.HTTPError as exc:
        # Do not echo request headers or credentials; response text is bounded.
        detail = exc.read(2000).decode("utf-8", errors="replace").replace(token, "[REDACTED]")
        print(f"error: Toggl returned HTTP {exc.code}: {detail}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        detail = str(exc).replace(token, "[REDACTED]")
        print(f"error: request failed: {detail}", file=sys.stderr)
        return 1


def parse_query(item):
    key, separator, value = item.partition("=")
    if not separator or not key:
        raise ValueError("query parameters must use KEY=VALUE")
    return key, value


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
