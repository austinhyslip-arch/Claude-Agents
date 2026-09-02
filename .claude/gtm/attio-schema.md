# Attio schema

Attio is the system of record. If something happened to a contact and it is not in Attio,
it did not happen.

Workspace: **Chanty**. Connected as austin@chanty.com with admin access. Verified
2026-09-02.

## What the workspace actually has today

Two standard objects, `companies` and `people`. No Deals object. One list,
`Customer Success`, parented to companies. The workspace is effectively empty of records.

**Companies still has no custom attributes. People now has two**, added by Austin in the UI
after the first draft of this file. They are the live tracking fields and both agents write
them. See the next section.

**The Attio MCP connection cannot create attributes.** It creates records, lists, notes,
tasks and comments, and it updates records and list entries. Adding a custom field is a
thing Austin does in the Attio UI, so an agent that wants a new field asks for it rather
than working around it.

So there are two ways to run. Option A still covers everything the two live fields do not.

## The live custom fields on People

Read from the workspace on 2026-09-02, after Austin created them. Re-read with
`list-attribute-definitions` at the start of any session that writes. Never type an option
title from memory.

### `stage` (title "Stage", type **status**, writable)

Attio's `status` type, not a select, so it behaves as a real pipeline stage. Write it by
passing the option title exactly: `{"stage": "Contacted"}`.

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

### `who_contacted` (title "Who Contacted", type **text**, writable)

Free text, so nothing enforces consistency. Both agents write exactly one of:

```
Austin (manual)
Agent 1 (automated)
Inbound
```

Agent 1 writes `Agent 1 (automated)`. Agent 2 writes `Austin (manual)`. Neither overwrites
the other's value silently: a record already carrying the other agent's name gets flagged,
because two systems working one human is worth Austin knowing about before the next send.

Converting this to a single Select with those three options would make drift impossible,
and it is far cheaper now than after the table fills up.

### What these fields do not cover

Nothing on this object holds a **buying power score**, an **employee estimate**, a
**persona tag**, a **sourcing tag**, an **email status** or a **time zone**. Those still
live in the `GTM record` note under Option A.

## Option A, no schema changes, works now

Use the standard fields for what they cover, put everything else in a structured note, and
use lists for the routing.

**Companies, standard fields used as-is**

| Attio field | Holds |
|---|---|
| `name` | company name |
| `domains` | dedupe key, strongest match |
| `description` | one line on what they are |
| `primary_location` | drives the time zone |
| `categories` | closest match, `Veterinary` and `Alternative Medicine` exist, most healthcare has no option |
| `employee_range` | the estimate, bucketed to `1-10`, `11-50`, `51-250`, `251-1K` |
| `linkedin` | profile |
| `team` | links to the people records |

**People, standard fields used as-is**

| Attio field | Holds |
|---|---|
| `name` | person name |
| `email_addresses` | verified addresses only |
| `phone_numbers` | company main line is fine |
| `job_title` | as written on their own site |
| `company` | record link |
| `description` | persona tag plus a one-line summary |
| `stage` | the pipeline stage, see the ladder below |
| `who_contacted` | which agent or person made contact, see above |
| `linkedin` | profile |
| `primary_location` | only when the person is clearly somewhere other than the company |

**Everything else goes in a note on the record**, created with `create-note`, titled
`GTM record` and formatted so it can be parsed back on the next run:

```
persona: ops-manager
timezone: America/Chicago
employee-estimate: 60 (basis: site-count)
sites: 4
score: 5 (size 2, footprint 1, growth 1, structure 1, fit 0)
list: Healthcare / CT / Agent
email-status: verified
sourcing: free-web-search
category: Outbound
bridge: none
signal: hiring, 3 front office roles, <url>, 2026-08-24
angle: company-trigger, <url>
status: Queued
```

The company gets its own `GTM account` note, which is where the dual write in
`crm-sync.md` lands until the custom fields exist:

```
account-status: Replied
last-touched: 2026-09-04
last-touched-by: Agent
touches: 3
next-step: Austin to reply to Jane, week of Sept 8
```

Read the note, change the lines, write it back with `update-note`. Slower than a field, but
it keeps the company record honest from day one.

