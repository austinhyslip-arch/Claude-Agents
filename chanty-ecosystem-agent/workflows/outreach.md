# Workflow: Outreach

Input: organizations in READY_FOR_OUTREACH.
Output: drafts sitting in Austin's Gmail. No sends.

1. Check for a current signal. `eco add-signal` if there is a new one.
2. Draft per `agents/outreach.md`, attaching every personalization claim with its
   source URL and type.
3. `python3 -m eco draft-check '<draft json>'`
   Claims, personalization and format must all pass. Fix the draft, never the
   gate.
4. `python3 -m eco gmail-draft '<draft json>'`
   Prints the `mcp__Gmail__create_draft` call. Plain text, no sign-off, `body`
   only and never `htmlBody`.
5. Make that call. The draft is now in Austin's Gmail.
6. Post the handoff block here so he knows what is sitting in there and why.

`eco send-check` still exists and still fails on `autonomy_or_human_approval`,
which is correct at level 2. Nothing in this workflow sends.

First 20 first-touch drafts: Austin reads every one in Gmail. Automated outreach
stays off until he has done that and says to turn it on. Audit each for
personalization, classification, contact choice, offer, evidence, tone, format,
and any assumption that crept in and got stated as fact.

Sequence: day 0, 4, 10, 21, then nurture. Any reply stops everything.
