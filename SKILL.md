---
name: whatsapp-utility-templates
description: Create, review, submit, or track a WhatsApp Cloud API (Meta) message template that needs UTILITY approval, with slots filled in by your own system, for any business messaging customers outside the 24 hour window.
---

# WhatsApp utility templates (Meta)

Outside the 24 hour window, only a template approved by Meta can open a
conversation with a lead or customer on WhatsApp. This skill teaches you to
create, submit, track, and use that template inside the UTILITY category,
the only category this skill covers. The MARKETING category costs more,
requires opt-in that most support or sales funnels never collect, and a
badly designed UTILITY template can get reclassified after approval and
drag the whole WABA's reputation down with it.

**The rule that never bends: UTILITY only, and proven before you submit.**
A template that gets approved and later falls to MARKETING is lost: it
doesn't come back, the name is burned, and the WABA carries that history
forward. That's why no definition goes to Meta without passing
`scripts/check.py`, calibrated against a measured corpus of 16 real
templates (16 of 16 verdicts match, reproduce it with
`python3 scripts/check.py --corpus`). `scripts/submit.py` calls the checker
itself and has no flag to skip it.

The doctrine here comes from a real case study: a vehicle protection company
selling to independent truck drivers, measured across 33 real templates on
one WABA (19 approved as UTILITY, 14 approved as MARKETING), plus a live
production incident where four templates got approved and reclassified
within 25 minutes of each other. All company names, agent names, customer
names, protocol numbers, and phone numbers here are placeholders; the
wording, timings, and verdicts are real.

## 1. The anchor test: what Meta accepts as utility

Meta defines UTILITY as a non-promotional message that serves the reader on
something they already started: a request, an order, a case in progress.
The practical test, before writing any template, is one question:

**Does the message talk about a case, order, or request the reader already has?**

If yes, the path is UTILITY. If the message exists to make the reader
consider something they didn't ask for (a deal, a slot, an advantage, an
invitation to learn about the product), it's MARKETING, and this skill
doesn't cover that path.

The measured corpus shows the contrast side by side. Approved UTILITY
templates open with "about your case", "as requested", "update on your
ticket", "the quote you asked for". Approved MARKETING templates open with
"over 42,000 members have already chosen us", "special terms", "only a few
spots left", "take advantage of our Black Friday deal". The difference
isn't tone, it's referent: one talks about something that already exists
for that specific person, the other invites them to start something new.

Rule of thumb: if the sentence would read the same for anyone who never
talked to you before, it's marketing in disguise. If the sentence only
makes sense because that person already asked, already has a case number,
already got a proposal, it's real utility.

## 2. The anatomy that passes

Approved UTILITY templates in the case study share a five-part structure.
Following it raises the odds of approval and, more importantly, is what
makes the template reusable: the same text serves many situations, because
the specific content enters through the slot.

1. **Open with a name, and who's writing.** "Hello, {{1}}." or "Hi, {{1}}!"
   followed, when the sender needs to identify themselves, by who's writing:
   "This is {{2}}, from [company]."
2. **The anchor.** A short phrase that locates the case: "about your case",
   "about your proposal for plate {{2}}", "update on your case ticket".
3. **The wide slot.** A `{{n}}` that receives the full sentence, assembled
   by your own side, with the specific content for that case. This is where
   the template's intelligence lives: the same model serves a quote, a
   missing document, a plate question, without needing one template per
   topic.
4. **A closer that asks for a reply.** "Just reply here.", "Reply here and
   I'll walk you through it.", "Any questions, just reply."
5. **Up to two short quick-reply buttons.** "Continue" / "Not now", "See it"
   / "Not now", "Sort it now" / "Later". Label up to 20 characters (Meta
   rejects anything longer). See `references/button-pairs.md` for the full
   accept/decline contract.

What stays out, always: emoji in the body, a text `HEADER`, and any money
value. No approved UTILITY template in the corpus used an emoji or a text
header in the main body. **An image or video header is different: it can
pass, but only inside the media notice family, and only with an
acknowledgement button** (section 8 covers the rule and the measurement
behind it). A currency value shows up only in one old billing template,
documented as a historical exception, not a model to copy: price stays out
of the template, always inside the live conversation, where it can be
verified against a real calculation.