**Lists carry the routing.** One Attio list per industry and region and type, created with
`create-list` and named to match `lists-and-icp.md`:

```
Healthcare / ET / Personal
Healthcare / ET / Agent
Healthcare / CT / Personal
...
```

A company or person joins the list its score puts it in. `add-record-to-list` does the
assignment, and list entries are what Austin sorts and works from.

## Option B, the custom fields

Cleaner, sortable, and worth having before the first real list build.

**Partly done.** People now carries `stage` and `who_contacted`, which cover the GTM status
and owner rows below. Companies is still entirely stock, so every company field here is
still to add, and the company roll-up in `crm-sync.md` runs through the `GTM account` note
until they exist.

If a field was added in the UI and the agent cannot see it, something is off: a different
workspace, an unsaved draft, or the connection needs reauthorising. Re-run
`list-attribute-definitions` before assuming the agent can write to a field, and never write
into a field name that has not come back from that call.

### On Companies

| Field | Type | Options |
|---|---|---|
| Industry (GTM) | select | Healthcare, Real Estate, Frontline, Other |
| Employee count (est.) | number | exact-ish estimate, see below |
| Employee count basis | select | site-count, linkedin, directory, stated, guess |
| Sites | number | |
| Time zone | select | ET, CT, MT, PT, AKT, HT, unknown |
| Buying power score | number | |
| List assignment | select | Personal, Agent, Excluded |
| Signal | select | former-customer, new-leadership, high-intent-visit, tech-stack, expansion, hiring |
| Signal source | text (URL) | |
| Signal date | date | |
| Sourcing | select | free-web-search, paid-apollo, paid-hunter, paid-clay |
| Account status | select | the ladder below, furthest rung any person there has reached |
| Last touched | date | any outreach to anyone at this company |
| Last touched by | select | Austin, Agent |
| Touches | number | running count across every person at the company |
| Next step | text | one line, what happens next at this account |

The last five are what make the dual write in `crm-sync.md` work. They are also what enforces
the one-cold-email-per-company-per-week rule, since without a company-level last-touched date
the agent has to go read every person record to find out whether the account was hit
this week.

### On People

| Field | Type | Options |
|---|---|---|
| Persona | select | owner-operator, clinical-lead, ops-manager, it-security, finance, hr-people, frontline-supervisor |
| Email status | select | verified, published-role-inbox, catch-all, unverified, bounced |
| Outreach category | select | Inbound, Postbound, Bridgebound, Outbound |
| Bridge path | text | |
| Personalization angle | select | authored-content, engaged-content, background, company-trigger, generic |
| Personalization source | text (URL) | |
| GTM status | select | the ladder below |
| Owner | select | Austin, Agent |
| Last touch | date | |
| Last touch type | select | email-sent, reply-received, call, meeting, note |

Once these exist, the agent writes to the fields instead of the note, and the note goes back
to being a note. Nothing else in the workflow changes.

## Where employee count belongs

**On Companies, not People.** It is a property of the business, so one company record holds
one number and every person there inherits it by being linked. Put it on people and the same
figure gets stored five times at a five-contact account, and the first time one copy is
updated the others are quietly wrong.

Three fields, all on Companies:

| Field | Type | Why |
|---|---|---|
| `employee_range` | select, already exists | Attio's stock bucketed field. Free, sortable, good for views. Buckets: 1-10, 11-50, 51-250, 251-1K |
| Employee count (est.) | number, to add | the actual estimate the score runs on, since the buckets are too coarse for the 0 to 4 size points |
| Employee count basis | select, to add | site-count, linkedin, directory, stated, guess. Keeps the estimate honest |

The agent writes all three together. The number drives the score, the range drives the view,
and the basis is what stops an estimate hardening into a fact.

**If it needs to be visible on a person record**, reach it through the `company` link rather
than copying it. Attio views can pull columns from a linked record, so a people view can show
the company's employee count without the person record owning the value. If a real copy on
the person is wanted anyway, the rule is one direction only: Companies is the source, the
agent overwrites the person's copy on every touch, and nothing ever writes back the other
way.

## Persona tags

Set on the person, used by both personalization and copywriting. Kept short on purpose.

