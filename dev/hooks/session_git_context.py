#!/usr/bin/env python3
"""SessionStart hook: inject the branch's drift from its base into context."""

import json
import os
import subprocess
import sys


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
    hook_input = json.loads(sys.stdin.read() or "{}")
    cwd = hook_input.get("cwd") or None

    if git("rev-parse", "--is-inside-work-tree", cwd=cwd).returncode != 0:
        return

    base = base_branch(cwd)
    lines = ["## Git"]

    branch = git("rev-parse", "--abbrev-ref", "HEAD", cwd=cwd).stdout.strip()
    lines.append(f"branch: {branch}")

    dirty = bool(git("status", "--porcelain", cwd=cwd).stdout.strip())
    lines.append(f"worktree: {'dirty' if dirty else 'clean'}")

    fetched = git("fetch", "--quiet", "--no-tags", "origin", base, cwd=cwd)
    counts = git(
        "rev-list", "--left-right", "--count", f"origin/{base}...HEAD", cwd=cwd
    )
    if counts.returncode != 0:
        lines.append(f"vs origin/{base}: unknown (no origin/{base} ref)")
    else:
        behind, ahead = counts.stdout.split()
        stale = " (fetch failed - offline? counts may be stale)" if fetched.returncode else ""
        lines.append(f"vs origin/{base}: {behind} behind, {ahead} ahead{stale}")
        if int(behind) > 0:
            lines.append(
                f"ACTION: rebase onto origin/{base} before touching files "
                f"(git rebase origin/{base})."
            )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(lines),
        }
    }))


if __name__ == "__main__":
    try:
        main()
    except subprocess.TimeoutExpired:
        pass
