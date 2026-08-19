# Driving personal Devin from opencode via the Devin MCP server

Devin exposes an [MCP server](https://docs.devin.ai/work-with-devin/devin-mcp) (base URL `https://mcp.devin.ai/`) with full session management: create sessions, send messages, check status, manage playbooks/knowledge/schedules. Any MCP-compatible client — opencode, Claude Code, Cursor — can use it, so a coding agent on your work machine can delegate tasks to your personal Devin account.

Authentication: a Personal Access Token (`cog_...`) from your personal account, plus an `X-Org-Id` header with your personal org ID (found in [app.devin.ai](https://app.devin.ai) organization settings). Legacy `apk_` keys are not supported.

## opencode config

Add to `~/.config/opencode/opencode.json` (or the project's `opencode.json`):

```json
{
  "mcp": {
    "devin": {
      "type": "remote",
      "url": "https://mcp.devin.ai/mcp",
      "headers": {
        "Authorization": "Bearer cog_YOUR_PAT",
        "X-Org-Id": "org-YOUR_PERSONAL_ORG_ID"
      }
    }
  }
}
```

Then in opencode: "Use the devin MCP tools to create a session that fixes X in repo Y, and report back the session URL." opencode handles the follow-up loop interactively.

Trade-offs vs. the Slack relay:

- No hosting or Slack app needed — works immediately from your terminal.
- But it's pull-based: you check on sessions from the terminal instead of getting pinged in a chat thread.
- opencode itself needs its own LLM provider key.
