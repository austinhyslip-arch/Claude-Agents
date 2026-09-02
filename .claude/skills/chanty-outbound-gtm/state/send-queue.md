# Send queue

Staged drafts waiting on Austin. Nothing here has been sent. Nothing here sends itself.

Newest block at the top. Format is in `references/send-policy.md`.

Status values:
- `Ready`: every box on the send-eligibility gate is checked
- `Held`: something failed the gate, reason written out on the block

When an email is sent, move its block into `state/run-log.md` under that day's entry, set the
person to `Sent` and roll the touch up to the company, per `.claude/gtm/crm-sync.md`. Record
any edit Austin made before sending.

---

## Held :: 2026-09-02 :: Alayna Brent, Chord Specialty Dental Partners

- Attio person: b2874814-0915-4b23-9b74-78a13a3586b7
- Attio company: 090d1bb7-6723-48f2-9d0d-24f9fada1269
- Email: none found (unverified, no address published)
- Phone: (484) 787-2900, company main line, medium confidence
- Stage: Not Contacted
- Persona: ops-manager | Score: 11 | List: Healthcare / CT / Personal
- Category: Outbound | Bridge: none | Premise: Multi-Persona
- Signal: hiring, Regional Operations Manager over eight clinics, sourced 2026-09-02
- Angle: company-trigger
- Proposed slot: 2026-09-08, 10:00 America/Chicago (Austin's calendar is clear)
- **Hold reason: no verified email address. Named on the company leadership page, no
  address published anywhere findable. Goes to the gap batch.**
- Second hold: this is a Personal list account, so Austin sends it, not the agent. Draft is
  here for him to use or bin.

Subject: eight clinics, one manager

```
Alayna,

I'm Austin, the co-founder of Chanty. We built it because the big internal
communications platforms aren't built for healthcare clinics who need a
simple, easy to use platform that's affordable.

You're hiring a regional ops manager over eight clinics, and most of the
people they'll need to reach aren't sitting at a computer.

Our base plan: no complex builds, no weeks-long integration, BAA signed,
HIPAA compliant, and affordable.

Any chance you have 15 minutes Tuesday the 8th at 10am your time?

Austin
```

---

## Held :: 2026-09-02 :: Kelly Cashman, Performance Therapy Institute

- Attio person: 61796639-dc1c-4f9b-94af-ef53b3270fed
- Attio company: 600a6d29-231e-4ef3-94cc-d81c32883690
- Email: **none usable.** Apollo returned kelly@premierrt.com, flagged extrapolated at 0.6
  confidence, on a catch-all domain, matched to a company in Bangor Maine. Rejected.
- Phone: (615) 465-6810, main line, high confidence
- LinkedIn: linkedin.com/in/kelly-cashman-56530b200
- Title: Front Office Manager, corrected from Office Manager
- Stage: Not Contacted
- Persona: ops-manager | Score: 5 | List: Healthcare / CT / Agent
- Category: Outbound | Bridge: none | Premise: typical cold outbound
- Angle: background, four offices under one front desk
- Proposed slot: 2026-09-09, 09:15 America/Chicago
- **Hold reason: no verified address. Phone is the live route to this account.**

Subject: four offices, one thread

```
Kelly,

I'm Austin, the co-founder of Chanty. We built it because the big internal
communications platforms aren't built for healthcare clinics who need a
simple, easy to use platform that's affordable.

You're running front desk across four offices, so a schedule change has
four places to go missing.

Our base plan: no complex builds, no weeks-long integration, BAA signed,
HIPAA compliant, and affordable.

Any chance you have 15 minutes Wednesday the 9th at 9:15am?

Austin
```

---

## Phone as the fallback channel

Both drafts are held on the same thing, a missing email address. Both accounts now have a
working phone number, which `never-guess-an-email` treats as a real answer rather than a
consolation prize: where there is no address, route to a channel that exists instead of
inventing one.

Two of the six main lines are worth calling. Performance Therapy Institute is a four-office
practice with a named office manager, so a call reaches a person. Chord's line is worth one
attempt to confirm it reaches Nashville at all.

Three are not. Nashville Healthcare Center's number is a patient appointments queue, so
calling it puts a sales call ahead of patients. Fast Pace Health is a corporate switchboard
at a 300-site operator. Family Practice Associates is blocked on the ownership question.

The agent does not call anyone. This is a note for Austin about which numbers are worth his
time, and the reasoning is on each company's `GTM account` note in Attio.
