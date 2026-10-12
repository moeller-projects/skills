#!/usr/bin/env python3
"""resolve-ado-user.py
Purpose: Resolve an Azure DevOps user identity by email for work-item mention markup.
Inputs: --organization (or ADO_ORGANIZATION) and --email options.
Outputs: Resolved identity and mention markup JSON on stdout; structured BLOCKER or ERROR output on stderr.
Side effects: Performs one authenticated Azure DevOps identities GET with bounded retries.
Requires Python 3.9+, standard library only. Run with: python scripts/resolve-ado-user.py
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib


def main() -> None:
    organization = __import__("os").environ.get("ADO_ORGANIZATION", "")
    email = ""
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ("--organization", "--email"):
            if i + 1 >= len(args):
                print(f"Unknown argument: {args[i]}", file=sys.stderr)
                raise SystemExit(1)
            if args[i] == "--organization":
                organization = args[i + 1]
            else:
                email = args[i + 1]
            i += 2
        else:
            print(f"Unknown argument: {args[i]}", file=sys.stderr)
            raise SystemExit(1)
    missing = []
    if not organization:
        missing.append("organization")
    if not email:
        missing.append("email")
    if missing:
        lib.emit_blocker("MISSING_INPUT", missing, "Provide organization and email before resolving an Azure DevOps user.")
    if "@" not in email:
        lib.emit_error("PARSE_FAILED", "parse", "--email must be a valid email address.", "Provide an email address such as user@example.com.")

    lib.require_pat()
    email_lower = email.lower()
    encoded = quote(email_lower, safe="")
    url = f"https://vssps.dev.azure.com/{organization}/_apis/identities?searchFilter=General&filterValue={encoded}&queryMembership=None&properties=Mail,Account,SignInAddress&api-version={lib.API_VERSION}"
    payload = lib.http_get_json(
        url,
        label=f"Azure DevOps identities for {organization}",
        error_code="FETCH_FAILED",
        error_message=f"Failed to query Azure DevOps identities for {organization} after bounded retries.",
        error_recovery="Check AZURE_DEVOPS_PAT permissions, organization name, and network connectivity.",
    )
    matches = []
    for user in (payload.get("value") or []):
        props = user.get("properties") or {}
        prop_value = ((props.get("Mail") or {}).get("$value") or (props.get("Account") or {}).get("$value") or (props.get("SignInAddress") or {}).get("$value") or "")
        if (str(prop_value).lower() == email_lower or str(user.get("providerDisplayName") or "").lower() == email_lower or str(user.get("customDisplayName") or "").lower() == email_lower or str(user.get("uniqueName") or "").lower() == email_lower):
            matches.append(user)
    if not matches:
        lib.emit_error("FETCH_FAILED", "fetch", f"No Azure DevOps identity was found for email {email} in organization {organization}.", "Verify the email is in this Azure DevOps organization and retry.")
    if len(matches) != 1:
        lib.emit_error("FETCH_FAILED", "fetch", f"Multiple Azure DevOps identities matched email {email} in organization {organization}.", "Resolve the identity ambiguity in Azure DevOps, then retry with a unique email.")
    user = matches[0]
    mention_id = user.get("id") or user.get("originId") or ""
    if not mention_id:
        lib.emit_error("PARSE_FAILED", "parse", f"Azure DevOps identity response did not include id or originId for {email}.", "Check Azure DevOps identity data and retry.")
    display_name = user.get("providerDisplayName") or user.get("customDisplayName") or user.get("displayName") or ""
    display_name = str(display_name) if display_name else email
    mention_markup = f'<a href="#" data-vss-mention="version:2.0,{{{html.escape(str(mention_id), quote=True)}}}">@{html.escape(display_name, quote=False)}</a>'
    result = {
        "organization": organization,
        "email": email,
        "mention_id": str(mention_id),
        "descriptor": str(user.get("descriptor") or ""),
        "identity_id": str(user.get("id") or ""),
        "origin_id": str(user.get("originId") or ""),
        "display_name": display_name,
        "principal_name": str(user.get("uniqueName") or user.get("principalName") or ""),
        "mention_markup": mention_markup,
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
