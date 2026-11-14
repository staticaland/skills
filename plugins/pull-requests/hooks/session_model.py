#!/usr/bin/env python3
"""SessionStart and PostModelSwitch hook: record the session's model.

No environment variable names the model a session runs on, and PreToolUse
input does not carry it in Claude Code. Two events do: SessionStart input has
an optional `model`, and PostModelSwitch input has `to_model` for every later
change. This hook writes that value to a file named after the session id.

`pr.py submit` in the create-pr skill calls `lookup` with
CLAUDE_CODE_SESSION_ID, the session id Claude Code exports to Bash commands,
and `display_name` to turn the id into the name the notice shows.

The hook prints nothing and always exits 0: stdout on these events becomes
context for the model, and a failure here must not disturb the session.
"""

import json
import re
import sys
import time
from pathlib import Path

STATE_DIR = Path.home() / ".cache" / "pull-requests-plugin" / "session-model"
MAX_AGE_SECONDS = 30 * 24 * 60 * 60

# What a model name may hold. It lands in markdown, so no markup characters.
SAFE_MODEL = re.compile(r"[\w .:/@\[\]-]{1,60}")
SAFE_SESSION = re.compile(r"[\w-]{1,100}")

# claude-opus-5-5, claude-sonnet-4-5-20250929, us.anthropic.claude-opus-5-v1:0
FAMILY_FIRST = re.compile(r"claude-([a-z]+)-(\d+)(?:-(\d{1,2}))?(?!\d)")
# claude-3-5-sonnet-20241022
VERSION_FIRST = re.compile(r"claude-(\d+)(?:-(\d{1,2}))?-([a-z]+)")


def clean(model):
    """model stripped, or None when it is not a plain model name."""
    if not isinstance(model, str):
        return None
    model = model.strip()
    return model if SAFE_MODEL.fullmatch(model) else None


def display_name(model):
    """A readable name for a model id: claude-opus-5-5 becomes Opus 5.5.

    An id that does not follow the Claude naming scheme is returned as it
    is, so a Codex slug or a gateway's custom id still shows. Returns None
    for a value that is not a plain model name.
    """
    model = clean(model)
    if model is None:
        return None
    if match := FAMILY_FIRST.search(model):
        family, major, minor = match.groups()
    elif match := VERSION_FIRST.search(model):
        major, minor, family = match.groups()
    else:
        return model
    version = f"{major}.{minor}" if minor else major
    return f"{family.capitalize()} {version}"


def state_file(session_id, state_dir=None):
    if not isinstance(session_id, str) or not SAFE_SESSION.fullmatch(session_id):
        return None
    return Path(state_dir or STATE_DIR) / session_id


def record(session_id, model, state_dir=None):
    """Store model as the model of session_id. Old records are removed."""
    path = state_file(session_id, state_dir)
    model = clean(model)
    if path is None or model is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(model + "\n")
    cutoff = time.time() - MAX_AGE_SECONDS
    for other in path.parent.iterdir():
        if other.is_file() and other.stat().st_mtime < cutoff:
            other.unlink(missing_ok=True)


def lookup(session_id, state_dir=None):
    """The model id recorded for session_id, or None."""
    path = state_file(session_id, state_dir)
    if path is None:
        return None
    try:
        return clean(path.read_text())
    except OSError:
        return None


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
        # SessionStart names the model `model`; PostModelSwitch, `to_model`.
        model = hook_input.get("to_model") or hook_input.get("model")
        record(hook_input.get("session_id"), model)
    except Exception:  # noqa: BLE001 - never fail the session over a notice
        pass


if __name__ == "__main__":
    main()
