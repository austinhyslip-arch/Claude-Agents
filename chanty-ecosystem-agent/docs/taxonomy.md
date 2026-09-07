# Organization Taxonomy

Extensible. Adding a category is a matter of adding a line here and using it;
`organization_type` is a free string in the schema precisely so a new category
does not require a migration. `taxonomy_group` is the constrained field.

## SMB ecosystem (`smb_ecosystem`)
Chamber, SCORE, SBDC, BNI, Business Network, Entrepreneur Center, Incubator,
Accelerator, Economic Development, Small Business Alliance

## Professional and vertical (`professional_vertical`)
Accounting, Legal, Construction, Real Estate, Insurance, Staffing, Recruiting,
Marketing, Advertising, Consulting, Financial Services, Healthcare, Dental,
Veterinary, Manufacturing, Logistics, Hospitality, Home Services, Property
Management, Nonprofit

## Technology (`technology`)
MSP, IT Consultant, Technology Advisor, Microsoft Consultant, Google Workspace
Consultant, Digital Transformation, Fractional CTO, Business Software Advisor

## Influence (`influence`)
Business Coach, Consultant, Fractional Executive, Business Newsletter, Business
Podcast, Business Media, Community Operator, Event Organizer

## Scaled (`scaled`)
Franchise, Franchise Association, National Association, Multi-Chapter
Organization, Buying Group, Dealer Network, Professional Network

## Chapter model

    NATIONAL ASSOCIATION
      -> STATE ASSOCIATION
        -> LOCAL CHAPTER

Parent and child are separate records linked by `parent_organization` and
`chapter`. Dedupe will not merge two records that differ in chapter, whatever
else they share, including the domain. When one chapter converts, the Learning
Agent looks for its siblings.
