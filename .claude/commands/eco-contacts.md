---
description: Find the person who controls distribution, using public sources only. Never enriches. Never guesses an email.
argument-hint: <tier1|tier2|ORG-ID>
allowed-tools: Bash, Read, Glob, Grep, WebSearch, WebFetch
---

Find public contacts for: $ARGUMENTS

Read `chanty-ecosystem-agent/agents/contact.md` and follow it exactly. It contains the strictest rules in this system.

Non-negotiable:
- Public sources only: staff, team, leadership, contact, program and event pages, org PDFs, public newsletters, public profiles where a business contact is displayed, contact forms, public phone numbers.
- Never use Apollo, ZoomInfo, Hunter, Clay contact enrichment or any equivalent. They are connected here and they are blocked.
- Never construct an email from a pattern, even an obvious one. Never verify a constructed address.
- Never swap in an easier-to-reach person.
- One primary contact. Optionally one secondary. Never a list.

If the email is not public: set `email_status: not_publicly_found`, run `python3 -m eco contact-report <CON-ID>`, print that block, set `requires_user_permission = true`, and ask me before doing anything else.

Create records with `python3 -m eco add-contact`, which will reject anything that breaks the policy.
