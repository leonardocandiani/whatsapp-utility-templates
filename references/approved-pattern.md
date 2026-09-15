# Real catalog: approved and rejected

Source: 33 templates read from the Graph API on a live WABA belonging to a
vehicle protection company selling to independent truck drivers, mostly
through WhatsApp outreach. 19 UTILITY templates approved, 14 MARKETING
templates approved on the same WABA. All company names, agent names,
customer names, protocol numbers, and phone numbers below are placeholders;
the wording, structure, and verdicts are the real measured data.

## UTILITY approvals that follow the Swiss-army pattern (opener + anchor + wide slot + closer)

**`utility_case_followup_v1`**
```
Hi, {{1}}! About your case: {{2}} Just reply here.
```
Buttons: Continue | Not now
Real example: "Marcos", "we received the confirmation of your details on ticket #8214, logged on 07/15/2026, and the next step is already unlocked."

**`utility_case_question_v1`**
```
Hi, {{1}}! There's something pending here: {{2}} Reply here to sort it out.
```
Buttons: Sort it now | Later
Real example: "Paulo", "one field on your record for ticket #5711 needs confirming to close out the step logged on 07/14/2026."

**`utility_case_notice_v2`**
```
Hello, {{1}}. Update on your case: {{2}} Any questions, just reply.
```
Buttons: See details | No, thanks
Real example: "Fernando", "ticket #3390, opened on 07/13/2026, was updated in the system and is waiting on your confirmation."

**`utility_proposal_update_v1`**
```
Hello, {{1}}. Update on your proposal for plate {{2}}: {{3}} Any questions, reply here.
```
Buttons: See proposal | Not now
Real example: "Paulo", "DEF4G56", "it's still on hold in the system under the same terms I showed you."

**`utility_case_pending_v1`**
```
Hello, {{1}}. Your case with us has an open item: {{2}}. {{3}} Reply here to resolve it.
```
Buttons: Resolve now | Later
Real example: "Marcos", "confirm your details", "It's quick, one minute fixes it."

**`utility_payment_status_v1`**
```
Hello, {{1}}. About the payment for plate {{2}}: {{3}} If you need a duplicate, reply here.
```
Buttons: Send duplicate | Already paid
Real example: "Fernando", "GHI7J89", "the PIX generated on 07/15/2026 is still valid and activation completes once it clears."

**`utility_minimal_case_v1`** (a leaner version of the same pattern, no buttons)
```
Hello, {{1}}. {{2}}. Reply here and I'll explain further.
```
Real example: "Rebeca", "we received the payment confirmation for ticket #1199, made on 10/12/2025"

## UTILITY approval for a voice follow-up

**`utility_appointment_reminder`**
```
Reminder: our advisor will call you on {{1}} at {{2}} to go over your truck's details. Please be available.
```
No buttons. A pure appointment reminder, nothing sales-related.

## UTILITY with a currency value in the body (a historical exception, do not copy)

One approved template carried `Payment amount: *$ {{3}}* via PIX.` in the body.
It got approved, but it predates the company's current rule that price never
leaves a live conversation. A new template with a price in the body should
not be modeled after this one.

## MARKETING approvals (same sender, same product, different category)

**`marketing_social_proof_v1`**
```
Hi, {{1}}! How's it going?
This is Jamie, from RoadShield
...Today, over 42,000 members have already chosen RoadShield for a simple,
affordable protection plan built for people who live on the road...
```
Reason: numeric social proof and an invitation to learn about the product,
nothing about anything the reader already has.

**`marketing_scarcity_v1`**
```
Hi, {{1}}!
I'm finishing up enrollment today, and only a few spots are left with
RoadShield's special terms.
...If you want out of the risk, message me now, this window might close.
```
Reason: artificial scarcity ("only a few spots left") and deadline pressure,
a classic sales trigger.

**`marketing_seasonal_v1`**
```
Hi, {{1}}! Jamie, from RoadShield, here.
Riding the Black Friday wave, we have special vehicle protection deals for
truck drivers.
```
Reason: an explicit promotional date in both the body and the template name.

**`marketing_price_pitch_v1`**
```
I'm reaching out because over 42,000 truck drivers have already chosen
RoadShield, protection with no red tape and guaranteed payout.
Our price is among the best in the market!
```
Reason: price comparison and social proof, no anchor to an existing case.

**`marketing_cold_open_v1`**
```
This is Jamie from RoadShield, real protection for people who live on the road
...Does it make sense to learn more about how this could help you?
```
Reason: a literal cold outreach message, an invitation to learn about the
product from zero.

## Button patterns observed on both sides

Every approved UTILITY template used only quick-reply buttons, at most two,
with short labels ("Continue", "Not now", "See proposal", "Resolve now",
"Later", "Send duplicate", "Already paid"). None of the UTILITY approvals in
this corpus used a "Block this number" button.

Approved MARKETING templates sometimes paired a `URL` button ("Tap here")
with a `QUICK_REPLY`, plus an image or video header. A media header by
itself doesn't define marketing (one UTILITY approval in the corpus carried
an image header), but the pattern this skill teaches, a plain-text
Swiss-army template, never carries a header: simpler to write, to audit, and
to resubmit as `_v2` if it gets rejected.

## One template submitted in two languages, two different review outcomes

The same body text got submitted twice, once declared as `pt_BR` and once as
`en`, both containing the same Portuguese sentence. That's a real trap in
the live catalog: the declared language at submission time doesn't have to
match the language of the text, but it does have to match the `language.code`
that the actual send will declare later. Always declare the language that
matches the text; don't copy this pattern of duplicating a template under a
second declared language.
