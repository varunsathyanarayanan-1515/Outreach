# context_docs

Everything backing the outbound motion to US accounting/CPA firms.

## Where to look

| Question | File |
|---|---|
| Who are my LinkedIn connections? | `network/my-linkedin-connections.csv` |
| Who did I send connection requests to? | `outreach/connection-requests-log.csv` |
| Who did I actually message, and what did I say? | `outreach/messages-log.csv` |
| Who should I reach out to next? | `targets/` |
| What do I know about the market? | `research/` |

## `network/` — who I know

- `my-linkedin-connections.csv` — Varun's own 1st-degree connections pulled from his logged-in account (`name, headline, public_id, location`). 742 of the 767 the LinkedIn UI reports; the API stops paginating short of the full count.
- `colleague-finance-connections-us.csv` — **not Varun's network.** 116 US finance profiles from a colleague's account; only 5 overlap with his own connections. Kept for reference only, do not treat as warm.

## `targets/` — who to reach out to

- `dream-100-accounts.md` — the account list and why each firm is on it.
- `dream-100-plan.md` — how the Dream 100 campaign runs.
- `dream100-contacts.csv` — named contacts at those firms, the source for connection requests.
- `warm-connections-us.csv` — warm 1st-degree connections with US market context, with a per-person writeup and a drafted message. Filtered out of `network/my-linkedin-connections.csv`.

## `outreach/` — what I've actually done

- `connection-requests-log.csv` — one row per connection request (`sent` / `skipped`), with the reason when skipped.
- `messages-log.csv` — one row per DM actually sent, with the verbatim message, whether a reply came back, and when to follow up.

Both logs are append-only. Nothing goes in until it has actually happened on LinkedIn.

## `research/` — what I know

- `accounting-software-market-learnings.md`
- `market-research.md`
- `reddit-voice-of-customer.md`
- `offers.md`
