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

## Gmail - connected, not wired in

Sending is not configured. Even if it were, the send gate fails on
`email_compliance` until a human sets the physical address, names the sending
infrastructure and records legal review. Gmail is also not a compliant bulk
sending path; that decision belongs to a human, not to this system.

## Google Drive and Calendar - connected, unused by this system

Available if a workflow later needs them (partner assets, event dates). Nothing
depends on them today.

## Public web research - the main tool

WebSearch and WebFetch do the real work. Source URLs and dates are preserved on
every claim.

## Checking a tool

    cd scripts && python3 -m eco check-tool mcp__Apollo_io__apollo_people_match

Exits non-zero and explains why when a tool is barred.
