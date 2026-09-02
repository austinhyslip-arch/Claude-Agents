# Routing and personalization

Order of operations: rank the signal, classify the lead, check for a bridge, map the
committee, then pick the angle. Each step narrows what the email can honestly say.

## 1. Rank the signal

Run `outbound-triggers-6`. The six categories, with what they look like in healthcare:

| Trigger | What to look for |
|---|---|
| Leadership change | new practice manager, new director of operations, new COO |
| Hiring | open roles posted in the last 60 days, especially front office or multi-site roles |
| Tech stack | a job post naming the tools they run, a vendor page listing them as a customer |
| Expansion | new location announced or opened, an acquisition of another practice |
| Funding or ownership | PE backing, a group roll-up, a management services organisation deal |
| Content or public activity | a leader posting, speaking, quoted in trade press |

Record the trigger, its source URL and its date. Anything older than 90 days is stale and
does not carry an email on its own.

No trigger is a normal state. Untriggered accounts still get worked, they just sort below
triggered ones inside the same list.

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
