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
Persona: Ops or IT manager
Angle: their Q2 post about running the team across Slack and Asana - https://example.com/post
Stage on send: Contacted
Email: jane@acme.com (given)

Subject: Slack and Asana overlap

Jane,

<body>

Austin

Notes: 94 words. The post is 6 weeks old, still current. Team size unverified, the draft
avoids it. No credits spent.
```

Field notes:

- **Attio** says what dedup found, and anything on the record that changed the draft.
  Uncertain matches say so here and the draft is held.
- **Who Contacted on record** flags it when Agent 1 is already working this person.
- **Angle** carries the source URL every time, even though the URL does not appear in the
  email.
- **Stage on send** is what will be written if Austin confirms it went out. Flagged stages
  say `flagged, needs your confirmation` instead.
- **Email** says where the address came from: given, on the record, revealed by Apollo, or
  blank.
- **Notes** carries word count, anything unverified, anything left out for lack of data,
  and any credit spent.

## Held targets

A target waiting on an uncertain Attio match or an unapproved credit gets a short block
saying what it is waiting for, not a draft. Do not draft around a blocked email address
and then present it as ready.

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
