#!/usr/bin/env python3
"""Submit a WhatsApp template (Meta Graph API) to a WABA.

Usage:
    export META_TOKEN="..."
    export META_WABA="<your WABA id>"
    python3 submit.py definition.json [--lang pt|en]

`definition.json` is the exact body of the POST to
/{waba}/message_templates, in the format described in the SKILL.md
submission contract. Before the request goes out, this script runs
check.check(): a definition that tends to become MARKETING never leaves
here. There is no flag to skip the check; a template outside the pattern
gets rewritten instead.

The token is never printed, in any output, log, or error message.
"""

import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check

GRAPH_VERSION = "v21.0"


def load_definition(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_definition(definition: dict) -> None:
    if definition.get("category") != "UTILITY":
        raise SystemExit("error: category must be UTILITY (this skill does not submit any other category)")
    if definition.get("allow_category_change") is not False:
        raise SystemExit("error: allow_category_change must be false (house contract)")
    if not definition.get("name") or not definition.get("language"):
        raise SystemExit("error: definition is missing name or language")
    if not isinstance(definition.get("components"), list) or not definition["components"]:
        raise SystemExit("error: definition is missing components")


def submit(waba: str, token: str, definition: dict) -> dict:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{waba}/message_templates"
    body = json.dumps(definition).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            structured = json.loads(error_body)
        except json.JSONDecodeError:
            structured = {"raw": error_body}
        print(json.dumps({"error": True, "status": e.code, "response": structured}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": True, "reason": str(e.reason)}, ensure_ascii=False, indent=2))
        sys.exit(1)


def main() -> None:
    args = sys.argv[1:]
    lang = "pt"
    if "--lang" in args:
        idx = args.index("--lang")
        try:
            lang = args[idx + 1]
        except IndexError:
            print("usage: --lang expects a value (pt|en)", file=sys.stderr)
            sys.exit(2)
        del args[idx:idx + 2]

    if len(args) != 1:
        print("usage: python3 submit.py <definition.json> [--lang pt|en]", file=sys.stderr)
        sys.exit(2)

    token = os.environ.get("META_TOKEN")
    waba = os.environ.get("META_WABA")
    if not token:
        print("error: META_TOKEN environment variable is not set", file=sys.stderr)
        sys.exit(2)
    if not waba or not waba.isdigit():
        print("error: META_WABA environment variable is missing or not numeric", file=sys.stderr)
        sys.exit(2)

    definition = load_definition(args[0])
    validate_definition(definition)
    reasons = check.check(definition, lang=lang)
    if reasons:
        print("rejected before submission: this template tends to become MARKETING", file=sys.stderr)
        for reason in reasons:
            print(f"- {reason}", file=sys.stderr)
        sys.exit(1)

    result = submit(waba, token, definition)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if "id" in result:
        print(
            f"\nsubmitted: id={result['id']} status={result.get('status', 'PENDING')} "
            f"category={result.get('category', '?')}",
            file=sys.stderr,
        )
        print(
            f"track with: python3 status.py {definition['name']}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
