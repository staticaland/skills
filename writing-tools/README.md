# writing-tools

Revise prose for clarity and busy readers, with automatic Vale linting of Markdown files on every edit.

## Skills

Model-invoked — Claude activates these automatically when the request matches.

- **[writing-revision](./skills/writing-revision/SKILL.md)** — Revises text to be clear, scannable, and action-oriented for busy readers.

## Hooks

- **Vale lint** (`hooks/vale_lint.py`, PostToolUse on Write|Edit) — Runs [Vale](https://vale.sh/) on Markdown files after Claude writes or edits them, surfacing prose style issues. Requires the `vale` CLI on your PATH.
