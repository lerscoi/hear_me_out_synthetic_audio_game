"""
Data export for the game.
Pushes anonymous per-session results to a GitHub repository via the REST API.
"""
import base64
import json
import time
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from logic import GameState

def push_result(state: "GameState", secrets) -> bool:
    """
    Serialize and push anonymous session results to GitHub.

    Each session is written as a separate JSON file:
        {folder}/{session_id}.json

    Returns True on success, False on any failure.
    """
    try:
        github = secrets["github"]
        token = github["token"]
        repo = github["repo"]
        branch = github.get("branch", "main")
        folder = github.get("folder", "results")
    except (KeyError, Exception):
        return False

    payload = {
        "schema_version": 1,
        "session_id": state.session_id,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "score": state.score,
        "trials": state.trials,
        "correct": state.correct,
        "accuracy_pct": round(state.correct / state.trials * 100) if state.trials > 0 else 0,
        "lives_left": state.lives,
        "rounds": state.rounds,
    }

    try:
        content = base64.b64encode(
            json.dumps(payload, indent=2).encode()
        ).decode()

        url = (
            f"https://api.github.com/repos/{repo}/contents/"
            f"{folder}/{state.session_id}.json"
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }
        body = {
            "message": f"session {state.session_id[:8]}",
            "content": content,
            "branch": branch,
        }

        resp = requests.put(url, json=body, headers=headers, timeout=10)
        return resp.status_code in (200, 201)

    except Exception:
        return False
