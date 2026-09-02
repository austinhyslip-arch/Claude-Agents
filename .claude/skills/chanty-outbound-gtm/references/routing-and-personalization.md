# Routing and personalization

Order of operations: rank the signal, classify the lead, check for a bridge, map the
committee, then pick the angle. Each step narrows what the email can honestly say.

## 1. Rank the signal

Run `buying-signals-6`. Its six signals are ranked by how well they correlate with an actual
purchase, strongest first:

| Rank | Signal | What it looks like in healthcare | Timing |
|---|---|---|---|
| 1 | Former customer or alumni user | someone who used Chanty at a previous practice | on detection |
| 2 | New leadership, 90 days or less | new practice manager, new director of operations, new COO | days 14 to 45 |
| 3 | High-intent site visits | pricing, comparison or demo pages | while it is warm |
| 4 | Tech stack change | a job post naming their tools, a vendor listing them as a customer | on detection |
| 5 | Expansion | new location announced or opened, a practice acquired | within 90 days |
| 6 | Hiring or downsizing | front office or multi-site roles posted in the last 60 days | within 60 days |

The wider trigger catalogue sits in the five `bridgebound-*` skills. Reach for them when the
six above come up empty: `bridgebound-firmographic-15` for business events,
`bridgebound-in-market-20` for active buyers and competitor timing, `bridgebound-symptoms-11`
for visible pain, `bridgebound-history-16` for anyone we have talked to before, and
`bridgebound-relationship-39` for warm paths, which feeds step 3.

Record the signal, its source URL and its date. Anything older than 90 days is stale and
does not carry an email on its own.

No signal is a normal state. Unsignalled accounts still get worked, they just sort below
signalled ones inside the same list.

**Note on the brief.** It had `outbound-triggers-6` doing this job. That skill does
something else, covered in step 6 below, so the signal ranking runs on `buying-signals-6`
instead.

## 2. Classify

`outreach-4-categories`:

- **Inbound**: they came to us. Never treat as cold. Route to Austin same day whatever the
  score says.
- **Postbound**: they showed intent without contacting us, for example a site visit, a
  pricing page hit, an event scan. Reference the intent only where it is something they
  would expect us to know.
- **Bridgebound**: a warm path exists. See step 3.
- **Outbound**: genuinely cold. Everything else.

## 3. Bridge before cold

`bridge-before-cold` runs before any Outbound draft is written. Look for:

- a shared connection who would actually make the intro
- an existing Chanty customer in the same group, region or franchise
- a partner, vendor or association overlap
- a past conversation on any record at the same company

If a bridge exists, the lead is Bridgebound and routes to Austin with the path named in the
`Bridge path` field, whichever list it scored into. Do not spend a cold first touch on an
account where a warm intro is available. The intro is worth more.

If no bridge exists, say so by leaving the field empty. An empty field is a real answer and
means the check was run.

## 4. Map the committee

`persona-mapping-framework`, at any account with more than one plausible buyer.

Healthcare, rough shape:

- **Feels the pain**: `frontline-supervisor`, `ops-manager`
- **Owns the budget**: `owner-operator`, `finance`
- **Can block**: `it-security`, `clinical-lead`
- **Often the best entry point**: `ops-manager`

Pick one entry point per account for the first touch. Two people at the same company do not
get cold-emailed in the same week. If the first contact goes quiet, the second person is a
later move and needs a different angle, not the same email with a new name on it.

## 5. Pick the angle

`personalization-playbooks`. Four angles, best first:

**Authored content.** They wrote, posted or were quoted somewhere. Strongest angle, because
it proves the email is meant for them. Needs the URL on the record.

**Engaged content.** They commented on, shared or spoke at something. Weaker than authoring
but still specific. Needs the URL.

**Background.** Something true about their role or path, for example running operations
across a set number of sites, or a recent move into the job. Needs a source, usually their
own site or profile.

**Company trigger.** The trigger from step 1. Works when the trigger genuinely changes their
week, for example a new location or a hiring burst. Weakest when it is generic company news.

**Generic.** No honest angle available. Persona and industry only. Tag the record
`personalization: generic` so reply rates stay comparable.

Generic is an acceptable outcome. Inventing a detail is not. If the record cannot support
the angle with a source, the angle is not available, whatever it would have done for the
open rate.

## 6. Pick the entry premise, cold accounts only

`outbound-triggers-6`, once the lead is genuinely Outbound and no bridge exists. Six premises
for getting into an account that has never heard of us:

| Premise | Shape | When it fits a healthcare account |
|---|---|---|
| CXO Passdown | email the top, ask to be pointed at the right person | small groups where the owner reads their own mail |
| Groundswell for info | start with end users, build support upward | larger groups with a real committee |
| Groundswell for product placement | get the product in frontline hands first | works with Chanty's free tier |
| Groundswell to decision maker | use internal usage as the proof point | only once there is usage to point at |
| Multi-Persona | coordinated outreach across the committee | multi-site groups with split budget authority |
| Typical cold outbound | one to one, heavy research, pattern-interrupt open | the default, and where most of this list lands |

Pick one per account and record it. The premise decides who gets the first email, which is
why it comes before writing and not during.

Note that CXO Passdown and Multi-Persona both put a second person at the same company in
scope. That runs into the one-cold-email-per-company-per-week rule in `send-policy.md`, and
the rule wins. Sequence them across weeks rather than emailing two people at once.

## Angle to persona, quick guide

| Persona | Angle that tends to land | Opening the email is about |
|---|---|---|
| `ops-manager` | background, company trigger | coordinating staff across shifts and sites |
| `owner-operator` | authored content, company trigger | what the coordination gap costs the business |
| `frontline-supervisor` | background | reaching staff who do not sit at a computer |
| `hr-people` | company trigger (hiring) | onboarding and reaching new staff quickly |
| `it-security` | company trigger (tech stack) | control and administration of who has access |
| `clinical-lead` | authored content | staff time lost to chasing people down |
| `finance` | company trigger (expansion, funding) | per-seat cost as the headcount grows |

The right-hand column is what the email is about, not a line to paste. Write it fresh
through the pipeline in `.claude/gtm/copywriting.md`.
