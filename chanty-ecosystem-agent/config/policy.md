# Central Policy

`config/policy.json` is the machine-readable source of truth. This file is the
human-readable mirror. If the two ever disagree, the JSON wins and someone needs to
fix this file. `tests/test_policy_consistency.py` checks the parts that matter.

No agent may write to either file. A human edits policy. That is the whole point of it.

## Pricing

Chanty is **$3 per seat**. That is a hard commercial fact.

The agent does not invent, offer, hint at, or "explore" any of the following:
discounts, member pricing, promotional pricing, free accounts, extended trials,
commissions, referral percentages, revenue share, or exclusivity.

The agent may recognise that a partnership economics conversation is warranted and
escalate it to a human. It may not conduct that conversation.

## Contact data

Public sources only. No enrichment. No guessing. No silent fallback.

The system must never use an enrichment platform, contact database, data broker or
paid contact service to find a person's email or phone. This holds even though
Apollo, ZoomInfo and Clay are connected in this environment. Connected is not
permitted.

If the right person is found but their email is not public, the record is marked
`email_status = not_publicly_found`, state moves to `EMAIL_NOT_PUBLIC`, and the
system asks the user. Permission is per-contact unless the user says otherwise in
writing.

Never construct an address from a pattern. Never verify a constructed address.
Never substitute an easier-to-find person for the right person.

## Offers

Approved offers, and only these:

1. Educational workshop
2. Member resource
3. Member benefit (Chanty at $3/seat, not framed as a discount)
4. Partner / referral program (economics require human approval)
5. Co-branded content
6. Event participation
7. Discovery conversation (the fallback when nothing else fits)

## Outreach

Four touches maximum: day 0, day 4, day 10, day 21. Then nurture.

No restart without a new qualifying signal, and not within 90 days.

Any meaningful reply stops automation immediately.

## Escalation

Always human: national partnerships, major associations, franchises, major MSP
opportunities, pricing, commissions, referral economics, contracts, exclusivity,
data sharing, security, compliance, HIPAA, legal, media, public endorsement,
complaints, and anything unusual.

## Autonomy

Current level: **2**. Research, contact discovery, and drafts written into
Gmail. Nothing sends itself.

Level 3 turns on automated outreach, and it does not happen until Austin has
read the first 20 drafts in Gmail and says to turn it on. The agent never raises
its own level. `autonomous_send_enabled_categories` is empty and stays empty
until he names the categories.

Tier A and strategic organizations stay human-approved at every level, including
after the promotion.

## How mail actually goes out

Sending mode is `manual_gmail_draft`. The agent writes a draft into Austin's
Gmail. He reads it and sends it himself, one to one, from his own mailbox.

That mode is why two bulk-mail requirements are switched off: there is no postal
address block and no unsubscribe link. Both are requirements for bulk commercial
mail and neither fits an individual message a person sends by hand. Legal
reviewed this on 2026-09-08.

What does not switch off: suppression. An opt-out arrives as a reply and is
written to suppression the same day, and a suppressed contact can never reach a
draft.

If the sending mode ever changes to a bulk platform, set
`physical_address_required` and `opt_out_link_required` back to true in
`policy.json`. The gate reads those flags, so it tightens on its own, but the
change deserves another legal look.

## Live sessions are remote

We join workshops, panels and speaking slots by video. No travel.

The first message says so. Not the follow-up, not the call after they say yes.
An organization putting us on an agenda is agreeing to something specific and
they should know what it is while they are deciding.

Applies to the workshop and event participation offers. It does not apply to
written resources or co-branded content, which have no delivery format to
disclose.

## Email format

Plain text. Gmail supplies the signature and the formatting, so the draft
supplies neither.

No sign-off. No "Best", no "Thanks", no name, no title, no links block. The
message ends on its last real sentence.

No markdown, no HTML, no bullets, no bold, no headings. The Gmail draft is
created with `body` only and never `htmlBody`, so plain text is enforced at the
API call rather than left to a reminder.

## State transitions

States change through explicit validated events, never because a model decided a
record "feels" qualified. See `scripts/eco/state_machine.py`.
