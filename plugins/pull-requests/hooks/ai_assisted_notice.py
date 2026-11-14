#!/usr/bin/env python3
"""PreToolUse hook: end gh pr and gh issue bodies with an AI-assistance notice.

Matches `gh pr create`, `gh pr edit`, `gh issue create`, and `gh issue edit`,
with inherited flags such as `-R owner/repo` allowed between the words. The
body may arrive as `--body`, `-b`, `--body-file`, `-F`, or a heredoc on
stdin. The call passes when that body ends with the notice; a body without
it is denied with the line to add. A heredoc the hook cannot delimit falls
back to a presence check on the command text.

The notice may name the model that wrote the body, as in
`**<sub>AI assisted 🤖 · Opus 5.5</sub>**`. The hook accepts the notice with
any model name and without one.

A `--body-file` path is expanded like a shell would. When a heredoc in the
same command writes that path, the hook judges the heredoc, since the file is
not written until after the hook runs. A body file that cannot be read is
denied with its own message, never with a request to append the notice.

`pr.py submit` in the create-pr skill imports `wrap` from this module, so the
skill and the hook agree on one notice.
"""

import json
import os
import re
import shlex
import sys
from pathlib import Path

NOTICE = "**<sub>AI assisted 🤖</sub>**"

# NOTICE, with or without " · <model name>" before the closing tag.
NOTICE_PATTERN = r"\*\*<sub>AI assisted 🤖(?: · [^<>\n]{1,80})?</sub>\*\*"
NOTICE_AT_END = re.compile(NOTICE_PATTERN + r"\s*\Z")

# Inherited gh flags that take a value, so the token after them is not a word.
VALUE_FLAGS = ("-R", "--repo")

HEREDOC = re.compile(
    r"<<-?\s*(?P<quote>['\"]?)(?P<tag>\w+)(?P=quote)(?P<after>[^\n]*)\n(?P<body>.*?)\n[ \t]*(?P=tag)[ \t]*(?:\n|$)",
    re.DOTALL,
)


# Shell operators that end one command and start the next.
SEPARATORS = (";", "&&", "||", "|", "&")
REDIRECTS = (">", ">>", ">|")


def notice(model=None):
    """NOTICE, naming model when there is one."""
    if not model:
        return NOTICE
    return NOTICE.replace("</sub>", f" · {model}</sub>")


def wrap(body, model=None):
    """Return body with the notice as its last line, naming model if given."""
    body = body.strip("\n")
    if ends_with_notice(body):
        if not model:
            return body + "\n"
        body = NOTICE_AT_END.sub("", body).rstrip("\n")
    return f"{body}\n\n{notice(model)}\n"


def ends_with_notice(text):
    return NOTICE_AT_END.search(text) is not None


def tokens(command):
    # A heredoc body is text, not shell: an apostrophe in it would make
    # shlex.split fail on the whole command, so keep only its first line.
    command = HEREDOC.sub(
        lambda match: match.string[match.start() : match.end("after")] + "\n",
        command,
    )
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


def body_path(value, cwd):
    """The file a --body-file value names, with $VARS and ~ expanded as a shell would."""
    expanded = os.path.expanduser(os.path.expandvars(value))
    return Path(cwd or ".") / expanded


def redirect_target(line):
    """The file the heredoc command on line writes with > or >>, or None."""
    lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        words = list(lexer)
    except ValueError:
        return None
    segment = []
    for word in words + [";"]:
        if word not in SEPARATORS:
            segment.append(word)
            continue
        if "<<" in segment:
            for index, word in enumerate(segment[:-1]):
                if word in REDIRECTS:
                    return segment[index + 1]
            return None
        segment = []
    return None


def heredoc_writing(value, command, cwd):
    """The last heredoc in command written to the body file value, or None.

    The hook runs before the command, so `cat > body.md <<'EOF'` in the same
    command has not written the file yet: judge the heredoc instead.
    """
    target = body_path(value, cwd)
    text = None
    for match in HEREDOC.finditer(command):
        start = command.rfind("\n", 0, match.start()) + 1
        written = redirect_target(command[start : match.end("after")])
        if written is not None and body_path(written, cwd) == target:
            text = match.group("body")
    return text


def stdin_ends_with_notice(command):
    """Judge the heredoc a `--body-file -` reads; fall back to presence."""
    match = HEREDOC.search(command)
    if match:
        return ends_with_notice(match.group("body"))
    return re.search(NOTICE_PATTERN, command) is not None


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
    elif (
        written := heredoc_writing(value, command, hook_input.get("cwd"))
    ) is not None:
        ok = ends_with_notice(written)
        where = f" in the heredoc that writes {value}"
    else:
        where = f" in {value}"
        try:
            ok = ends_with_notice(body_path(value, hook_input.get("cwd")).read_text())
        except OSError:
            # Not "add the notice": appending to a file that does not exist yet
            # leaves a body that holds nothing but the notice.
            deny(
                f"The {what} body file {value} does not exist or cannot be read. "
                "This hook runs before the command, so it blocked the whole "
                "command and nothing in it ran - not even an earlier step that "
                "writes the file. Write the body file in a separate step first, "
                f"then run gh {what} on its own."
            )
            return

    if not ok:
        deny(
            f"The {what} body{where} needs the AI-assistance notice as its last "
            f"line. Add this line at the end, then run the command again:\n{NOTICE}"
        )


if __name__ == "__main__":
    main()
