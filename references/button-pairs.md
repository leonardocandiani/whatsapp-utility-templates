# Buttons: one accept, one decline, and the click has to land somewhere

Every UTILITY skeleton in this pattern carries exactly two quick-reply
buttons, and both answer the question the skeleton itself asks. The accept
confirms the pending item ("Do you still want the numbers here?" asks for
"Yes, go ahead"); the decline closes the pending item without friction
("Not needed"). A generic label that doesn't match the closing question
("Yes, that's me" on a skeleton that asks about a quote) is a design error.

## Why "Block this number" is the wrong second button

Measured on a live template that sent 2,818 messages in a single day: 105
clicks on "Block this number" against 49 on the accept button. The button
does help approval and number quality (it reads as an easy opt-out to Meta),
and it costs you in opt-outs. That's a product decision, not a formatting
one, and on its own it fails the button-pair rule below because the click
usually isn't wired to anything: the reader asks to stop and keeps
receiving messages anyway.

## The rules, in the order the checker enforces them

1. **Accept first, decline second.** Position is a contract: the send logic
   records the click payload by index, not by label text.
2. **Up to 20 characters, and never these words**: "more", "see", "want",
   "know", "learn", "continue" (the `BAD_BUTTON_WORDS` list in
   `scripts/check.py`). "Not needed anymore" fails because of "more".
3. **The decline closes the pending item, not the channel.** "Not needed"
   or "No, cancel" end that specific case; a global opt-out stays a matter of
   explicit text from the reader, never a button.
4. **When the skeleton has no question to decline** (a plain notice, nothing
   pending), the second button isn't a decline: "I have a question" asks for
   attention instead, and gets treated as an accept.

## The payload contract (so the click routes without depending on the label)

Every button ships with a payload, not just a label, so the webhook can
route the click without depending on button text (which the reader's app
may localize, truncate, or a future edit to the template may change):

```json
{ "type": "QUICK_REPLY", "text": "Yes, go ahead" }
```

sends with

```json
{ "type": "payload", "payload": "<context>:<id>:accept" }
```

on index 0, and `<context>:<id>:decline` on index 1. `<context>` names the
kind of thing being answered (a case, a batch, an appointment); `<id>`
identifies which one. Without a payload, Meta hands back the button's
label text on click, and the receiving system ends up depending on a string
that a template edit can silently break.

## What the click means once it lands

| Click | What should happen |
|---|---|
| Accept | Mark the pending item as accepted, hand the conversation to whoever owns it, notify them that the reader responded |
| Decline | Mark the pending item as declined, and suppress that specific pending item from re-triggering for some cooldown window (not a permanent number-level opt-out) |
| Delivered / read (webhook status events) | Advance delivery and read tracking on the pending item, so a dashboard doesn't show "0 arrived" when everything actually arrived |

A global stop-messaging request only comes from explicit text from the
reader ("stop", "remove me", the local equivalent), never inferred from a
button click on a specific case.
