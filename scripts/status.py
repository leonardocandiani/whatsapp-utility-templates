#!/usr/bin/env python3
"""Look up a WhatsApp template's status (Meta Graph API) by name.

Usage:
    export META_TOKEN="..."
    export META_WABA="<your WABA id>"
    python3 status.py utility_case_followup_v1

Returns status (PENDING, APPROVED, REJECTED), category, and, when rejected,
rejected_reason. The token is never printed, in any output, log, or error.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

GRAPH_VERSION = "v21.0"
FIELDS = "id,name,language,status,category,rejected_reason,components"


def look_up(waba: str, token: str, name: str) -> dict:
    query = urllib.parse.urlencode({"name": name, "fields": FIELDS, "limit": "100"})
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{waba}/message_templates?{query}"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
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
    if len(sys.argv) != 2:
        print("usage: python3 status.py <template_name>", file=sys.stderr)
        sys.exit(2)

    token = os.environ.get("META_TOKEN")
    waba = os.environ.get("META_WABA")
    if not token:
        print("error: META_TOKEN environment variable is not set", file=sys.stderr)
        sys.exit(2)
    if not waba or not waba.isdigit():
        print("error: META_WABA environment variable is missing or not numeric", file=sys.stderr)
        sys.exit(2)

    name = sys.argv[1]
    result = look_up(waba, token, name)
    items = result.get("data", [])

    if not items:
        print(json.dumps({"found": False, "name": name}, ensure_ascii=False, indent=2))
        sys.exit(0)

    for item in items:
        output = {
            "id": item.get("id"),
            "name": item.get("name"),
            "language": item.get("language"),
            "status": item.get("status"),
            "category": item.get("category"),
        }
        if item.get("status") == "REJECTED" and item.get("rejected_reason"):
            output["rejected_reason"] = item["rejected_reason"]
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
