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

Current level: **0** (research only). Default posture is draft, don't send.

Tier A organizations stay human-approved at every level.

## Email compliance

Sending is blocked until a human fills in the physical address, names the sending
infrastructure, and records that legal review happened. Those three fields are
null in `policy.json` right now, and the send gate fails closed on them.

## State transitions

States change through explicit validated events, never because a model decided a
record "feels" qualified. See `scripts/eco/state_machine.py`.
