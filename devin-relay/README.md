# Devin Relay

A minimal Slack bot that routes tasks from any Slack workspace to a **personal Devin account** via the [Devin API](https://docs.devin.ai/api-reference/overview). Useful when your day-to-day identity (company email) has no Devin credits but your personal account does.

How it works:

- `@devin-relay <task>` in a channel (or just DM the bot) → creates a Devin session in the account that owns `DEVIN_API_KEY`.
- Replies in that Slack thread → forwarded to the same session.
- Devin's messages, status changes ("waiting on you", "finished"), and PR links → posted back into the thread.

The bot uses Slack **Socket Mode**, so it needs no public URL — it can run on a laptop, a VPS, or any free-tier host.

## Setup

### 1. Get a Devin API token (personal account)

Log in to [app.devin.ai](https://app.devin.ai) with your **personal** account → Settings → API keys / Personal Access Tokens → create a token (`cog_...`). Sessions created with it use that account's credits.

### 2. Create the Slack app

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From a manifest** → pick your workspace → paste `slack_app_manifest.yaml`.
2. Under **Basic Information → App-Level Tokens**, generate a token with the `connections:write` scope → this is `SLACK_APP_TOKEN` (`xapp-...`).
3. Under **Install App**, install to the workspace → copy the **Bot User OAuth Token** → this is `SLACK_BOT_TOKEN` (`xoxb-...`).

If your company workspace doesn't allow custom apps, create a free Slack workspace of your own — the relay works the same.

### 3. Run it

```bash
cd devin-relay
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # fill in the three tokens
.venv/bin/python relay.py
```

Optional: set `ALLOWED_SLACK_USER_IDS` in `.env` to lock the bot to your Slack user ID(s).

### Keeping it running

- **Laptop/VPS**: `nohup .venv/bin/python relay.py &` or a systemd unit:

  ```ini
  [Unit]
  Description=Devin Relay
  After=network.target

  [Service]
  WorkingDirectory=/path/to/devin-relay
  ExecStart=/path/to/devin-relay/.venv/bin/python relay.py
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

- **Fly.io / Railway / Render background worker**: deploy as a worker process (no HTTP port needed). Set the three env vars in the platform dashboard instead of `.env`.

## Usage

- New task: `@devin-relay Fix the login bug in owner/repo` (or DM the bot the task directly).
- Follow-up / answer Devin's question: reply in the same thread (no @mention needed).
- Session state (thread ↔ session mapping) is kept in `state.json`.

## Alternative: opencode / any MCP client

See [`opencode-devin-mcp.md`](./opencode-devin-mcp.md) for driving your personal Devin from opencode (or Claude Code, Cursor, etc.) via the Devin MCP server — no hosting at all, but terminal-driven rather than chat-triggered.
