# Attio dedup, logging, and stage

Workspace verified September 2, 2026: **Chanty**, austin@chanty.com, admin.

Two objects only, `people` and `companies`. **No Deals object and no pipeline list.** One
list exists, `customer_success`, on companies, and this agent does not write to it.

Both outreach lists live on the same People records. Agent 1 writes automated outreach,
this agent writes what Austin drafts and sends by hand. Same records, different method, so
`who_contacted` has to be written every time or the two become indistinguishable.

Call `list-attribute-definitions` on `people` before the first write of a session. Every
slug and option title below was read from the live workspace, and the live read always wins
over anything written here.

## The two tracking fields, verified live

Both exist on `people` as of September 2, 2026. Austin built them, and the shapes below are
what is actually in the workspace, not what was originally specced. Read them from
`list-attribute-definitions` at the start of a session anyway. Do not hardcode.

### `stage` (title "Stage", type **status**, writable)

Not a select. Attio's `status` type, which means it behaves as a real pipeline stage.
Write it by passing the option title exactly: `{"stage": "Contacted"}`.

Eleven options, in workspace order. **The casing is not what you would guess, so copy it:**

```
1  Not Contacted
2  Contacted
3  Follow-Up Sent      <- capital U
4  Replied
5  Meeting Booked
6  Opportunity
7  Contracting
8  WON-Closed          <- not "Closed Won"
9  LOST-Closed         <- not "Closed Lost"
10 Not a Fit
11 Follow Up Needed    <- no hyphen, unlike option 3
```

"Follow-Up Sent" and "Follow Up Needed" differ by one hyphen and mean opposite things.
Passing the wrong string fails or lands in the wrong stage, so read the option list rather
than typing from memory.

### `who_contacted` (title "Who Contacted", type **text**, writable)

Free text, so nothing stops it drifting into "austin", "Austin H" and "the agent" inside a
month. It needs a convention, and this is it. Write exactly one of:

```
Austin (manual)
Agent 1 (automated)
Inbound
```

This agent always writes `Austin (manual)`. Never a variant, never lowercase.

If the field already holds a different one of those values, **flag it and do not
overwrite**. A record that says `Agent 1 (automated)` and is about to get a hand-written
email from Austin is exactly the collision worth telling him about before he sends.

## Stage lives on People, and that has consequences

There is still no Deals object, so one person carries one stage. A contact who buys twice,
changes companies, or gets worked for two different products has nowhere to put the second
pipeline position. That is fine at current volume. It stops being fine when Austin needs
two open opportunities against one human, and the fix at that point is a Deals object, not
a workaround here.

## Attribute slugs on `people`

| Field | Slug | Type | Notes |
|---|---|---|---|
| Name | `name` | personal-name | Format is `"Last, First"`, or an object with `first_name`, `last_name` and `full_name` all present. Getting this backwards is the easiest mistake to make here. |
| Email | `email_addresses` | email-address, multiselect, **unique** | Always an array. Unique means a create with an existing address fails, so use `upsert-record`. |
| Job title | `job_title` | text | |
| Company | `company` | record-reference to companies | Pass a domain for the simple format, or `{"target_object": "companies", "target_record_id": "<uuid>"}`. |
| LinkedIn | `linkedin` | text | |
| Description | `description` | text | Where the contact source goes when there is no better field. |
| Phone | `phone_numbers` | phone-number, multiselect | |
| Stage | `stage` | status | Eleven options, see above. Write the title exactly. |
| Who Contacted | `who_contacted` | text | Controlled vocabulary, see above. |
| Last interaction | `last_interaction` | interaction | **Read only.** Useful for dedup context. |
| Next calendar interaction | `next_calendar_interaction` | interaction | **Read only.** This is how a booked meeting shows up, see the status table. |

## Dedup, run before anything is created

Use `search-records` on `people`, then confirm with `get-records-by-ids`. Order:

1. **Exact match on `email_addresses`.** Confident. Use that record.
2. **No email, but `name` and `company` both match.** Confident. Use that record.
3. **Name matches, company does not. Or company matches, name does not.** Uncertain.
4. **More than one record matches.** Uncertain, always, even if one looks obviously right.
5. **No match.** New person. Nothing is created yet, see below.