Example of a body that passes:

```
Hi, {{1}}! {{2}}, from [company], here.

About your case: {{3}}

Just reply here.
```

Buttons: `Continue` | `Not now`

## 3. Parameter rules: what Meta requires, and what you should require on top

### What Meta requires (blocks the submission if it doesn't match)

- **Every slot needs an example.** Every `{{n}}` in the body needs an
  example value in `example.body_text`, in the same order. A template
  missing an example for any parameter is rejected.
- **Sequential numbering, no gaps.** Parameters start at `{{1}}` and go up
  one at a time. `{{1}}` and `{{3}}` with no `{{2}}` gets rejected.
- **No line break, tab, or four consecutive spaces inside the parameter
  value itself.** This applies to the value that fills the slot at send
  time, not the template's fixed text (which can have paragraphs).
- **A variable can't sit right next to another, or alone at the edge of the
  text.** `{{1}}{{2}}` with nothing between them, or a body that starts or
  ends raw on `{{n}}`, reads to Meta as "a message that's just a filled-in
  field" and gets rejected.
- **Button label up to 20 characters.** Above that, rejected.
- **At most one URL button per template**, and if the URL has a variable,
  a suffix example is required.

### What you should require on top, inside the free slot (the wide `{{n}}` from section 2)

Meta doesn't see the free slot's real content at submission time, because
at that point it's still just example text. It sees the real content later,
once the template is approved and in use: user complaints and quality drops
reclassify the whole template, and one reclassification drags the WABA down
with it. That's why the free slot carries five checks of your own, testable
in code before any real send:

1. **One sentence, up to 140 characters, ending in a period or a question
   mark.**
2. **No currency value, no percentage, no monthly payment amount.** Price
   never leaves a template.
3. **No promotional word**: discount, deal, offer, special terms, last
   spot, today only, don't miss out. This is the line that separates
   utility from marketing in Meta's later reading, and it's the same list
   `scripts/check.py` uses to reject before submission (`SALES_WORDS`).
4. **No jargon from your own do-not-say list**, whatever internal terms
   your product avoids saying to a customer directly.
5. **The sentence talks about that specific reader's case**: a quote, a
   plate, a vehicle, a document, a call. A sentence that would serve any
   reader equally is a sign it belongs in a template without a free slot
   (a plain batch message), not this one.

Examples that pass: "your quote is ready and I can walk you through it in
two minutes.", "I set aside the material you asked about trailer coverage.",
"we're missing the year of the truck to finish the calculation."

Examples that don't pass: "we have a special deal just this week." (promo),
"it came out to $380 a month." (price), "we're the best in the market."
(generic and promotional).

A batch template (the same message going out to a whole list) doesn't carry
a free slot on purpose: in a batch send nobody models a sentence per reader,
and a free slot in a batch template is exactly the hole where promotional
text sneaks in without anyone noticing.

## 4. Naming, and what to do when Meta rejects

Name your template `<finality>_v<n>`, always lowercase snake_case, starting
with a letter, `_v1` on the first revision and `_v2`, `_v3` on the ones
after. Whatever system stores your template catalog should enforce this at
write time, so a template can approve on Meta and still be useless because
it never enters your catalog under the name your code expects.

When a template is rejected or reclassified, the rule is firm: **never
resend the same text hoping the verdict changes.** The right move is to bump
the revision, `_v2`, with the text rewritten to tie more tightly to that
specific reader's case, following the anchor test in section 1. A rejected
revision stays as history, it doesn't get deleted or resubmitted unchanged.

## 5. How to submit and track

### Submission contract

Every POST to `/{waba}/message_templates` goes out with:

```json
{
  "name": "utility_case_followup_v1",
  "language": "pt_BR",
  "category": "UTILITY",
  "allow_category_change": false,
  "components": [...]
}
```

`allow_category_change: false` is deliberate, not an oversight. If Meta
wants to classify it as MARKETING, it rejects the submission instead of
silently accepting it; then the text gets rewritten to remove whatever read
as promotional, instead of accepting the category change and inheriting
marketing's cost and opt-in rules without having designed for them.

