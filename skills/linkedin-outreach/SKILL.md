---
name: linkedin-outreach
description: Run a LinkedIn outreach campaign from a logged-in browser session, including building a target contact CSV, sending connection requests without notes, sending casual curious DMs to existing connections, checking for existing threads before messaging, tracking acceptances, and automating a daily batch. Use when asked to do LinkedIn prospecting, connection campaigns, or warm-network outreach.
---

# LinkedIn Outreach Campaign

End-to-end playbook for running outbound on LinkedIn through an agent-controlled browser with the user's logged-in session.

## Prerequisites

- User logs into LinkedIn once in the agent's browser (via the Desktop tab). The session persists on the VM. Do NOT store the password unless the user opts in; 2FA makes re-login painful, so keep one long-lived session and have any daily automation message the SAME session rather than starting fresh machines.
- A target list. Either:
  - Cold: a company list (e.g. Dream 100). Find 4-5 decision makers per firm via web search, keep a profile only if the indexed LinkedIn content mentions the firm (anonymous URL checks return HTTP 999, LinkedIn blocks them).
  - Warm: the user's own connections, exported via the Voyager API (below).

## Exporting connections and locations (fast path)

Use Playwright over CDP against the running Chrome, then call LinkedIn's internal Voyager API from page context with the JSESSIONID as csrf-token:

- Connections list: `GET /voyager/api/relationships/dash/connections?decorationId=com.linkedin.voyager.dash.deco.web.mynetwork.ConnectionListWithProfile-16&count=100&q=search&sortType=RECENTLY_ADDED&start=N` (paginate by 100).
- Profile location: `GET /voyager/api/identity/dash/profiles?q=memberIdentity&memberIdentity=<publicIdentifier>&decorationId=com.linkedin.voyager.dash.deco.identity.profile.TopCardCore-1` and read the `common.Geo` entity's `defaultLocalizedName`. Throttle ~0.4s between calls.
- Headers needed: `csrf-token: <JSESSIONID value>`, `accept: application/vnd.linkedin.normalized+json+2.1`, `x-restli-protocol-version: 2.0.0`.

Filter by keyword on headline (cpa, accounting, cfo, controller, tax, audit, fintech, investor, wealth, banking, finance) and add a one-line "why relevant" per contact. Filter US-only via the location call.

## Sending connection requests

- Open the profile. Verify name AND firm match the CSV before doing anything; skip and log mismatches (many same-name profiles or same-name companies exist).
- If the primary button is Connect, click it. If it is Follow, click the ellipses (More) menu and pick Connect from there.
- Send WITHOUT a note unless the user says otherwise.
- Volume: ~15/day is safe. Stop immediately on any login wall, verification challenge, or invite-limit warning and tell the user.

## Sending DMs to existing connections

- Message style ("curious qq"): all lowercase, 1-2 sentences, starts "hey NAME, qq -", asks one specific question about THEIR work that shows you actually read their profile, no pitch, no call CTA, no em dashes. Example: "hey surya, qq about aqqrue - when you say 3x clients without headcount, is the bottleneck you're removing mostly the close work or the client back-and-forth? curious which one actually eats the hours"
- CRITICAL: after clicking Message, LOOK at the thread first. If a conversation already exists, do NOT send; flag it in the log instead. If a prior thread shows the person asked not to be contacted, exclude them permanently.
- Log every action (sent / skipped / excluded, date, one-line note) to a CSV and commit it.

## Tracking acceptances

Daily, check My Network > Manage invitations (or whether a profile now shows a Message button as 1st degree) and mark accepted rows in the log so the user knows who to DM next.

## Daily automation

Create a schedule automation whose action is `message_session` targeting the SAME session that holds the LinkedIn login (fresh machines would need re-login + 2FA). The daily prompt: pick next N unsent from the CSV, verify identity, send, update the log, check acceptances, stop on any LinkedIn warning, message the user a one-line summary. Respect the user's current mode (connects vs DMs only, cool-off days).

## Files

- `contacts.csv` - cold targets (rank, company, name, title, url)
- `finance_connections_us.csv` - warm targets (name, headline, url, why relevant, location)
- `outreach-log.csv` / `dm-log.csv` - action logs
- `messages.md` / `warm-messages.md` - drafted copy
