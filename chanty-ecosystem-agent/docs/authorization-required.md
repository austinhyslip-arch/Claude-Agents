# What Needs a Human Before This System Can Do More

Nothing below has been worked around, defaulted, or quietly assumed. Each item
is a deliberate stop.

## Settled on 2026-09-08

1. **Sending path.** Drafts go into Austin's Gmail. He reads each one and sends
   it himself. `email_compliance.sending_mode` is `manual_gmail_draft`.
2. **No postal address.** Not required for one-to-one mail from a personal
   mailbox. `physical_address_required` is false.
3. **No unsubscribe link.** Same reason. `opt_out_link_required` is false, and
   `opt_out_honored_on_reply` is true, so a request to stop is written to
   suppression the same day.
4. **Legal review done.** `legal_review_status` is `reviewed`.
5. **Autonomy level 2.** Research, contact discovery, and drafts into Gmail.

`eco send-check` now passes everything except `autonomy_or_human_approval`,
which is correct: at level 2 a human approves each one, and that human is Austin
hitting send in Gmail.

## The one thing still open on sending

**Level 3, after the first 20.** Automated outreach turns on once Austin has read
the first 20 drafts in Gmail and says to turn it on. Two fields change then, and
only he changes them:

- `autonomy.current_level` to 3
- `autonomy.autonomous_send_enabled_categories` to the categories he names

The agent never raises its own level. Tier A and strategic organizations stay
human-approved regardless.

Level 3 also needs a real sending path decided at that point. Gmail drafts do not
automate, so automated outreach means either a scripted Gmail send or a proper
platform. A bulk platform brings the postal address and unsubscribe requirements
back, which is why those flags exist in policy rather than being deleted.

## Required for full Attio fidelity

Custom attributes cannot be created through the MCP surface. In Attio, under
Settings > Objects:

On **Companies**: ecosystem_state (status), organization_score (number),
priority_band (select), organization_type (select), partner_tier (select),
attribution_id (text), audience_size (number), audience_confidence (select),
recommended_offer (select), parent_organization (record reference),
last_researched (date).

On **People**: email_status (select), email_source_url (text), role_category
(select).

Also useful: a list named "Ecosystem Partners" on companies, for the pipeline
view. `eco attio-plan` includes the definition.

Until then the detail goes into a note on the company record, which is readable
but not filterable.

## Required for attribution to mean anything

- A partner landing page pattern, so tracking URLs resolve.
  `attribution.create` currently builds `https://www.chanty.com/partners/<id>`,
  which is a placeholder until someone confirms the real pattern.
- A way to read trial, activation and paid conversion data back per tracking ID.
  Without it, `direct` attribution stays at zero and every forecast stays an
  assumption.

## Decisions only you can make

- Whether the partner/referral offer has any economics at all, and what they are.
  The system will identify when that conversation is warranted and will never
  conduct it.
- Whether enrichment is ever permitted, and for which contact. The default is no,
  per contact, and asked each time.
- Which Tier 2 categories, if any, ever get automated outreach.

## What has not been done, on purpose

- No outreach was sent.
- No enrichment provider was called.
- No email address was constructed or inferred.
- No Attio records were created or modified.
- No credentials were requested, stored, or worked around.