### Reading the response

A successful submission returns `id` (a numeric string), `status` (usually
`PENDING` at first), and `category`. Save the `id`: it identifies the
template in later lookups, not the name (the name can repeat across
different WABAs).

### Tracking until approval

A text UTILITY template usually approves in minutes, but can take hours.
Poll with `GET /{waba}/message_templates?name=<name>&fields=id,name,language,status,category,components`
until `status` becomes `APPROVED`. Don't poll aggressively: a check every
few minutes is enough, and it's reasonable to cache an approved status for
an hour at send time, since an approved template's status rarely flips
between one conversation turn and the next.

### On REJECTED

The response carries `rejected_reason`. Read the reason, adjust the text
following sections 1 through 3, and resubmit as `_v2` (never resend the
same body). If the rejection is about category (Meta wanted MARKETING), the
body probably has a promotional smell that slipped through: check it
against the `SALES_WORDS` list in section 3 before trying again.

### Measured incident: approved and reclassified within the same minute

Four templates were submitted as UTILITY on the same WABA, all with
`allow_category_change: false`. Within 25 minutes, Meta approved two of them
and, in the same act, flipped the category to MARKETING
(`previous_category: UTILITY`). A third became MARKETING while still
pending, and a fourth held for ten minutes before falling. All four from
that first batch ended up as MARKETING. What separated the ones that fell
from the ones that, in the next batch, held:

- Fell last: "You asked for a quote for your truck and it sat pending on
  our side. It's ready now. Reply here and I'll send it over." No free slot
  and an admission of delay, but "quote", "truck", and "send it over" in
  the fixed text, plus a button reading "Send it over".
- Held: an agent introduction ("This is {{2}}, an advisor with us") followed
  by "The quote you asked for is ready" with a button "See it"; and the
  Swiss-army version "About your case: {{3}}" whose slot example read "your
  quote is ready and I can walk you through it in two minutes." Meta reads
  the slot's example as part of the text, and an example that sounds like a
  sales pitch takes the whole template to MARKETING.

