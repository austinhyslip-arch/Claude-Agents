# Evidence Model

## Source hierarchy

**A** - the organization's official website. A staff page, an events page, a
member benefits page.

**B** - the organization's own social account or announcement. Their LinkedIn
post, their press release.

**C** - a reputable third party. A trade publication, a local business journal,
a government SBDC listing.

**D** - a search snippet, an aggregator, an unverified directory.

D-level information is discovery only. It tells you where to look next. It never
appears in a message and never supports a scoring component on its own. The
personalization gate rejects it outright.

## Every claim carries

    claim         what is being asserted, in one sentence
    source        who said it
    source_type   A, B, C or D
    source_url    the specific page, not the homepage
    date_checked  when you actually looked
    confidence    KNOWN_FACT, ESTIMATE or UNKNOWN

## Fact, estimate, unknown

**KNOWN_FACT** - the organization stated it. "We represent 2,500 businesses" on
their about page. You may use the number.

**ESTIMATE** - we inferred it from directory counts, event sizes, or a third
party. You may use it internally for scoring and forecasting. You may not put the
number in a message. Write "your member community", not "your 2,500 members".

**UNKNOWN** - we do not know. Leave the field null. Do not fill it to make the
record look complete.

The gate that enforces this is `gates.check_personalization`, which looks for
numbers from ESTIMATE-level evidence appearing in the message body.

## Contradictions

When two sources disagree on something material, record both in
`contradictions` and leave it unresolved. An unresolved material contradiction
fails the hard qualification gate. Do not average, do not pick the more
convenient number, do not quietly prefer the higher one.
