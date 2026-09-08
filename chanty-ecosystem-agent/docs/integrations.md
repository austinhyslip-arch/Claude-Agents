# Integrations

Checked against this environment on 2026-09-07. Nothing here is assumed.

## Attio - connected, system of record

Workspace: Chanty. Access: admin (austin@chanty.com).

What is actually there:
- Objects: `companies` and `people`. Both standard. No custom objects.
- Lists: Customer Success, Free Plans, Healthcare / CT / Agent, Healthcare / CT /
  Personal, Pipeline, VC Deal Flow.
- `people` carries a custom `Stage` status (Not Contacted through WON-Closed) and
  a `Who Contacted` text field.

What that means for this system: Attio has no home for ecosystem state, score,
band, partner tier, attribution ID, audience size or email status. The MCP surface
can create records, lists, notes and tasks, but it cannot create objects or
attributes, so those fields cannot be added programmatically.

Until a human adds them in the Attio UI, `scripts/eco/attio.py` writes the
structured detail into a note on the company record and lists exactly which
attributes are missing. It never crams a value into a field that means something
else.

`python3 -m eco attio-plan <ORG-ID>` prints the calls. Nothing runs without
approval.

A contact whose email is not public is never written to Attio's people object. It
stays in the local store as EMAIL_NOT_PUBLIC.

## Clay - connected, organizations only

Workspace: Chanty (1356452).

Permitted: `find-and-enrich-company`, `query-objects`,
`ask-question-about-accounts`, `add-company-data-points`, custom subroutines that
operate on companies.

Blocked: `find-and-enrich-contacts-at-company`, `find-and-enrich-list-of-contacts`,
`add-contact-data-points`. Blocked by name in `config/policy.json` and tested.

Clay being connected is not permission to enrich contacts.

## Apollo.io - connected, fully blocked

Every `mcp__Apollo_io__*` tool is blocked by prefix. Apollo is a contact
enrichment provider and this system does not use one. This includes the parts of
Apollo that are not enrichment: the prefix block is deliberate and blunt, because
a partial block invites a workaround.

## ZoomInfo - connected, fully blocked

Same reasoning, same prefix block.

## Gmail - connected, this is where drafts go

Sending mode is `manual_gmail_draft`. `scripts/eco/gmail.py` builds the
`mcp__Gmail__create_draft` payload and the agent makes the call. Austin reads
each draft in Gmail and sends it himself.

Two details enforced in code rather than by reminder:

- `htmlBody` is never set. The tool treats `body` as the plain-text field, so
  passing only `body` makes plain text the only possible outcome.
- `gates.check_format` rejects markdown, HTML, bullets, headings and sign-offs
  before a payload is built at all. Gmail's native signature is the only
  signature.

Because messages go one to one from a personal mailbox rather than through a
bulk platform, `physical_address_required` and `opt_out_link_required` are false
in policy. Legal reviewed this on 2026-09-08. Flip `sending_mode` to a bulk
platform and both flags go back to true; the gate reads the flags, so it
tightens on its own.

Nothing about suppression changes. An opt-out arrives as a reply, is written to
suppression the same day, and a suppressed contact can never reach a draft.

## Google Drive and Calendar - connected, unused by this system

Available if a workflow later needs them (partner assets, event dates). Nothing
depends on them today.

## Public web research - the main tool

WebSearch and WebFetch do the real work. Source URLs and dates are preserved on
every claim.

## Checking a tool

    cd scripts && python3 -m eco check-tool mcp__Apollo_io__apollo_people_match

Exits non-zero and explains why when a tool is barred.
