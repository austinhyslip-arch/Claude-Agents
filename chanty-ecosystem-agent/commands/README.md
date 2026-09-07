# Commands

The working slash commands live in `.claude/commands/` at the repository root,
because that is where Claude Code loads them from:

    /eco-discover   find organizations, verify, dedupe, save
    /eco-research   research and score existing organizations
    /eco-score      score or rescore against the rubric
    /eco-contacts   find public contacts, never enrich, never guess
    /eco-signals    find dated reasons to make contact
    /eco-drafts     write drafts and run the claims gates
    /eco-review     the human review queue
    /eco-send       run the full send gate, send nothing without approval
    /eco-learn      analyze outcomes, build archetypes, propose changes
    /eco-report     weekly or monthly report
    /eco-run        the whole loop, stopping at human review

The deterministic half of each command is the `eco` CLI:

    cd scripts && python3 -m eco --help

    init            create the store and print the current posture
    status          counts by state, autonomy level, enrichment usage
    policy [key]    read policy (nothing writes it)
    add-org         create an organization after a dedupe check
    dedupe-check    check a candidate without creating anything
    score           score an organization and set its band and tier
    gate            run the hard qualification gates
    transition      fire a state machine event
    add-contact     create a contact, rejecting policy violations
    contact-report  print the EMAIL_NOT_PUBLIC handoff block
    check-tool      is this tool permitted for contact data
    add-signal      record a signal and compute its decay band
    draft-check     claims and personalization gates
    send-check      the full send gate
    response        what a reply classification means
    attribution     create a partner tracking ID
    forecast        expected paid seats, with its inputs shown
    report          weekly or monthly
    learn           outcome analysis and recommendations
    attio-plan      the Attio calls to make, pending approval
    suppress        write a suppression record
    validate        revalidate every record against its schema
    audit           tail the audit log
