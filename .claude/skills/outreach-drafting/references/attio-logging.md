# Attio dedup, logging, and status

Workspace verified September 2, 2026: **Chanty**, austin@chanty.com, admin.

Two objects only, `people` and `companies`. **No Deals object and no pipeline list.** One
list exists, `customer_success`, on companies, and this agent does not write to it.

Both outreach lists live on the same People records. Agent 1 writes automated outreach,
this agent writes what Austin drafts and sends by hand. Same records, different method, so
the method has to be recorded or the two become indistinguishable.

Call `list-attribute-definitions` on `people` before the first write of a session. The
slugs below were read from the live workspace, but the Status column is new and its real
slug wins over anything hardcoded here.

## Required setup, one time, in the Attio UI

The connector cannot create attributes, so Austin adds these two on the People object.
Until the first one exists, the agent logs the send and reports that the status could not
be written. It does not invent a place to put it.

**1. Status** (type: Select, single). Options in this order:

```
Not Contacted
Contacted
Follow-up Sent
Replied
Meeting Booked
Opportunity
Contracting
Closed Won
Closed Lost
Not a Fit
```

**2. Outreach Method** (type: Select, single). Options:

```
Agent (automated)
Manual (Austin)
Inbound
```

This agent always writes `Manual (Austin)`. If a record already says
`Agent (automated)` and Austin is now emailing them by hand, flag it rather than
overwriting. Two systems touching one person is worth him knowing about.

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
apart (job title, company, `last_interaction`, Outreach Method), and ask. Do not merge, do
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

- New record: name, email, job title, company, LinkedIn if known, Status, Outreach Method,
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

**Status.** Per the table below.

## Status ladder

| Stage | Set automatically |
|---|---|
| Not Contacted | Yes, on create when nothing has gone out |
| Contacted | Yes, on a confirmed cold first touch |
| Follow-up Sent | Yes |
| Replied | Yes, when Austin says they replied |
| Meeting Booked | Yes, when Austin says a meeting is booked, or when `next_calendar_interaction` on the record shows a future meeting. Nothing else owns this field now that Calendly is out of the stack. |
| Opportunity | No. Flag. That is a qualification call. |
| Contracting | Never. Flag for confirmation. |
| Closed Won, Closed Lost, Not a Fit | Never. Flag for confirmation. |

Rules on top of the table:

- The status reflects what the message says, not the best case. "Following up after our
  call" means at least Replied. "Sent it" on a first touch means Contacted and nothing more.
- Never advance a stage on the strength of an open or a click. Mailtrack under-reports and
  over-reports on Apple Mail, so a pixel is not evidence of anything.
- Never move a stage backward. If the record is further along than the message implies,
  flag it. That usually means dedup matched the wrong person.
- Ambiguous stage, ask in one line. Guessing upward pollutes the pipeline.

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
