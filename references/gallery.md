# Gallery from three real WABAs (measured September 2026)

Source: a full pull from the Graph API across three WABAs belonging to the
same vehicle protection company, anonymized as RoadShield. One WABA runs a
Gallabox-based chat channel (33 templates), one runs an outbound research
line (51 templates), and one is a central messaging account for the sales
team (21 templates). Meta's analytics window covers 89 days. Meta returns
`quality_score: UNKNOWN` for all 105 templates in this capture, without
exception, so there is no way to cross category against a quality score
here. The research WABA's own template analytics endpoint returns zero for
every template; its real send numbers come from the company's own delivery
log instead, and are labeled as such below. All 105 templates across the
three WABAs are `APPROVED`; there is no `REJECTED` or `PENDING` template in
this capture. Company, agent, and lead names are placeholders; wording,
counts, and verdicts are real.

Two caveats about that delivery log apply to every number below that comes
from the research WABA: (1) the log does not store which button label was
clicked, so "clicks per button" has no measurement on that WABA even when a
send count exists; (2) one internal event fires on almost every delivered
message as a pipeline artifact at send time, not as a reply from the reader,
so every "reply rate" figure below already excludes that artifact rather
than counting it as engagement. Opt-out on that WABA, where cited, is a
share of reads, not a share of sends (an honest denominator).

## Utility skeleton family (50 templates)

The two-layer mold this skill already documents: a short, protocol-style
body, a fixed name and speaker, one wide slot that carries the real
sentence, and a closing question or instruction. This is the largest family
in the gallery, and also the most repetitive: of the 51 templates on the
research WABA, 30 turn out to be only three distinct texts submitted ten
times each, with no difference in body or buttons between revisions.

### Research WABA (33 of its 51 templates)

