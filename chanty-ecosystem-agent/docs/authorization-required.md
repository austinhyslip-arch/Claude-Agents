# What Needs a Human Before This System Can Do More

Nothing below has been worked around, defaulted, or quietly assumed. Each item
is a deliberate stop.

## Required before any message can be sent

1. **Physical mailing address** for the commercial email footer.
   `config/policy.json` -> `email_compliance.physical_address` is null.
2. **Sending infrastructure.** Which platform actually sends, with its own
   suppression list wired to ours.
   `email_compliance.sending_infrastructure` is null.
3. **Legal review.** `email_compliance.legal_review_status` is `not_reviewed`.
   The commercial email requirements this system implements are the baseline;
   counsel should review the production architecture.
4. **Autonomy level.** `autonomy.current_level` is 0, research only. Level 2
   permits drafts. Level 3 permits automated outreach for named Tier 2
   categories, which are listed in `autonomy.autonomous_send_enabled_categories`
   and that list is empty.

Until all four are set, `eco send-check` fails. That is the intended state.

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
