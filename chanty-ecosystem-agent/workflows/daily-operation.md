# Workflow: Daily Operation

Morning (the routine fires here, 07:12 Central)
- Discover new organizations in one category slice.
- Research the organizations that entered DISCOVERED yesterday.
- Find public contacts, and stop at EMAIL_NOT_PUBLIC rather than guessing.
- Write drafts into Gmail for anything that passes every gate.
- Run `eco send-window --drafts-only` and report, per draft, whether it can go
  out now and when its window opens. Austin sends; the window is his to respect
  and the report is what makes that easy.
- Review anything sitting in HUMAN_REVIEW, oldest first.

Through the day
- Check signals on qualified organizations.
- Process any responses immediately. A reply stops the sequence before anything
  else happens.
- Build handoff briefs for anything needing a human.

Evening
- `python3 -m eco validate`
- `python3 -m eco attio-plan <ORG-ID>` for records that changed, then execute the
  approved calls against Attio.
- Update attribution for any partner activity.
- `python3 -m eco status` and log the day.

Nothing in this loop sends anything. The default posture is draft, don't send.
