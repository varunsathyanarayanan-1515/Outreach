---
name: annuity-advisor-outreach
description: End-to-end LinkedIn outreach system for AnnuityOrigin - prospect independent annuity/FIA advisors, build a screened target CSV, run A/B-tested connection requests and DMs capped at 15/day, and automate the daily loop. Use when asked to prospect advisors, send outreach, or run the daily AnnuityOrigin campaign.
---

# AnnuityOrigin advisor outreach

Full loop: prospect -> screen -> connect -> message -> log -> daily automation. Runs on the operator's own LinkedIn account in a persistent logged-in browser session.

## 0. Prerequisites

- A Devin session (or any browser you control) logged into the operator's LinkedIn. Keep ONE long-lived session; 2FA makes re-login painful. Never log out, never launch a second Chrome.
- A working directory (ideally a git repo) holding the CSVs and copy doc.

## 1. ICP - who goes on the list

Ideal profile (reference: linkedin.com/in/rodney-fetaya): independent, advisor-led practice selling annuities / FIA / retirement income / guaranteed lifetime income. US-based only, verify location on the live profile.

Screenable from profiles:
- independent advisor-led practice (founder/owner/agent, not captive or FMO staff)
- FIA / safe-money / retirement-income specialization
- multi-state or virtual/nationwide model
- visible acquisition spend (seminars, radio, podcast, lead-gen site, webinars, ads)

NOT screenable (qualify in conversation): $3M-$15M written premium, calendar capacity, acquisition scars, whether they measure funded premium vs leads.

Anyone FIA/annuity/retirement adjacent still gets added. Non-advisors in the industry (CMOs, FMO owners, coaches, IMO staff) go on the list as tier `industry` and get the feedback angle, never the pitch.

## 2. Prospecting

Run parallel web searches like:
- `"fixed indexed annuities" advisor independent site:linkedin.com/in`
- `"retirement income specialist" annuities licensed states site:linkedin.com/in`
- `"guaranteed lifetime income" advisor site:linkedin.com/in`
- `"annuity" "lifetime income" advisor {state names} site:linkedin.com/in`
- seminar/radio/podcast + annuity combinations for acquisition-spend evidence

Parse results, dedupe against the CSV, keep only rows with real evidence.

## 3. Target CSV schema (`annuity-advisors.csv`)

```
tier,name,practice,title,linkedin_url,independent_fia_evidence,multistate_virtual_evidence,acquisition_spend_evidence,notes
```
tier: A (strong FIA/independent/virtual evidence), B (good fit, gaps), C (adjacent, verify), industry (feedback-angle contacts). Mark missing evidence `unknown - qualify`, never invent it.

## 4. Copy - adapted from the cold email sequence

Two A/B axes, logged per send:
- case: `lower` (all lowercase) vs `caps` (normal capitalization)
- connect: `note` vs `nonote` invite

Connection note (N1, <=200 chars):
> hey {{first_name}}, are you actively taking on more annuity cases right now or at capacity? building annuityorigin.com and talking to advisors like you

Messages after accept (rotate M1-M6, personalize the first clause from their profile, no em dashes):
- M1 capacity: "{{first_name}}, are you actively taking on more annuity cases at the moment or are you at capacity?"
- M2 intro CTA: pre-qualified $3m+ retirees on your calendar, worth an intro? happy to walk you through it even if you just take the strategy and run
- M3 pay per show: meetings with pre-qualified $3m+ retirees, you pay only when they show and pass the agreed state, asset, and intent criteria
- M4 exclusive: exclusive no-lead-sharing access, placed directly on your calendar, pay only if they show and qualify
- M5 pre-education: "when a new annuity lead lands on your calendar, do they already know why they're meeting with you specifically?" we pre-educate each one
- M6 lead scar: "are you paying for annuity leads that never turn into a qualified conversation?"

Industry contacts (F1): "i'm building annuityorigin.com... you've seen this space from the {{role}} side, qq - what do most lead vendors get wrong with advisors?" Curious, no pitch.

## 5. Daily execution rules

- HARD CAP: 15 total connects + messages per day. Skips do not count; replace with the next row.
- Tier A first, then B, then C.
- Verify on the live profile before acting: name, practice, US location. Mismatch = skip + log.
- If the primary button is Follow, use the three-dots (More) menu -> Connect.
- Existing 1st-degree connections: NEVER message without asking the operator first. Flag and skip.
- Before any DM, open the thread. Existing conversation = skip + flag.
- Stop immediately on login walls, verification challenges, invite/message limit warnings. Tell the operator.

## 6. Logging (`annuity-dm-log.csv`)

```
linkedin_url,name,segment,action,variant,case,date,details
```
- segment: advisor | industry
- action: connect-note | connect-nonote | dm
- variant: N1 / M1..M6 / F1

Each run: log every send/skip, check for newly accepted invites and mark them, commit, send the operator a one-line summary (connects by note/no-note, DMs by variant+case, skips, acceptances, new prospects added).

## 7. Automation

Devin automation with a schedule:recurring trigger, daily 12pm PT incl weekends (rrule `DTSTART;TZID=America/Los_Angeles:19700101T000000 / RRULE:FREQ=DAILY;BYHOUR=12;BYMINUTE=0`), using a message_session action pointed at the long-lived logged-in session (this is what preserves the 2FA'd login). The prompt = section 5 + 6 plus a prospecting pass from section 2.

## Caveats

- LinkedIn automation of this kind is against LinkedIn ToS. Keep volume low (15/day), human-like pacing, and stop on any warning.
- Anonymous profile fetches return HTTP 999; all verification must go through the logged-in browser.
- Track reply rates per variant/case cell before scaling any single message.
