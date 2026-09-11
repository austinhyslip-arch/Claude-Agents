# Copy, auto-outreach

The pipeline and every rule in `.claude/gtm/copywriting.md` applies in full. This file only
covers what is specific to sending without a human reading it first.

## Subject lines

Set by Austin on 2026-09-11, replacing the lowercase problem-fragment style that produced
"five sites, one thread". That style is retired.

**Sentence case, plain, no brand.** No "Chanty", no "Chanty.com", no URL. Two to six words,
ten the hard ceiling. No emoji, no brackets except the parenthetical form below, no fake
"Re:", no question mark on a statement.

**Named person gets the product category.** It says what the email is, so the reader
self-selects in a second. At this volume a fast delete from someone who does not care is a
good outcome.

- Internal team chat
- Internal team chat for shift teams
- Team chat that works on a phone
- Internal comms for non-desk staff
- HIPAA team chat (healthcare only)

**Role inbox gets a plain question**, because there the agent genuinely is asking to be
routed and the question is honest rather than a device.

- Who runs internal comms there?
- Who handles team chat for you?
- Right person for internal comms?

**Never** the problem-fragment style, which is the one Austin rejected: "five sites, one
thread", "four offices, one thread", "eight clinics, one manager". Same template with
different nouns, and it reads like one.

**Never** name a competitor in a subject line or a first touch. The value-prop file marks
the Slack and Teams comparisons as safe from the reply onward, not before.

**No two emails in the same batch carry the same subject line.** Rotate through the bank.

## The price test

Austin's instruction: try the price in the subject, judge it on reply rate, keep it if it
works, and **always state the price in the body either way**.

Run it as a straight split, half and half, every day:

| Variant | Subject shape | Example |
|---|---|---|
| A, control | category only | Internal team chat |
| B, price | category plus price | Internal team chat at $3/user |

Rules that keep the result readable:

- Assign the variant randomly per contact, not per batch, per day or per industry.
  Anything else confounds the result with timing or vertical.
- Record the variant on the Attio person record and in `state/sent-log.md`. A test nobody
  can reconstruct later is not a test.
- **Reply rate is the only metric.** There is no tracking pixel and there never will be, so
  opens cannot be measured. Do not report open rates, and do not add a pixel to get them.
- Do not call a winner early. Report the running split in every weekly summary, and say
  plainly that it means nothing yet until each variant has at least 100 sends. At 200 each
  the difference is worth acting on, and even then only if it is large.
- If one variant bounces or draws complaints at a higher rate, that ends the test
  immediately regardless of replies.

## No formatting

Plain text. No markdown, no bold, no bullets, no HTML, no signature block, no images and no
tracking pixel. Gmail handles the rendering. Anything that arrives looking designed reads
as bulk mail.

## Openings by vertical

Both versions are approved and live as of 2026-09-11. The full wording is in
`.claude/gtm/copywriting.md` and it is not paraphrased or shortened here.

**The agent picks the opening from the industry.** That is the only choice it makes.

| Industry | Line 2, the reason | Line 4, the value line |
|---|---|---|
| Healthcare | Austin's healthcare wording | five parts, ends BAA signed, HIPAA compliant, and affordable at $3 a user |
| Plumbing, trucking, distribution, field services, retail, hospitality, anything with a non-desk workforce | the non-desk wording | three parts, ends and affordable at $3 a user |
| Everyone at a desk all day | neither applies | **hold the contact**, do not invent a third version |

The third row matters. An all-desk professional services firm qualifies on headcount and
fits neither reason, and `icp.md` already calls it a weak fit. Holding it is correct, and
writing it a reason that is not true about them is not.

The price goes in the body of every email regardless of which subject variant it carries.
$3 a user is the annual figure. It is $4 billed monthly, so never quote $3 as monthly.

## Hedging, which matters more here

Every claim about how the reader's business runs is an inference. Auto-send means nobody
catches an overconfident sentence before it goes, so hedge harder than a staged draft would.
"more than likely", "probably", "I'd guess". Facts stay flat, inferences get softened. Full
rule in `.claude/gtm/copywriting.md`.

## Role inboxes

Most companies in the 50 to 100 band publish a role inbox and nothing else. Those get a
routing note, not the full email: who Austin is, one hedged line about the company, and a
single ask to be pointed at the right person. No pitch, no value line, no meeting time.
Pitching a shared inbox as though it were the decision maker is how a real company marks
the domain as spam.

That means a good share of what this agent sends is the short version. Worth knowing before
reading reply rates.

## Follow-up

Three business days after the first touch, per `send-policy.md`. Short, no new pitch, no
guilt, no "just bumping this". One line acknowledging the first email, one line that adds
something the first did not say, and the same meeting ask. Under 60 words.

Never re-send the original. Never open with "following up" or "circling back", both already
banned in the shared contract.

## Before any send

Re-read the drafted email against the rejection list in `.claude/gtm/copywriting.md`. No
em-dashes, no banned phrases, no career-history opener, no named competitor, no invented
detail, no claim that is not backed by `.claude/gtm/value-prop.md`. A draft that fails goes
back through stage five, and if it fails twice the contact is held rather than sent.
