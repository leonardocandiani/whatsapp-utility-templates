# Send preflight: fail-closed before every message

Approval is not permanent. A template that is `APPROVED`/`UTILITY` today
can turn into `MARKETING` tomorrow, from a user complaint or a quality
drop, with no warning at all. The code that actually sends the message has
no way to know that unless it asks again, right before sending. This is
the contract any integration should replicate, whatever language or
framework it runs on, instead of inventing its own preflight from scratch.

## What gets checked

`GET /{waba}/message_templates?name=<name>&fields=name,language,status,category,previous_category,quality_score`
before every send, with a short timeout and no silent redirect following.
The match needs the name **and** the declared language to agree at the
same time: the same name can exist across different WABAs, or in different
languages inside the same WABA, and the wrong item passing the check
without anyone noticing is exactly the failure mode this guards against.

## What decides a pass

Two conditions, both required:

1. **Exactly one item matches** on name and language. Zero matches (the
   template disappeared) or more than one (a name collision) both fail.
2. **`status === "APPROVED"` and `category === "UTILITY"`**, at the same
   time. Any other combination blocks the send: `PENDING`, `REJECTED`,
   `PAUSED`, or `DISABLED` on the status side; `MARKETING` or
   `AUTHENTICATION` on the category side. There is no "let it through this
   once, it's just a warning": a failed check means the message does not
   go out.

A deeper implementation can go one step further and compare the
structural shape of the approved content against the payload about to be
sent, component by component (`BODY`, `HEADER`, `BUTTONS`), including
validating that a dynamic `URL` button follows its suffix contract. That
catches a template that is `APPROVED` and `UTILITY` but whose live
definition drifted from what the sending code assumes it looks like. This
skill's own `scripts/check.py` covers a related but different concern
(rejecting a definition before it is ever submitted); the send preflight
covers what happens after approval, at send time, for every single send.

## What happens on each outcome

| Meta returns | Preflight does |
|---|---|
| `APPROVED` + `UTILITY` | Passes. Only this pair. |
| `APPROVED` + `MARKETING` | Blocks. A real reclassification; the reason cites `previous_category` when it is present. |
| `PAUSED` / `DISABLED` | Blocks. Status is not `APPROVED`, category does not matter. |
| `REJECTED` | Blocks. |
| Network error, timeout, non-2xx response | Blocks. **Never** lets the send through "to be safe" or "because it could not confirm". Fail-closed means exactly this: no positive confirmation, no send. |
| Zero or more than one match | Blocks, same as not found. |

## Caching: one hour, with a bypass

Checking Meta before every single message does not scale (rate limits,
latency). The pattern is to cache the result for one hour and serve from
cache inside that window, with an explicit flag to force a fresh check.
The cache is never a fallback for a failed live check: it only ever holds
what Meta answered on the last successful live check. A stale cache plus
Meta being unreachable is a block, not "the last good answer we had".

## Monitoring: scan the whole WABA

A per-template preflight covers a single send. To catch a reclassification
before anyone even tries to send anything, a periodic full-WABA scan
compares every template's current category against the category recorded
on the previous scan, and reports who changed. That is what turns into a
daily cron job: an alert that fires before someone hits the wrong surprise
at send time.

## Reference implementation

`scripts/preflight.py` in this repository implements this exact contract,
standalone, stdlib only. Run it before any send, and run it with a
full-WABA scan on a schedule:

```bash
export META_TOKEN="..."
export META_WABA="<your WABA id>"
python3 scripts/preflight.py utility_case_followup_v1
python3 scripts/preflight.py utility_case_followup_v1 --lang pt_BR --fresh
python3 scripts/preflight.py --all
```

`ok: <name> APPROVED UTILITY (cache|live)` with exit 0 is the only output
that authorizes a send. Any `blocked: ...` with exit 1 means no, without
exception.
