#!/usr/bin/env python3
"""PreToolUse hook: require an AI-assistance notice on gh pr and gh issue bodies.

Matches `gh pr create`, `gh pr edit`, `gh issue create`, and `gh issue edit`.
The body may arrive as `--body`, `-b`, `--body-file`, `-F`, or a heredoc on
stdin. The call passes when NOTICE appears in the command text or in the body
file it names; a body without it is denied with the line to add.

`pr.py submit` in the create-pr skill imports `wrap` from this module, so the
skill and the hook agree on one notice.
"""

import json
import re
import shlex
import sys
from pathlib import Path

NOTICE = "<sub>🤖 Written with AI assistance.</sub>"

BODY_FLAGS = ("--body", "-b", "--body-file", "-F")


def wrap(body):
    """Return body with NOTICE as the first and last line."""
    body = body.strip("\n")
    if body.startswith(NOTICE) and body.endswith(NOTICE):
        return body + "\n"
    return f"{NOTICE}\n\n{body}\n\n{NOTICE}\n"


def strip_quoted(command):
    """Drop quoted segments so a mention of the command is not a match."""
    return re.sub(r"'[^']*'|\"[^\"]*\"", "", command)


def body_file(command):
    """The path given to --body-file or -F, or None."""
    try:
        argv = shlex.split(command)
    except ValueError:
        argv = command.split()
    for index, arg in enumerate(argv):
        if arg in ("--body-file", "-F") and index + 1 < len(argv):
            return argv[index + 1]
        if arg.startswith("--body-file="):
            return arg.partition("=")[2]
    return None


def has_body_flag(stripped):
    return any(
        re.search(rf"(^|\s){re.escape(flag)}(=|\s|$)", stripped) for flag in BODY_FLAGS
    )


def deny(reason):
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def main():
    raw = sys.stdin.read()
    if "gh" not in raw:  # runs on every Bash call - skip the parse work early
        return

    hook_input = json.loads(raw)
    command = hook_input.get("tool_input", {}).get("command", "")
    if isinstance(command, list):  # Codex may pass argv as a list
        command = " ".join(str(part) for part in command)

    stripped = strip_quoted(command)
    match = re.search(r"\bgh\s+(pr|issue)\s+(create|edit)\b", stripped)
    if not match:
        return

    kind, verb = match.groups()
    what = f"{kind} {verb}"

    if NOTICE in command:
        return

    path = body_file(command)
    if path and path != "-":
        cwd = Path(hook_input.get("cwd") or ".")
        try:
            if NOTICE in (cwd / path).read_text():
                return
        except OSError:
            pass  # the file is missing or unreadable; gh will say so
        deny(
            f"The {what} body in {path} needs the AI-assistance notice. Add "
            f"this line as its first and last line, then run the command again:\n"
            f"{NOTICE}"
        )
        return

    if has_body_flag(stripped):
        deny(
            f"The {what} body needs the AI-assistance notice. Add this line as "
            f"its first and last line, then run the command again:\n{NOTICE}"
        )
        return

    if verb == "create" and not re.search(r"(^|\s)(--web|-w)(\s|$)", stripped):
        deny(
            f"gh {what} needs a body that carries the AI-assistance notice. Pass "
            f"--body or --body-file with this line as its first and last line:\n"
            f"{NOTICE}"
        )


if __name__ == "__main__":
    main()