Rules that come out of this: (1) `allow_category_change: false` only holds
at submission time; once approved, Meta can reclassify freely, and the only
defense is a fail-closed check before every send. (2) A free slot's example
needs to be as transactional as the fixed body: "the plate you sent came
back as a passenger car, can you confirm the truck's plate?" passes, "I can
walk you through it in two minutes" doesn't. (3) An invitation to see
something ("Want to see it", "Learn more") pushes toward MARKETING; a
request to continue something already pending ("Send it over", "Continue
this case", "Sort it now") holds in UTILITY. (4) A case or ticket number in
the body is the strongest anchor there is. (5) A reclassified category can
be appealed inside Meta's window through the WhatsApp Manager; that's a
human click, not an API call.

### Counter-proof, measured the same day: the skeleton that passes

Twenty minutes after the reclassified batch, three skeletons modeled after
the templates with the highest real send volume on the same WABA (over
1,500 sends each, 84 to 88 percent read rate) were approved as UTILITY and
never got reclassified. The mold: a minimal body with a name, who's writing,
and "about your open case"; a wide slot whose EXAMPLE reads like a
service-desk note ("I'm reaching out about case ticket #18345, opened on
09/02/2026"); a fixed close with a question ("Do you still {{4}}?" or "Reply
here."); a footer with the company name; buttons "Yes, go ahead" or "Yes,
I do" plus "Not needed". The real message (a quote is ready, a plate didn't
match) only enters when the slot gets filled at send time, and Meta never
reads it at approval time.

Two format rejections Meta returns at submission time, both fixable
without changing the name: `Params Words Ratio Exceeds Limit` (too many
variables for the body's length; four variables in thirteen words got
rejected, in seventeen words it passed) and `INVALID_FORMAT` (body ending in
a variable; close with fixed text after the last slot). A rejected template
can be edited with `POST /{template_id}` with new components and goes back
to PENDING.

### Third measurement the same day: an invitation to continue becomes MARKETING

A template reading "My name is {{2}}, from [company]. {{3}}. Can we
continue this conversation here?" with buttons "We can" / "Not now" was
approved and reclassified to MARKETING within the same hour, with the exact
same service-desk example that held the other four in UTILITY. The
difference was only in the closer: "can we continue" is a re-engagement
invitation, and Meta treats re-engagement as marketing even with a ticket
number anchoring the body. The closer that holds asks about something the
reader already has pending: "Do you still need that callback?", "Do you
still want the numbers here?". Resubmitted as `_v2` with that closer and a
button reading "Yes, I need it": approved as UTILITY in 15 minutes, no
reclassification, as the checker had predicted. Rule: the skeleton's closer
asks about the pending item, never proposes picking the conversation back
up.

### On a later reclassification

An approved template can be reclassified afterward, from a user complaint
or a quality drop. That's why sending should never trust a status saved
long ago: check the live category before every send outside a short cache
window, and refuse to send anything that doesn't come back `APPROVED` +
`UTILITY` (fail-closed). Apply this same principle to any new integration:
never assume "it approved once" still holds.

## 6. How the template gets used after approval

A template is per-WABA. The same template approved on one WABA doesn't
automatically exist on another: submit again on every WABA that will
actually send it.

Two ways to use it, with the same sentence contract:

- **Per reader, in the conversation.** An agent picks the purpose, the fixed
  slots come from data you already have (the reader's name, the agent's
  name), and the free slot gets the sentence the agent writes, following
  the rules in section 3. Before sending, a preview shows the exact filled
  text: that's the moment to catch a bad sentence before it goes out.
- **In bulk, for a batch.** The same sentence goes out identically to every
  reader in the batch, so it has to be true for all of them ("the quote you
  requested sat pending on our side"), never specific to one person's
  vehicle or case.

In both paths, the sentence goes through the same rule engine, so what a
per-reader preview rejects, the batch path also rejects.

Anyone who replies to a template reopens the 24 hour window, and the
conversation continues free from there.

**Fail-closed preflight before every send.** Never trust that "it approved
once" still holds. Run `scripts/preflight.py <name>` before sending: it
checks the live category on Meta (one hour cache, `--fresh` forces a new
check) and only exits 0 with `APPROVED` + `UTILITY`. A network error,
`PAUSED`, `REJECTED`, or a reclassification to `MARKETING` all block,
always, never "let it through to be safe". Run `scripts/preflight.py --all`
on a daily cron to catch a reclassification before anyone tries to send
anything. Full contract in `references/send-preflight.md`.

## 7. Gallery of real examples, paired with the reason

See `references/approved-pattern.md` for the full catalog.

**Pass (approved UTILITY):**

| Template | Body | Why it passes |
|---|---|---|
| `utility_case_followup_v1` | "Hi, {{1}}! About your case: {{2}} Just reply here." | Clear anchor to an existing case, free slot carries the specific content, closes asking for a reply |
| `utility_proposal_update_v1` | "Hello, {{1}}. Update on your proposal for plate {{2}}: {{3}} Any questions, reply here." | Talks about a proposal that already exists, tied to that reader's plate |
| `utility_case_pending_v1` | "Hello, {{1}}. Your case with us has an open item: {{2}}. {{3}} Reply here to resolve it." | A pending item is something the reader already has, not an invitation to start something |

**Don't pass (MARKETING, same sender and product):**

| Template | Body (excerpt) | Why it fails as utility |
|---|---|---|
| `marketing_social_proof_v1` | "Today, over 42,000 members have already chosen us..." | Generic social proof, doesn't talk about that reader's case |
| `marketing_scarcity_v1` | "...only a few spots left with our special terms." | Scarcity and special terms, a classic marketing trigger |
| `marketing_seasonal_v1` | "Riding the Black Friday wave, we have special deals..." | Invitation to start something new, promotional date in the name |

The lesson from the pair: the same subject (vehicle protection) and the
same sender can become UTILITY or MARKETING depending on just one thing,
whether the sentence starts from something the reader already has or
invites them into something they haven't asked for.

## 8. Gallery (105 templates, three WABAs, measured September 2026)

`references/gallery.md` walks through the full gallery from three real
WABAs belonging to the same company, with the body, buttons, and whatever
real send data was available per family. The strongest findings:

- **The button decides category even on a media template.** The six
  "Important notice" templates share an identical body; the one that stayed
  UTILITY uses "Notify me", the five reclassified to MARKETING use "Want to
  know more" or "Talk to an advisor". The button rule is not just for plain
  text: `check.py` (September 15 revision) passes an `IMAGE`/`VIDEO` header
  when the body is clean and every button is an acknowledgement or a
  decline, and still rejects a text header every time.
- **"Block this number" is the single most used button in the whole
  corpus**, present in UTILITY-approved templates on all three WABAs. It
  confirms numerically why `references/button-pairs.md` argues against it:
  the button helps approval, but the click usually is not wired to
  anything, and old revisions carrying it stay live in the catalog.
- **None of the 105 templates carries a `quality_score` other than
  `UNKNOWN`.** There is no way, in this capture, to cross quality score
  against category.
- **Almost half the templates (roughly 57 of 105) are an identical revision
  of a body that already exists**, not new content: three distinct texts
  account for 30 of the 51 templates on the research WABA alone.
- **Only 7 of the 105 templates (6.7%) have any measured send.** Six come
  from the company's own delivery log (Meta's own analytics endpoint
  returns zero for that WABA); the seventh is a template outside this
  company's domain. This gallery describes approved anatomy, not campaign
  performance.
- **Reading more does not mean replying more**: the template with the best
  read rate (92.9%) replies worse (40.5%) than the one with the best reply
  rate (60.1%, 87.6% read).
- **The case and skeleton anatomies replicate word for word between two
  WABAs**, confirming that submitting per-WABA (section 6) is standard
  practice, not a hypothesis.
- **The currency exception stays isolated to one template** across both
  WABAs where it exists, always `APPROVED`/`UTILITY`. No new template
  repeats it.

## 9. Buttons

See `references/button-pairs.md` for the full accept/decline contract: label
rules, the words that sink a button, and the payload contract so a click
routes by index instead of by label text.

## 10. Scripts

`scripts/check.py definition.json` rejects a definition that tends to become
MARKETING (exit 1 with the reasons) and `scripts/check.py --corpus` reruns
the calibration against `references/measured-corpus.json`; change a rule,
and the corpus has to stay 16 of 16. `scripts/submit.py` takes a template
definition JSON (the same format as the submission contract in section 5),
runs the checker, and, if it passes, submits it to a WABA. `scripts/status.py`
looks up a template's current status by name. Both scripts read `META_TOKEN`
(access token) and `META_WABA` (numeric WABA id) from environment
variables, never from a file, and never print the token in any output, log,
or error.

```bash
export META_TOKEN="..."
export META_WABA="<your WABA id>"
python3 scripts/check.py definition.json
python3 scripts/submit.py definition.json
python3 scripts/status.py utility_case_followup_v1
```

Word lists ship in both Portuguese and English, selectable with `--lang pt|en`
(default `pt`): `python3 scripts/check.py definition.json --lang en`. The
measured corpus in `references/measured-corpus.json` is in Portuguese, and
`--corpus` always checks it against the Portuguese list regardless of the
`--lang` flag.

`definition.json` example, in `examples/skeleton-followup.json`:

```json
{
  "name": "utility_case_followup_v1",
  "language": "pt_BR",
  "category": "UTILITY",
  "allow_category_change": false,
  "components": [
    {
      "type": "BODY",
      "text": "Olá, {{1}}, tudo bem? Aqui é {{2}}, da nossa equipe, sobre o seu atendimento em aberto. {{3}}. Você ainda {{4}}?",
      "example": {
        "body_text": [["Jordan", "Jamie", "Estou entrando em contato referente ao protocolo de atendimento 40219 aberto em 02/09/2026", "precisa concluir esse chamado"]]
      }
    },
    { "type": "FOOTER", "text": "Suporte" },
    {
      "type": "BUTTONS",
      "buttons": [
        { "type": "QUICK_REPLY", "text": "Sim, preciso" },
        { "type": "QUICK_REPLY", "text": "Não preciso" }
      ]
    }
  ]
}
```