On uncertain: stop for that one target, show Austin both records with enough to tell them
apart (job title, company, `last_interaction`, `stage`, `who_contacted`), and ask. Do not merge, do
not create a second record, do not pick the newer one. Keep drafting the other targets
while that one waits.

`merge-records` exists in the connector. Never call it. A wrong merge cannot be undone.

## When records get created

At logging time, after Austin confirms a send. Not at draft time. A batch of six drafts
where he sends two should leave two records behind, not six.

Reading an existing record early is still the right move, it just does not imply writing
one.

## What gets written on a confirmed send

**Person record**, via `upsert-record` on `people`, matched on `email_addresses`.

- New record: name, email, job title, company, LinkedIn if known, `stage`, `who_contacted`,
  and the contact source in `description` (Personal list, referral and who from, conference
  and which one).
- Existing record: fill empty fields only. Never overwrite a populated field with something
  a tool produced. If a tool disagrees with what is there, put it in a note and leave the
  field alone.

**The email itself.** Check the record's existing notes and emails first, with
`search-emails-by-metadata` or `search-notes-by-metadata`. Attio's native Gmail sync may
have already caught it, and two copies of one email on a timeline makes the timeline
useless. If there is no synced copy, attach a note with `create-note`:

```
Title: Outreach sent YYYY-MM-DD

Angle: <one line>
Method: manual send by Austin
Subject: <subject>

<body>
```

**Stage and Who Contacted.** Per the ladder below. `who_contacted` is written on every
send, `stage` per the table.

## Stage ladder

| Stage | Set automatically |
|---|---|
| Not Contacted | Yes, on create when nothing has gone out |
| Contacted | Yes, on a confirmed cold first touch |
| Follow-Up Sent | Yes, on a confirmed follow-up |
| Follow Up Needed | Yes, as a queue flag. See below. |
| Replied | Yes, when Austin says they replied |
| Meeting Booked | Yes, when Austin says a meeting is booked, or when `next_calendar_interaction` on the record shows a future meeting. Nothing else owns this field now that Calendly is out of the stack. |
| Opportunity | No. Flag. That is a qualification call. |
| Contracting | Never. Flag for confirmation. |
| WON-Closed, LOST-Closed, Not a Fit | Never. Flag for confirmation. |

### How "Follow Up Needed" is used

Read it as a work queue, not a pipeline position. It sits at order 11, after the closed
stages, which is where a queue flag belongs rather than where a stage would.

- **Set it** when a sent touch has gone unanswered past the follow-up window and no
  follow-up has gone out yet.
- **Clear it** to `Follow-Up Sent` when the follow-up goes out, or to `Replied` if they
  answer first.
- **Never set it** over `Meeting Booked` or anything later without asking. Someone with a
  meeting on the calendar does not need chasing.
- Ask this agent who needs a follow-up and it filters `people` on this stage. That is the
  point of the flag.

This reading was inferred from the option name and its position. If Austin means something
else by it, this section is the thing to correct.

### Rules on top of the table

- The stage reflects what the message says, not the best case. "Following up after our call"
  means at least Replied. "Sent it" on a first touch means Contacted and nothing more.
- Never advance a stage on the strength of an open or a click. Mailtrack under-reports and
  over-reports on Apple Mail, so a pixel is not evidence of anything.
- Never move a stage backward. If the record is further along than the message implies,
  flag it. That usually means dedup matched the wrong person.
- Ambiguous stage, ask in one line. Guessing upward pollutes the pipeline.
- Agent 1 writes the same field on the same records. Both agents follow this table, or the
  pipeline stops meaning anything.

## Never

- Never call `merge-records` or delete a record.
- Never write a draft as activity. Only confirmed sends.
- Never create a duplicate to get around an uncertain match.
- Never write a personal note about someone that Austin did not say and that is not
  publicly sourced.
- Never write to the `customer_success` list. It belongs to a different workflow.

## Also log locally

Append the row to `../state/send-log.md` on every confirmed send. That file is the record
when Attio is unreachable, and it is what makes follow-up timing possible.
