# Workflow: Qualification

Input: organizations in DISCOVERED.
Output: scored, gated organizations, and a clear reason for every rejection.

1. `python3 -m eco transition <ORG-ID> start_research`
2. Research per `agents/intelligence.md`. Audience, distribution, partnership
   behaviour, timing, contradictions.
3. `python3 -m eco score <ORG-ID> '<score inputs>'`
4. Build the opportunity per `agents/opportunity.md`.
5. Find the contact per `agents/contact.md`. This is where most organizations
   stop, and stopping here is a normal outcome, not a failure.
6. `python3 -m eco gate <ORG-ID> --contact-id ... --opportunity-id ...`
7. On pass: `transition qualify`, then `identify_contact`, then
   `ready_for_outreach`.
   On fail: read the named failures. Missing evidence goes back to research.
   Missing public email goes to `contact_email_not_public` and asks the user.
   Wrong audience goes to `disqualify` with the reason recorded.

The gate result is stored on the organization. Anyone can read why later.
