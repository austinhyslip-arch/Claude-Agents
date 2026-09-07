# Workflow: Partner Activation

A partnership is not won when someone says yes. It is won when distribution
actually happens.

1. Human sets `partner_won` (agents cannot).
2. `python3 -m eco attribution <ORG-ID>` creates the tracking ID and URL.
3. Activation checklist, all confirmed before go-live:
   - audience and geography
   - offer, exactly as agreed
   - date
   - landing page
   - tracking parameters live and tested
   - attribution record wired to the tracking URL
   - approved messaging, checked against `config/approved-claims.md`
   - logos and brand usage agreed
   - email copy for the partner to send
   - social copy
   - event logistics if applicable
   - follow-up owner and date
4. `transition begin_activation`, then `go_live` once every item is confirmed.
5. `distribution_occurred` stays false until the newsletter goes out, the webinar
   runs, or the resource is posted. A partner sitting at "live" with no
   distribution is a partner we have not activated.
6. Record outcomes into attribution as they arrive: reach, registrations,
   attendees, visits, signups, activated teams, paid accounts, seats, MRR.
   Direct and assisted stay in separate buckets.
