"""Slack -> Devin relay.

Mention the bot (or DM it) with a task to start a Devin session in the
account that owns DEVIN_API_KEY. Replies in the same Slack thread are
forwarded to the session, and Devin's messages, status changes, and PR
links are posted back to the thread.
"""

import json
import logging
import os
import re
import threading
import time

import requests
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("devin-relay")

DEVIN_API_BASE = os.environ.get("DEVIN_API_BASE", "https://api.devin.ai/v1").rstrip("/")
DEVIN_API_KEY = os.environ["DEVIN_API_KEY"]
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL_SECONDS", "15"))
STATE_FILE = os.environ.get("STATE_FILE", "state.json")
ALLOWED_USERS = {u.strip() for u in os.environ.get("ALLOWED_SLACK_USER_IDS", "").split(",") if u.strip()}

TERMINAL_STATUSES = {"finished", "expired"}

app = App(token=os.environ["SLACK_BOT_TOKEN"])

_bot_user_id = ""
_state_lock = threading.Lock()


def _load_state() -> dict:
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_state(state: dict) -> None:
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)


def _devin(method: str, path: str, **kwargs) -> requests.Response:
    resp = requests.request(
        method,
        f"{DEVIN_API_BASE}{path}",
        headers={"Authorization": f"Bearer {DEVIN_API_KEY}"},
        timeout=30,
        **kwargs,
    )
    resp.raise_for_status()
    return resp


def _strip_mention(text: str) -> str:
    return re.sub(r"<@[A-Z0-9]+>", "", text or "").strip()


def _thread_key(channel: str, thread_ts: str) -> str:
    return f"{channel}:{thread_ts}"


def _create_session(prompt: str) -> dict:
    return _devin("POST", "/sessions", json={"prompt": prompt}).json()


def _send_to_session(session_id: str, message: str) -> None:
    _devin("POST", f"/sessions/{session_id}/message", json={"message": message})


def _handle_task_message(event: dict, say, client) -> None:
    user = event.get("user")
    if ALLOWED_USERS and user not in ALLOWED_USERS:
        return
    channel = event["channel"]
    ts = event["ts"]
    thread_ts = event.get("thread_ts", ts)
    text = _strip_mention(event.get("text", ""))
    if not text:
        say(text="Give me a task, e.g. `@devin-relay fix the login bug in repo X`.", thread_ts=thread_ts)
        return

    key = _thread_key(channel, thread_ts)
    with _state_lock:
        state = _load_state()
        entry = state.get(key)

    if entry:
        try:
            _send_to_session(entry["session_id"], text)
            client.reactions_add(channel=channel, name="incoming_envelope", timestamp=ts)
        except requests.HTTPError as e:
            say(text=f"Failed to forward message to Devin: `{e}`", thread_ts=thread_ts)
        return

    try:
        session = _create_session(text)
    except requests.HTTPError as e:
        say(text=f"Failed to create Devin session: `{e}`", thread_ts=thread_ts)
        return

    with _state_lock:
        state = _load_state()
        state[key] = {
            "session_id": session["session_id"],
            "url": session.get("url"),
            "channel": channel,
            "thread_ts": thread_ts,
            "seen_event_ids": [],
            "last_status": None,
            "done": False,
            "pr_posted": False,
        }
        _save_state(state)

    say(
        text=f"Started Devin session: {session.get('url', session['session_id'])}\n"
        "Reply in this thread to send follow-ups. I'll post Devin's updates here.",
        thread_ts=thread_ts,
    )


@app.event("app_mention")
def on_mention(event, say, client):
    _handle_task_message(event, say, client)


@app.event("message")
def on_message(event, say, client):
    if event.get("bot_id") or event.get("subtype"):
        return
    channel_type = event.get("channel_type")
    if channel_type == "im":
        _handle_task_message(event, say, client)
        return
    # In channels, only react to replies inside threads we already track
    # (top-level tasks in channels must @mention the bot).
    thread_ts = event.get("thread_ts")
    if not thread_ts:
        return
    if f"<@{_bot_user_id}>" in (event.get("text") or ""):
        return  # app_mention handler covers this
    key = _thread_key(event["channel"], thread_ts)
    with _state_lock:
        tracked = key in _load_state()
    if tracked:
        _handle_task_message(event, say, client)


def _poll_once() -> None:
    with _state_lock:
        state = _load_state()
    for key, entry in state.items():
        if entry.get("done"):
            continue
        try:
            details = _devin("GET", f"/sessions/{entry['session_id']}").json()
        except requests.RequestException as e:
            log.warning("poll failed for %s: %s", entry["session_id"], e)
            continue
        _relay_updates(key, entry, details)


def _relay_updates(key: str, entry: dict, details: dict) -> None:
    channel = entry["channel"]
    thread_ts = entry["thread_ts"]
    seen = set(entry.get("seen_event_ids", []))
    changed = False

    for msg in details.get("messages") or []:
        if msg.get("type") != "devin_message" or msg.get("event_id") in seen:
            continue
        app.client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=msg["message"])
        seen.add(msg["event_id"])
        changed = True

    pr = details.get("pull_request") or {}
    if pr.get("url") and not entry.get("pr_posted"):
        app.client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=f"Pull request: {pr['url']}")
        entry["pr_posted"] = True
        changed = True

    status = details.get("status_enum")
    if status and status != entry.get("last_status"):
        if status == "blocked":
            app.client.chat_postMessage(
                channel=channel, thread_ts=thread_ts,
                text="Devin is waiting on you — reply in this thread to answer.",
            )
        elif status in TERMINAL_STATUSES:
            app.client.chat_postMessage(
                channel=channel, thread_ts=thread_ts,
                text=f"Session {status}: {entry.get('url', '')}",
            )
            entry["done"] = True
        entry["last_status"] = status
        changed = True

    if changed:
        entry["seen_event_ids"] = sorted(seen)
        with _state_lock:
            state = _load_state()
            state[key] = entry
            _save_state(state)


def _poll_loop() -> None:
    while True:
        try:
            _poll_once()
        except Exception:
            log.exception("poll loop error")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    _bot_user_id = app.client.auth_test()["user_id"]
    threading.Thread(target=_poll_loop, daemon=True).start()
    log.info("devin-relay running (bot user %s)", _bot_user_id)
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
