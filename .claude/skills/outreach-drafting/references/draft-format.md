# How drafts come back

One block per target, in the order Austin listed them. Plain text, no preamble about the
process, no summary of the workflow that just ran.

## Batch header, when there are two or more targets

```
6 targets. 2 drafted, 3 waiting on approvals below, 1 flagged.
2 people at acme.com, different angles on each.
Sends today: 6 in this batch, plus whatever has already gone out.
```

Drop the header for a single target.

## Per target

```
### 1. Jane Doe, Head of Ops, Acme

Attio: existing record, last touched 2026-04-02 by Austin. No reply on that thread.
Who Contacted on record: empty
Persona: ops-manager
Angle: company-trigger, their Q2 post on onboarding four new sites - https://example.com/post
Email: jane@acme.com, published on their team page, verified
Time suggested: Thu Sep 10, 10:00 CT. Austin's calendar is clear.
On send: stage Contacted, who_contacted Austin (manual), company touch rolled up

Subject: onboarding four sites

Jane,

<body>

Austin

Notes: 84 words. Post is 6 weeks old, still current. No competitor named. No credits spent.
```

Field notes:

- **Attio** says what dedup found, and anything on the record that changed the draft.
  Uncertain matches say so here and the draft is held.
- **Who Contacted on record** flags it when Agent 1 is already working this person.
- **Persona** is a tag from `.claude/gtm/attio-schema.md`, not a free-text description.
- **Angle** is one of `authored-content`, `engaged-content`, `background`,
  `company-trigger` or `generic`, and carries a source URL every time even though the URL
  does not appear in the email.
- **Email** says where the address came from and whether it is verified. An assembled
  address or a catch-all domain is not verified and the target is held, not drafted.
- **Time suggested** names the slot in the CTA and confirms Austin's calendar is clear for
  it. The contract requires a specific time, so this is not optional.
- **On send** is what gets written to both records if Austin confirms. Flagged stages say
  `flagged, needs your confirmation` instead.
- **Notes** carries word count against the under-90 first-touch target, anything unverified,
  anything left out for lack of data, and any credit spent.

## Held targets

A target waiting on an uncertain Attio match, an unapproved credit, or an unverified
address gets a short block saying what it is waiting for, not a draft. Do not draft around
a blocked address and then present it as ready.

## Closing line

End the batch with one line, not a paragraph:

```
Reply with edits, or tell me which ones you sent and I'll log them.
```

## Gmail drafts

Only when Austin asks. Push the exact text shown, no reformatting, no signature block he
did not ask for. Say which ones landed. Creating a draft is not sending, and the send stays
his.

## Saving a batch

Only when Austin asks to keep one. Write it to `../state/drafts/YYYY-MM-DD-<label>.md` with
the same blocks. Sent drafts are recorded in `../state/send-log.md` either way.
