# Attio dedup, logging, and status

Same dedup logic as Agent 1. Read the workspace's real attribute definitions before the
first write in a session. The status names below are the intent, not guaranteed to be the
literal option labels in the workspace.

## Dedup, run before anything is created

Checked in this order, for every target:

1. **Exact email match on a Person record.** Confident. Use that record.
2. **No email, but full name and company both match.** Confident. Use that record.
3. **Name matches, company does not. Or company matches, name does not.** Uncertain.
4. **More than one record matches.** Uncertain, always, even if one looks obviously right.
5. **No match.** New person. Nothing is created yet, see below.

On uncertain: stop for that one target, show Austin both records with enough to tell them
apart (title, company, last activity, owner), and ask. Do not merge, do not create a
second record, do not pick the newer one. Keep drafting the other targets while that one
waits.

## When records get created

At logging time, after Austin confirms a send. Not at draft time. A batch of six drafts
where he sends two should leave two records behind, not six.

Reading an existing record early is still the right move, it just does not imply writing
one.

## What gets written on a confirmed send

**Person record**
- Create with name, email, title, company, and the source of the contact (Personal list,
  referral and who from, conference and which one).
- On an existing record, fill empty fields only. Never overwrite a populated field with
  something a tool produced. If a tool disagrees with what is there, add a note saying so
  and leave the field alone.

**The email itself**
- Check the record for an already-synced copy first. Attio's native Gmail sync may have
  caught it, and duplicating the body twice on one record makes the timeline useless.
- If there is no synced copy, attach a note:

```
Outreach sent YYYY-MM-DD via Gmail
Angle: <one line>
Subject: <subject>

<body>
```

**Status.** Set from what Austin's message says, per the table below.

## Status ladder

| Stage | Set automatically |
|---|---|
| Not Contacted | Yes, on create when nothing has gone out |
| Contacted | Yes, on a confirmed cold first touch |
| Follow-up sent | Yes |
| Replied or Engaged | Yes, when Austin says they replied or a call happened |
| Meeting Booked | No by default. The Calendly to Attio Zapier owns this field. Set it only if Austin confirms that automation is not live, and say in the log that it was set by hand. |
| Contracting or Negotiation | Never. Flag for confirmation. |
| Closed Won, Closed Lost, or any terminal stage | Never. Flag for confirmation. |

Rules on top of the table:

- The status reflects what the message says, not the best case. "Following up after our
  call" means at least Engaged. "Sent it" on a first touch means Contacted and nothing
  more.
- Never advance a stage on the strength of an open or a click. Mailtrack under-reports and
  over-reports on Apple Mail, so a pixel is not evidence of anything.
- Never move a stage backward. If the record is further along than the message implies,
  flag it, that usually means the dedup matched the wrong person.
- Ambiguous stage, ask in one line. Guessing upward pollutes the pipeline.

## Never

- Never merge or delete a record.
- Never write a draft as activity. Only confirmed sends.
- Never create a duplicate to get around an uncertain match.
- Never write a personal note about someone that Austin did not say and that is not
  publicly sourced.

## Also log locally

Append the row to `../state/send-log.md` on every confirmed send. That file is what makes
follow-up timing possible when Attio is unreachable or not yet connected.
