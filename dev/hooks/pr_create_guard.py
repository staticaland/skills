#!/usr/bin/env python3
"""PreToolUse hook: route gh pr create through the create-pr skill."""

import json
import re
import sys


def strip_quoted(command):
    """Drop quoted segments so a mention of the command is not a match."""
    return re.sub(r"'[^']*'|\"[^\"]*\"", "", command)


def main():
    hook_input = json.loads(sys.stdin.read())
    command = hook_input.get("tool_input", {}).get("command", "")

    if not re.search(r"\bgh\s+pr\s+(?:create|new)\b", strip_quoted(command)):
        return

    if "SKILL_CREATE_PR=1" in command:
        return

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Direct gh pr create is blocked. Invoke the create-pr skill "
                "instead: it builds the PR description from the whole "
                "session and fills the PR template."
            ),
        }
    }))


if __name__ == "__main__":
    main()
