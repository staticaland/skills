#!/usr/bin/env python3
"""Deterministic halves of the create-pr skill.

Usage:
  pr.py prepare
    Pushes the branch, then prints the template to fill: this skill's
    references/pr-template.md. Comments stay in - they carry
    the writing instructions. Also creates an empty, uniquely named
    body file in /tmp and prints its path, so no leftover file from an
    earlier session can be submitted by mistake.

  pr.py submit [--model <model>] <title> <body-file>
    Strips HTML comments from <body-file>, puts the AI-assistance notice
    on its last line, then creates the PR with the
    SKILL_CREATE_PR=1 marker the guard hook requires.

    The notice names the model that wrote the PR. The model the
    session_model hook recorded for this session comes first, since the
    harness reported it. --model is used when there is no record: in
    Codex, or after /clear in Claude Code. With neither, the notice
    names no model.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PLUGIN_ROOT / "hooks"))

from ai_assisted_notice import wrap  # noqa: E402
from session_model import display_name, lookup  # noqa: E402

USAGE = "Usage: pr.py {prepare | submit [--model <model>] <title> <body-file>}"


def prepare() -> None:
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)

    skill_dir = Path(__file__).resolve().parent.parent
    template = skill_dir / "references" / "pr-template.md"

    fd, body_file = tempfile.mkstemp(prefix="pr-body-", suffix=".md", dir="/tmp")
    os.close(fd)

    print(f"TEMPLATE: {template}")
    print(f"BODY FILE: {body_file}")
    print(template.read_text(), end="")


def model_name(stated: str | None) -> str | None:
    """The model to name in the notice, or None when it is not known."""
    try:
        recorded = lookup(os.environ.get("CLAUDE_CODE_SESSION_ID"))
        return display_name(recorded) or display_name(stated)
    except Exception:  # noqa: BLE001 - a missing name must not stop the PR
        return None


def submit(title: str, body_file: str, model: str | None = None) -> None:
    path = Path(body_file)
    if not path.is_file():
        sys.exit(f"Error: no such file: {body_file}")

    body = re.sub(r"<!--.*?-->\n?", "", path.read_text(), flags=re.DOTALL)
    if not body.strip():
        sys.exit(f"Error: body file is empty: {body_file}")

    subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body-file", "-"],
        check=True,
        input=wrap(body, model_name(model)),
        text=True,
        env={**os.environ, "SKILL_CREATE_PR": "1"},
    )


def take_model(args: list[str]) -> tuple[str | None, list[str]]:
    """Split a --model <model> or --model=<model> option off args."""
    for index, arg in enumerate(args):
        if arg == "--model" and index + 1 < len(args):
            return args[index + 1], args[:index] + args[index + 2 :]
        if arg.startswith("--model="):
            return arg.partition("=")[2], args[:index] + args[index + 1 :]
    return None, args


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ["prepare"] and len(args) == 1:
        prepare()
        return
    model, rest = take_model(args)
    if rest[:1] == ["submit"] and len(rest) == 3:
        submit(rest[1], rest[2], model)
    else:
        sys.exit(USAGE)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
