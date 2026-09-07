# Workflow: Daily Operation

Morning
- Discover new organizations in one category slice.
- Research the organizations that entered DISCOVERED yesterday.
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
