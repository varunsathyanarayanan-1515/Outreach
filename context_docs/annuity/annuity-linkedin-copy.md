# AnnuityOrigin LinkedIn copy (adapted from cold email sequence)

Two axes A/B tested, logged per send in annuity-dm-log.csv:
- case: `lower` (all lowercase) vs `caps` (normal capitalization)
- connect: `note` (short personalized note in the invite, <=200 chars) vs `nonote`

Rotation: cycle through variants evenly so each cell gets volume. Cap: 15 total connects+messages per day.

## Connection note variants (when `note` arm)

N1 lower:
> hey {{first_name}}, are you actively taking on more annuity cases right now or at capacity? building annuityorigin.com and talking to advisors like you

N1 caps:
> Hey {{first_name}}, are you actively taking on more annuity cases right now or at capacity? Building AnnuityOrigin.com and talking to advisors like you.

## First message after accept (or InMail-free DM if already connected via new invite)

M1 (capacity, short - mirrors Email 1):
> {{first_name}}, are you actively taking on more annuity cases at the moment or are you at capacity?

M2 (call CTA - Email 2A):
> {{first_name}} - if we could put pre-qualified high-asset retirees ($3m+ in assets) who want to talk about annuities on your calendar, would it be worth an intro? happy to walk you through exactly how we do this for advisors like you, even if you just take the strategy and run with it yourself

M3 (pay per show - Email 3A/3B):
> {{first_name}}, are you actively taking on more annuity cases, or at capacity? we place meetings with pre-qualified retirees with $3m+ in liquid investable assets on your calendar. you pay only when they show up and pass the agreed state, asset, and intent criteria. worth an intro?

M4 (exclusive - Email 3):
> {{first_name}}, if we could give you exclusive (no lead sharing) access to pre-qualified retirees with $3m+ in liquid investable assets, worth an intro? they're placed directly on your calendar and you pay only if they show up and are qualified

M5 (pre-education - Email 5):
> {{first_name}}, when a new annuity lead lands on your calendar, do they already know why they're meeting with you specifically? we pre-educate each qualified $3m+ retiree on annuities before the meeting. you pay only if they show up and qualify. worth an intro?

M6 (lead scar - Email 6):
> {{first_name}}, are you currently paying for annuity leads that never turn into a qualified conversation? we put retirees with $3m+ in liquid investable assets directly on your calendar, and you only pay when they show up and qualify. worth seeing how it works?

Each M variant exists in `lower` (as written above, all lowercase) and `caps` (normal capitalization, same words). Personalize the first line where the profile gives a hook (their radio show, seminar practice, niche) but keep it one clause, yuvan style, no em dashes.

## Industry / CMO / non-advisor variant (feedback angle, curious not selling)

F1 lower:
> hey {{first_name}}, i'm building annuityorigin.com, we put pre-qualified $3m+ retirees on advisors' calendars. you've seen this space from the {{their_role}} side, qq - what do most lead vendors get wrong with advisors? breaking into the space and would genuinely value your read

F1 caps: same words, normal capitalization.

## Logging columns (annuity-dm-log.csv)
linkedin_url,name,segment,action,variant,case,date,details
- segment: advisor | industry
- action: connect-note | connect-nonote | dm
- variant: N1/M1..M6/F1
