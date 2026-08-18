#!/usr/bin/env python3
"""Deterministic halves of the create-pr skill.

Usage:
  pr.py prepare
    Pushes the branch, then prints the template to fill: the repo's
    .github/PULL_REQUEST_TEMPLATE.md if it exists, otherwise this
    skill's references/pr-template.md. Comments stay in - they carry
    the writing instructions. Also prints a body file path in a fresh
    /tmp directory, so no leftover file from an earlier session can be
    submitted by mistake. The path does not exist yet - writing it
    creates it, so an overwrite guard never fires.

  pr.py submit <title> <body-file>
    Strips HTML comments from <body-file>, then creates the PR with the
    SKILL_CREATE_PR=1 marker the guard hook requires.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def prepare() -> None:
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)

    skill_dir = Path(__file__).resolve().parent.parent
    template = skill_dir / "references" / "pr-template.md"
    repo_root = Path(
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )
    repo_template = repo_root / ".github" / "PULL_REQUEST_TEMPLATE.md"
    if repo_template.is_file():
        template = repo_template

    body_file = Path(tempfile.mkdtemp(prefix="pr-body-", dir="/tmp")) / "body.md"

    print(f"TEMPLATE: {template}")
    print(f"BODY FILE: {body_file}")
    print(template.read_text(), end="")


def submit(title: str, body_file: str) -> None:
    path = Path(body_file)
    if not path.is_file():
        sys.exit(f"Error: no such file: {body_file}")

    body = re.sub(r"<!--.*?-->\n?", "", path.read_text(), flags=re.DOTALL)
    if not body.strip():
        sys.exit(f"Error: body file is empty: {body_file}")

    subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body-file", "-"],
        check=True,
        input=body,
        text=True,
        env={**os.environ, "SKILL_CREATE_PR": "1"},
    )


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ["prepare"] and len(args) == 1:
        prepare()
    elif args[:1] == ["submit"] and len(args) == 3:
        submit(args[1], args[2])
    else:
        sys.exit("Usage: pr.py {prepare | submit <title> <body-file>}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