- `owner-operator`: owns or runs the business, signs the cheque
- `clinical-lead`: physician lead, medical director, clinical director
- `ops-manager`: practice manager, office manager, operations
- `it-security`: IT, security, compliance
- `finance`: CFO, controller, finance lead
- `hr-people`: HR, people ops, staffing
- `frontline-supervisor`: supervises the non-desk staff who would actually use Chanty

## Status ladder

The ladder is now the live `stage` field, not a set of names this file invents. Where the
original ladder and the built field disagree, **the field wins**, because it is what Austin
sorts his pipeline by.

| Original rung | Live `stage` option | Notes |
|---|---|---|
| New | `Not Contacted` | |
| Queued | no field option | A staged draft is not a CRM state. Queue membership lives in Agent 1's `state/send-queue.md`. Do not invent a stage for it. |
| Sent | `Contacted` | First touch. |
| (none) | `Follow-Up Sent` | New. Every touch after the first. |
| Replied | `Replied` | |
| Meeting Booked | `Meeting Booked` | |
| (none) | `Opportunity` | New. A qualification call, so it is flagged, never automatic. |
| Contracting | `Contracting` | Flagged. |
| Won / Lost | `WON-Closed` / `LOST-Closed` | Flagged. |
| (none) | `Not a Fit` | New. Flagged. |
| (none) | `Follow Up Needed` | New. A work queue flag, not a pipeline position, which is why it sits at order 11 after the closed stages. Set it when a touch has gone unanswered and no follow-up has gone out. Clear it to `Follow-Up Sent` when one does, or `Replied` if they answer. Never set it over `Meeting Booked` or later. |

Nothing skips a rung without Austin saying so, and nothing moves backward. A new cold
contact at an account already at `Replied` does not drag anything back.

### The three side statuses have nowhere to live

`Bounced`, `Held` and `Do Not Contact` are all required by `crm-sync.md` and **none of them
is an option on the `stage` field.** That is a live gap, and `Do Not Contact` is the
dangerous one: `crm-sync.md` calls it the one flag that moves without asking and never gets
reversed, so it must not be recoverable only from a note body.

Until Austin adds them as options:

- **Do Not Contact** is written to the `GTM record` note as `status: Do Not Contact`, the
  person is pulled from every queue, and it is repeated in the run summary. Never
  approximate it with `Not a Fit`, which means the opposite thing about the account.
- **Bounced** goes in the note as `email-status: bounced` and the address is suppressed.
- **Held** is a queue state, so it stays in Agent 1's `state/send-queue.md` where it already
  lives, and needs no field.

Adding `Do Not Contact` and `Bounced` to the `stage` field is the cleanest fix and should
happen before real volume.

There is no Deals object in the workspace, so `Contracting` and past it live on the person
record for now. One person therefore carries one stage, which caps things at one open
opportunity per human. If Austin adds Deals later, those rungs move there and the person
record keeps everything up to `Meeting Booked`.

## Views

What Austin actually reads:

1. **Personal list pinned at the top.** Sortable by time zone, contact info visible in the
   row without opening the record, sorted by score descending inside each time zone.
2. **Agent list underneath, its own section.** Same columns, same sort.

Attio views are configured in the UI, not over the API, so the agent's part is getting the
list membership and the fields right. The layout is a one-time setup job.

## Tools the agent uses

| Job | Tool |
|---|---|
| Find an existing record before creating | `search-records`, then `get-records-by-ids` |
| Create or update in one call | `upsert-record`, keyed on domain for companies and email for people |
| Create only | `create-record` |
| Update a known record | `update-record` |
| Structured detail | `create-note`, `update-note`, `get-note-body` |
| Routing | `create-list`, `add-record-to-list`, `update-list-entry-by-record-id` |
| Reading replies against records | `search-emails-by-metadata`, `semantic-search-emails`, `get-email-content` |
| Confirming a booked meeting | `search-meetings` |
| Duplicates | `merge-records`, **only after Austin confirms**, never on the agent's own judgement |

## Fallback

If the Attio connection is down, produce a spreadsheet with one tab per list, named
`<industry>-<region>-<personal|agent>`, carrying the same fields in the same order. Say in
the run summary that the fallback was used and why, and load it into Attio once the
connection is back.
