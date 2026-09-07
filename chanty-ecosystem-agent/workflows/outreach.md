# Workflow: Outreach

Input: organizations in READY_FOR_OUTREACH.
Output: drafts in the review queue. No sends.

1. Check for a current signal. `eco add-signal` if there is a new one.
2. Draft per `agents/outreach.md`, attaching every personalization claim with its
   source URL and type.
3. `python3 -m eco draft-check '<draft json>'`
   Claims and personalization must both pass. Fix the draft, do not fix the gate.
4. `python3 -m eco send-check '<draft json>'`
   Today this fails on `email_compliance` and `autonomy_or_human_approval`, which
   is correct: sending is not configured and autonomy is 0.
5. Queue for human review with the handoff block.
6. A human approves, and a human sends, until the user changes the autonomy level
   and fills in the compliance fields.

First 100 first-touch messages: every one is human reviewed, no exceptions.
Audit personalization, classification, contact choice, offer, evidence, tone, and
any assumption that crept in.

Sequence: day 0, 4, 10, 21, then nurture. Any reply stops everything.
