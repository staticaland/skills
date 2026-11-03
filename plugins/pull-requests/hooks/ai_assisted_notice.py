#!/usr/bin/env python3
"""PreToolUse hook: end gh pr and gh issue bodies with an AI-assistance notice.

Matches `gh pr create`, `gh pr edit`, `gh issue create`, and `gh issue edit`,
with inherited flags such as `-R owner/repo` allowed between the words. The
body may arrive as `--body`, `-b`, `--body-file`, `-F`, or a heredoc on
stdin. The call passes when that body ends with NOTICE; a body without it is
denied with the line to add. A heredoc the hook cannot delimit falls back to
a presence check on the command text.

`pr.py submit` in the create-pr skill imports `wrap` from this module, so the
skill and the hook agree on one notice.
"""

import json
import re
import shlex
import sys
from pathlib import Path

NOTICE = "**<sub>AI assisted 🤖</sub>**"

# Inherited gh flags that take a value, so the token after them is not a word.
VALUE_FLAGS = ("-R", "--repo")

HEREDOC = re.compile(
    r"<<-?\s*(?P<quote>['\"]?)(?P<tag>\w+)(?P=quote)[^\n]*\n(?P<body>.*?)\n[ \t]*(?P=tag)[ \t]*(?:\n|$)",
    re.DOTALL,
)


def wrap(body):
    """Return body with NOTICE as its last line."""
    body = body.strip("\n")
    if body.endswith(NOTICE):
        return body + "\n"
    return f"{body}\n\n{NOTICE}\n"


def ends_with_notice(text):
    return text.rstrip().endswith(NOTICE)


def tokens(command):
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def skip_flags(argv, index):
    """Index of the first token after the flags that start at index."""
    while index < len(argv) and argv[index].startswith("-"):
        index += 2 if argv[index] in VALUE_FLAGS else 1
    return index


def find_invocation(argv):
    """(kind, verb, index after verb) for the first gh pr|issue create|edit."""
    for start, token in enumerate(argv):
        if token != "gh":
            continue
        index = skip_flags(argv, start + 1)
        if index >= len(argv) or argv[index] not in ("pr", "issue"):
            continue
        kind = argv[index]
        index = skip_flags(argv, index + 1)
        if index >= len(argv) or argv[index] not in ("create", "edit"):
            continue
        return kind, argv[index], index + 1
    return None


def body_argument(argv):
    """("inline" | "file", value) from the body flag in argv, or None."""
    for index, arg in enumerate(argv):
        following = argv[index + 1] if index + 1 < len(argv) else ""
        for flag, kind in (("--body-file", "file"), ("--body", "inline")):
            if arg == flag:
                return kind, following
            if arg.startswith(flag + "="):
                return kind, arg.partition("=")[2]
        for flag, kind in (("-F", "file"), ("-b", "inline")):
            if arg == flag:
                return kind, following
            if arg.startswith(flag) and len(arg) > 2 and not arg.startswith("--"):
                return kind, arg[2:]
    return None


def stdin_ends_with_notice(command):
    """Judge the heredoc a `--body-file -` reads; fall back to presence."""
    match = HEREDOC.search(command)
    if match:
        return ends_with_notice(match.group("body"))
    return NOTICE in command


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

    argv = tokens(command)
    invocation = find_invocation(argv)
    if not invocation:
        return
    kind, verb, index = invocation
    what = f"{kind} {verb}"
    rest = argv[index:]

    body = body_argument(rest)
    if body is None:
        if verb == "create" and not ({"--web", "-w"} & set(rest)):
            deny(
                f"gh {what} needs a body that ends with the AI-assistance notice. "
                f"Pass --body or --body-file with this line at the end:\n{NOTICE}"
            )
        return

    source, value = body
    if source == "inline":
        ok = ends_with_notice(value)
        where = ""
    elif value == "-":
        ok = stdin_ends_with_notice(command)
        where = ""
    else:
        where = f" in {value}"
        try:
            ok = ends_with_notice(
                (Path(hook_input.get("cwd") or ".") / value).read_text()
            )
        except OSError:
            ok = False  # missing or unreadable; gh will say so once the body is fixed

    if not ok:
        deny(
            f"The {what} body{where} needs the AI-assistance notice as its last "
            f"line. Add this line at the end, then run the command again:\n{NOTICE}"
        )


if __name__ == "__main__":
    main()
