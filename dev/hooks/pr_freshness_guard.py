#!/usr/bin/env python3
"""PreToolUse hook: block gh pr create/ready while HEAD is behind its base."""

import json
import os
import re
import subprocess
import sys


def strip_quoted(command):
    """Drop quoted segments so a mention of the command is not a match."""
    return re.sub(r"'[^']*'|\"[^\"]*\"", "", command)


def git(*args, cwd=None):
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        timeout=15,
    )


def base_branch(cwd):
    override = os.environ.get("BASE_BRANCH")
    if override:
        return override
    head = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD", cwd=cwd)
    if head.returncode == 0:
        return head.stdout.strip().removeprefix("origin/")
    return "main"


def main():
    raw = sys.stdin.read()
    if "gh" not in raw:  # runs on every Bash call - skip the parse work early
        return

    hook_input = json.loads(raw)
    command = hook_input.get("tool_input", {}).get("command", "")
    if isinstance(command, list):  # Codex may pass argv as a list
        command = " ".join(str(part) for part in command)

    if not re.search(r"\bgh\s+pr\s+(create|ready)\b", strip_quoted(command)):
        return

    cwd = hook_input.get("cwd") or None
    base = base_branch(cwd)
    if git("fetch", "--quiet", "--no-tags", "origin", base, cwd=cwd).returncode != 0:
        return  # offline or no origin - never block on missing data

    counts = git("rev-list", "--count", f"HEAD..origin/{base}", cwd=cwd)
    if counts.returncode != 0:
        return
    behind = int(counts.stdout.strip() or 0)
    if behind == 0:
        return

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"HEAD is {behind} commit(s) behind origin/{base}. Rebase "
                f"(git rebase origin/{base}), re-run the checks, then retry."
            ),
        }
    }))


if __name__ == "__main__":
    try:
        main()
    except subprocess.TimeoutExpired:
        pass  # a hung fetch must not block the tool call
