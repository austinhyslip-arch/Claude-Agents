# Attio schema

Attio is the system of record. If something happened to a contact and it is not in Attio,
it did not happen.

Workspace: **Chanty**. Connected as austin@chanty.com with admin access. Verified
2026-09-02.

## What the workspace actually has today

Two standard objects, `companies` and `people`. No custom attributes on either. No Deals
object. One list, `Customer Success`, parented to companies. The workspace was created the
same day this was written, so it is effectively empty.

That matters for two reasons. The agent has no field to write a buying power score into
yet, and **the Attio MCP connection cannot create attributes**. It can create records,
lists, notes, tasks and comments, and it can update records and list entries. Adding a
custom field is a thing Austin does in the Attio UI.

So there are two ways to run, and the first one works today.

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

Order matters. Nothing skips a rung without Austin saying so.

`New` → `Queued` → `Sent` → `Replied` → `Meeting Booked` → `Contracting` → `Won` / `Lost`

Side statuses that do not sit on the ladder: `Bounced`, `Held`, `Do Not Contact`.

There is no Deals object in the workspace, so `Contracting` and past it live on the person
record for now. If Austin adds Deals later, those two rungs move there and the person
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