| Body (identical revisions) | Buttons | Measured sends (company's own log) |
|---|---|---|
| "Hello, {{1}}, how is it going? Jamie here. {{2}}. Do you still {{3}}?" (`utility_case_checkin_v3` and its 10 revisions) | Yes, I do / Block this number | latest revision only: 2,422 sends, 84.2% read, 46.9% replied |
| "Hi, {{1}}, how is it going? Jamie here. {{2}}?" (`utility_case_checkin_v2` and its 10 revisions) | Yes, that's me / Block this number | latest revision only: 979 sends, 84.2% read, 44.9% replied |
| "Hello, {{1}}, how is it going? My name is {{2}}. Do you still {{3}}?" (`utility_case_checkin_v1` and its 10 revisions) | Still driving it / Block this number | latest revision only: 997 sends, 82.3% read, 40.7% replied |
| Same body as `_v3`, one revision only (`utility_case_checkin_v3_latest`) | Yes, I do / Block this number | 763 sends, 92.9% read, 40.5% replied |
| Same body as `_v2`, one revision only (`utility_case_checkin_v2_latest`) | Yes, that's me / Block this number | 1,503 sends, 87.5% read, 53.9% replied |
| Same body as `_v1`, one revision only (`utility_case_checkin_v1_latest`) | Still driving it / Block this number | 1,560 sends, 87.6% read, 60.1% replied |

Reading: the three texts share the same anatomy, only the wide slot moves
(an explicit `{{3}}` question versus a single slot `{{2}}` that already
carries the question). The one with the highest real read rate (92.9%) is
the one that separates the question from the rest of the body ("Do you
still {{3}}?"); the one with the highest reply rate (60.1%) is the
shortest, without a fixed "Jamie here", leaving the introduction to the
slot. All ten identical revisions per text only ever measured a send on the
latest one: the company keeps resubmitting the same body, apparently to
rotate the template name rather than because the text changed.

### Gallabox chat WABA (7 templates)

| Template | Body | Buttons |
|---|---|---|
| `utility_minimal_prompt_v1` | "Hey {{1}}. To continue, tap the button below." | Learn more / Block this number |
| `utility_minimal_prompt_v2` | "Hi there, {{1}}. To continue, tap the button below." | Learn more / Block this number |
| `utility_minimal_prompt_v3` | "Hello, {{1}}. To continue, pick an option below." | Learn more / Block this number |
| `utility_minimal_prompt_v4` | "Hey, {{1}}. To continue, tap the button below." | Learn more / Block this number |
| `utility_notice_plain_v1` | "Notice: {{1}} {{2}} To continue, tap the button below." | Notify me / Block this number |
| `utility_minimal_case_v1` (and its `en`-declared duplicate) | "Hello, {{1}}. {{2}}. Reply here and I will explain further." | no button |

Reading: this batch (`utility_minimal_prompt_*`) is the most minimal
skeleton in the whole corpus, with no protocol anchor at all in the fixed
text, just a greeting and "to continue". It still approved UTILITY, with a
"Learn more" button, which the checker's rule table already rejects as an
invitation to start something. That is evidence the checker's ruler is set
tighter than Meta's actual minimum: it rejects cases Meta still approves, on
purpose, because it is guarding against a future reclassification from a
complaint, not against the first approval.

### Central sales WABA (10 templates)

| Purpose | Body (latest revision) | Buttons (latest revision) |
|---|---|---|
| `utility_case_status_check` | "Hello, {{1}}, how is it going? My name is {{2}}, from RoadShield. {{3}}. Do you still {{4}}?" | Yes, go ahead / Not needed (v3); Block this number in earlier revisions |
| `utility_case_status_notice` | "Hello, {{1}}, how is it going? My name is {{2}}, from RoadShield. {{3}}. Any questions, just reply here." | Got it / I have a question (v2); Block this number in `v1` |
| `utility_case_status_reopen` | "Hello, {{1}}, how is it going? My name is {{2}}, from RoadShield. {{3}}. Do you still need that callback?" | Yes, I need it / Not needed (v3); Block this number in v2 |
| `utility_reengagement_attempt_v1` (no revision number) | "...{{3}}. Can we continue this conversation here?" | We can / Not now (**reclassified MARKETING**) |
| `utility_case_followup_v2` | "{{2}}, from RoadShield, here. About your case: {{3}} Just reply here." | Continue / Not now (**reclassified MARKETING**) |

Reading: this is the series `SKILL.md` section 6 already narrates in detail
(the two-layer mold, section "The two layers"). The gallery confirms that
swapping the second button from "Block this number" to a named decline
("Not needed", "No, cancel") is the most recent revision (`_v2`/`_v3`) of
each purpose, and the older revisions with "Block this number" stay
`APPROVED` and `UTILITY` in the catalog, just replaced in day-to-day use.
None has a measured send in this capture.

## Utility case family (31 templates)

The Swiss-army pattern: an explicit anchor to an existing case, ticket,
proposal, or pending item in the fixed text, not just the slot example. It
is the most repeated family across all three WABAs: `utility_case_followup_v1`,
`utility_case_question_v1`, `utility_case_notice_v2`, `utility_case_pending_v1`,
and `utility_proposal_update_v1` exist, with the same body, on both the
Gallabox chat WABA and the research WABA.

| Template | Body | Buttons | WABA(s) |
|---|---|---|---|
| `utility_case_followup_v1` | "Hi, {{1}}! About your case: {{2}} Just reply here." | Continue / Not now | chat, research |
| `utility_case_question_v1` | "Hi, {{1}}! There is something pending here: {{2}} Reply here to sort it out." | Sort it now / Later | chat, research |
| `utility_case_notice_v2` | "Hello, {{1}}. Update on your case ticket: {{2}} Any questions, just reply." | See details / No, thanks | chat, research |
| `utility_case_pending_v1` | "Hello, {{1}}. Your case with us has an open item: {{2}}. {{3}} Reply here to resolve it." | Sort it now / Later | chat, research |
| `utility_proposal_update_v1` | "Hello, {{1}}. Update on your proposal for plate {{2}}: {{3}} Any questions, reply here." | See proposal / Not now | chat, research |
| `utility_case_open_v1` | "*Your truck protection request is still open in the system.* To continue, just send the plate number." | Send the plate / Ask a question / Talk to a human | research |
| `utility_conversation_reopen_v1` | "Your conversation with us is still open in the support queue. Want to pick up where we left off?" | Let's continue / Later / Close it out | research |
| `utility_proposal_pending_v1` | "Your proposal for plate {{2}} is still waiting for a reply in the system until {{3}}." | Let me check / One more day / Close it out | research |
| `utility_case_progress_v1` | "The record for plate {{2}} is still open here in the system. {{3}} Reply here to close out your case." | Continue / Not now | research |
| `utility_quote_details_v1`/`v2` | "As requested, here is the quote data for vehicle {{2}}: Monthly payment {{3}}, Annual total {{4}}, Down payment {{5}}..." | Talk now | chat |
| `utility_appointment_reminder` | "Reminder: our advisor will call you on {{1}} at {{2}} to go over your truck's details." | no button | chat |
| `utility_call_permission_v1` | "Would you like to receive a call from one of our representatives?" plus a `CALL_PERMISSION_REQUEST` component | (native call-permission control, not a `QUICK_REPLY`) | chat |
| `utility_case_status_ask` / `utility_case_status_confirm` | "...here, from RoadShield, about your open case. {{3}}? Feel free to reply here." | Yes (several forms) / a named decline or Block this number | central |
| `utility_case_followup_v2` | "...from RoadShield, here. About your case: {{3}} Just reply here." | Continue / Not now (**reclassified MARKETING**) | central |
| `utility_call_confirmed_v1` | "Great news! Your call with the RoadShield advisor is confirmed for today at {{2}}." plus a `HEADER TEXT` and a `URL` button | See order (**reclassified MARKETING**) | chat |

Reading: five bodies are byte-for-byte identical between the chat WABA and
the research WABA. That confirms the case-family catalog gets copied
template by template into each new WABA, exactly as section 6 already says
("a template is per-WABA"), and neither copy has a measured send in this
capture. `utility_call_confirmed_v1` is the only reclassified template in
this family with a text header and a URL button: the body does not talk
about anything the reader asked for (a confirmed call with no ticket, no
plate), and "advisor" in the fixed text is the same sales word the checker
already flags.

## Utility media family (6 templates, all on the chat WABA)

One approval as UTILITY with an image header, and five near-identical
variants with a video header (or no header) that Meta reclassified to
MARKETING. All six share the same body:

```
Hello, {{1}}. Important notice!

We are letting you know that {{2}}

{{3}}

To {{4}}, tap the button below.
```

| Template | Header | Buttons | Category |
|---|---|---|---|
| `utility_media_notice_v1` | IMAGE | Notify me / Block this number | **UTILITY** (not reclassified) |
| `utility_media_notice_v2` | none | Want to know more / Not interested | MARKETING (was UTILITY) |
| `utility_media_notice_v3` | VIDEO | Want to know more / Not interested | MARKETING (was UTILITY) |
| `utility_media_notice_v4` | VIDEO | Want to know more / Not interested | MARKETING (was UTILITY) |
| `utility_media_notice_v5` | VIDEO | URL "Tap here" / Want to know more / Block contact | MARKETING (was UTILITY) |
| `utility_media_notice_v6` | VIDEO | URL "Tap here" / Talk to an advisor / Block | MARKETING (was UTILITY) |

Reading, and this is the strongest finding in this family: **the body is
identical across all six, and what separates the one that stayed UTILITY
from the five that became MARKETING is only the accept button's label.**
`utility_media_notice_v1` uses "Notify me", a verb that acknowledges
something that already arrived; the five reclassified ones use "Want to
know more" or "Talk to an advisor", which are invitations to start
something, exactly the pattern `SKILL.md`'s "what sinks it, what holds it"
table already lists for plain text templates. **The gallery extends that
rule to confirm it holds the same way for an image or a video header**:
Meta does not treat media as a free pass, it reads the button the same way.
None of the six carries a header example that speaks to any specific
RoadShield content (the `header_handle` is a generic WhatsApp media asset
URL), so this data cannot say whether the media content itself weighs in,
only the body-plus-button pair.

## Utility billing family (5 templates)

| Template | Body (excerpt) | Buttons | WABA(s) |
|---|---|---|---|
| `utility_billing_reminder_v1` | "*Your membership for plate {{2}} is still waiting on confirmation in the system.* Membership amount: *$ {{3}}* via bank transfer. Expires on {{4}}." | Let's activate / One more day / Talk to support | chat, research |
| `utility_payment_status_v1` | "About the payment for plate {{2}}: {{3}} If you need a duplicate, reply here." | Send duplicate / Already paid | chat, research |
| `utility_document_reminder_v1` | "Your membership for plate {{2}} is waiting on a document: {{3}}. Send it here on WhatsApp to unlock the next step." | I'll send it / Ask a question / Talk to support | research |

Reading: `utility_billing_reminder_v1` stays `APPROVED`/`UTILITY` on both
WABAs where it exists, with a currency value spelled out in the body
(`$ {{3}}`), confirming the exception `SKILL.md` section 2 already flags
("a historical exception, do not copy"). No other template in the gallery
carries a currency amount in the fixed text this way. `utility_document_reminder_v1`,
in the same billing/pending-process family, asks for a document, not money,
so it does not carry the same exception.

One nuance worth flagging that the gallery surfaced and the skill's earlier
text did not: `utility_quote_details_v1`/`v2` (see the case family above)
lists monthly payment, annual total, and down payment through slots labeled
in the fixed text (`Monthly payment: {{3}}`), without a literal `$` sign
baked into the body itself. That is money-shaped structure without the
currency exception's exact signature, and it approved UTILITY anyway. It is
not the same pattern as `utility_billing_reminder_v1`, and it should not be
read as a second confirmed exception, but it is close enough to the line
that a new billing template should not assume the "no money" rule is a
blanket ban on numeric fields tied to a quote.

## Marketing open family (8 templates, all on the chat WABA)

None of the eight carries a `BUTTONS` component, all have a single name
slot and sign off as "Jamie, from RoadShield". None has a measured send in
this capture.

| Template | Marketing trigger | Excerpt |
|---|---|---|
| `marketing_social_proof_v1` / `v2` | numeric social proof | "over 42,000 members have already chosen RoadShield" |
| `marketing_seasonal_v1` | promotional date | "Riding the Black Friday wave" |
| `marketing_followup_nudge_v1` | price comparison | "our price is one of the best in the market" |
| `marketing_price_pitch_v1` | social proof plus price | "42,000 truck drivers... price among the best in the market" |
| `marketing_referral_v1` | referral-based social proof | "58% of new members come in through a referral" |
| `marketing_scarcity_v1` | scarcity | "only a few spots left with special terms" |
| `marketing_cold_open_v1` | cold outreach | "Does it make sense to learn more about how this could help you?" |

Reading: matches `references/approved-pattern.md` point for point, no new
finding here. This is the family with zero ambiguity: none of these eight
talk about anything the reader already has.

## Noise (5 templates, either test traffic or off-topic for this domain)

`noise_test_connection_v1` ("This is a real test of the official ZapMentor
connection with Meta") is an integration smoke test, no doctrine value here.
The four `noise_out_of_scope_v1` through `v4` belong to a different
product line (wording about "terms", "model", "no credit check" reads like
vehicle financing, not vehicle protection), reusing the same research WABA
by scope mistake or cross-testing. Interestingly, `noise_out_of_scope_v1` is
the only template in the entire gallery with a real send measured directly
by Meta's own analytics endpoint (not the company's delivery log): 3,576
sends, 76.3% read, an accept button ("Work out the numbers") with 56 clicks
against a decline ("No, thanks") with 318. It stays here as a data
curiosity (the only native Meta measurement in the whole capture), not as a
doctrine example: it is not a RoadShield template and should not feed any
anatomy lesson.

## What the gallery changes in the rule

1. **The button decides more than the header, even on a media template.**
   The six "Important notice" templates share an identical body; the one
   that stayed UTILITY uses "Notify me", the five that became MARKETING use
   "Want to know more" or "Talk to an advisor". Section 2 of `SKILL.md`
   already said an image or video header belongs to "a different family",
   but it did not say the button rule from the button-pairs reference holds
   the same way for that family. It does, and the gallery is the proof.

2. **None of the 105 templates carries a `quality_score` other than
   `UNKNOWN`.** This skill cannot claim a correlation between quality score
   and category from this capture: the account does not expose that score.
   Any future claim that "a low quality score triggers reclassification"
   needs a different source (an event history, not the template's current
   state).

3. **"Block this number" is the single most used button in the whole
   corpus.** It is the confirmation of what the button-pairs reference
   already argues against: the button helped approval across all three
   WABAs, but nobody wired the click to an actual opt-out, and old
   revisions carrying it stay live in the catalog, just superseded by newer
   revisions. When designing a new skeleton, check whether that purpose
   already has an older revision with that button before repeating it.

4. **Almost half the templates in this capture are an identical revision of
   a body that already exists, not new content.** The three texts in the
   `utility_case_checkin` series alone account for 30 of the 105 templates,
   all sharing the same body and button pair, and only the latest revision
   of each ever has a measured send. Proliferating a revision without
   changing the text is not the same thing as testing a variant; it is a
   template name spent without any learning gained. When the real goal is
   rotating the sender or dodging a per-template frequency limit, that
   should be said in the name or a catalog comment, not look like ten A/B
   attempts that never diverged.

5. **Only 7 of the 105 templates have any measured send in this capture
   (6.7%).** Six come from the company's own delivery log (not Meta's
   analytics endpoint, which returns zero for that WABA), and one comes
   from Meta's own API but belongs to a template outside this company's
   domain. That means this gallery describes **approved anatomy**, not
   **campaign performance**: most of the 105 templates exist in the
   catalog but were never actually sent at volume in this 89-day window, or
   were sent through a channel that records neither Meta template analytics
   nor an equivalent delivery log of its own.

6. **Among the ones that were measured, read rate and reply rate move
   independently, even between near-identical texts.** The template with
   the best read rate (92.9%) replies worse (40.5%) than the one with the
   best reply rate (60.1%, 87.6% read). The difference between the two is
   where the speaker's name sits: fixed in the first, inside a slot in the
   second. Reading more does not mean replying more; when the two metrics
   disagree, the one that decides a handoff to a human agent is reply rate,
   not read rate.

7. **The case and skeleton anatomies replicate template by template between
   two WABAs, word for word.** Five bodies (`utility_case_followup_v1`,
   `utility_case_question_v1`, `utility_case_notice_v2`,
   `utility_case_pending_v1`, `utility_proposal_update_v1`) exist,
   unchanged, on both the chat WABA and the research WABA, confirming that
   submitting per-WABA (section 6) is standard practice here, not a
   hypothesis.

8. **The currency exception stays isolated to one template.** `utility_billing_reminder_v1`
   is the only one of the 105 with a literal `$ {{n}}` in the fixed text,
   on two different WABAs, always `APPROVED`/`UTILITY`. No new template in
   the catalog (including the money-free sibling billing templates) repeats
   that pattern, which is the expected behavior: a historical exception is
   not a model to copy.
