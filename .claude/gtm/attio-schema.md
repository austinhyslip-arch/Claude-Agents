# Attio schema

Attio is the system of record. If something happened to a contact and it is not in Attio,
it did not happen.

Workspace: **Chanty**. Connected as austin@chanty.com with admin access. Verified
2026-09-02.

## What the workspace actually has today

Two standard objects, `companies` and `people`. No Deals object. Lists as below.

**Austin's custom fields, live on `people` as of 2026-09-02:**

| Field | api_slug | Type | Notes |
|---|---|---|---|
| Stage | `stage` | status | 11 statuses, the real pipeline. See the ladder below. |
| Who Contacted | `who_contacted` | text | "Who reached out to this opportunity" |

**Companies has no custom fields at all**, and that matters more than it sounds. It has no
phone attribute either, standard or custom, so a company main line has nowhere to live on
the company record. Two consequences, both worked around rather than solved:

- Main lines are written to the **person** records at that company, and to the company's
  `GTM account` note.
- The company half of "every touch updates both records" has no fields to write into, so it
  goes in the note until the fields below exist.

The Attio MCP connection **cannot create attributes**. It creates records, lists, notes,
tasks and comments, and updates records and list entries. Adding a field is a thing Austin
does in the UI. Always re-run `list-attribute-definitions` before writing to a field rather
than assuming it is there.

Attio also enriches company records by itself. Creating Fast Pace Health with a name and
domain pulled in categories, LinkedIn, Twitter, an estimated ARR band and a foundation date
without being asked. Worth knowing before the agent goes and researches something Attio was
about to fill in for free.

### Lists

| List | api_slug | list_id | Parent |
|---|---|---|---|
| Customer Success | `customer_success` | d1090ab0-1b1a-4119-83bd-210b3e80d0c7 | companies |
| Healthcare / CT / Personal | `healthcare_ct_personal` | 54d05801-0490-4976-95aa-12c923494ed7 | companies |
| Healthcare / CT / Agent | `healthcare_ct_agent` | ec286089-7d94-4d73-838a-07a585f15b7e | companies |

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
stage: Not Contacted
who-contacted: (empty until someone actually reaches out)
```

The company gets its own `GTM account` note, which is where the dual write in
`crm-sync.md` lands until the custom fields exist:

```
main-line: (615) 465-6810
account-stage: Replied
last-touched: 2026-09-04
who-contacted: Agent
touches: 3
next-step: Austin to reply to Jane, week of Sept 8
```

The `main-line` line is there because Companies genuinely has no phone field. It moves to a
real attribute the day one exists.

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

**Checked 2026-09-02 against the live workspace and none of these exist yet.** Companies has
31 attributes and people has 28, all of them stock. If fields were added in the UI and the
agent cannot see them, something is off: a different workspace, an unsaved draft, or the
connection needs reauthorising. Re-run `list-attribute-definitions` before assuming the
agent can write to a field, and never write into a field name that has not come back from
that call.

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
| **Main line** | **phone number** | **the one to add first. Companies has no phone field of any kind today, so every main line the agent finds has to live on a person record or in a note.** |
| Account stage | status | mirror of the people `stage` ladder, furthest rung any person there has reached |
| Last touched | date | any outreach to anyone at this company |
| Who contacted | text | matches the people field of the same name |
| Touches | number | running count across every person at the company |
| Next step | text | one line, what happens next at this account |

The last five are what make the dual write in `crm-sync.md` work. They are also what enforces
the one-cold-email-per-company-per-week rule, since without a company-level last-touched date
the agent has to go read every person record to find out whether the account was hit
this week.

### On People

`Stage` and `Who Contacted` already exist. These would still help:

| Field | Type | Options |
|---|---|---|
| Persona | select | owner-operator, clinical-lead, ops-manager, it-security, finance, hr-people, frontline-supervisor |
| Email status | select | verified, published-role-inbox, catch-all, unverified, bounced |
| Outreach category | select | Inbound, Postbound, Bridgebound, Outbound |
| Bridge path | text | |
| Personalization angle | select | authored-content, engaged-content, background, company-trigger, generic |
| Personalization source | text (URL) | |
| Owner | select | Austin, Agent |
| Last touch | date | |
| Last touch type | select | email-sent, reply-received, call, meeting, note |
| Do Not Contact | checkbox | see the gap noted under the ladder |

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

## Stage, the real ladder

Austin's `stage` field on people. These eleven are the pipeline, and the agent uses them
rather than any ladder invented in this repo.

| # | Status | Who sets it | When |
|---|---|---|---|
| 1 | Not Contacted | Agent | on record creation, always |
| 2 | Contacted | Agent | after a first touch actually goes out, never when it is only staged |
| 3 | Follow-Up Sent | Agent | after a follow-up goes out |
| 4 | Replied | Agent | on any inbound reply, no confirmation needed |
| 5 | Meeting Booked | Agent | Calendly to Attio, or Austin confirms |
| 6 | Opportunity | **Austin** | a judgement call about whether a real deal exists |
| 7 | Contracting | **Austin** | never inferred from email content |
| 8 | WON-Closed | **Austin** | |
| 9 | LOST-Closed | **Austin** | |
| 10 | Not a Fit | Agent, narrowly | only on objective disqualification: out of ICP, wrong ownership, no distributed workforce. A judgement call goes to Austin. |
| 11 | Follow Up Needed | Agent | a reply that says "not now, come back later", or any commitment made to follow up |

Statuses 6 through 9 are the ones that wait for Austin. That is the same line the original
brief drew at `Contracting`, moved one rung earlier because `Opportunity` is a judgement
about deal quality and the agent is not the one to make it.

### Who Contacted

Set on **every** touch, to whoever actually reached out. `Austin` or `Agent`, or a name if
someone else did. This field is the reason the dual write exists: without it, an account
with three people at it gives no way to see who has already spoken to whom.

### One gap in the ladder

**There is no Do Not Contact status.** Opt-outs currently have nowhere honest to go. `Not a
Fit` means the wrong kind of account, which is a different thing from someone asking not to
be emailed, and collapsing the two loses information that matters. Worth adding either a
twelfth status or a checkbox on people. Until then, an opt-out sets `Not a Fit`, gets a note
saying it was an opt-out and not a fit judgement, and gets flagged to Austin.

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
