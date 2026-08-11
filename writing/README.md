# writing

Add sourced footnotes, revise prose for clarity and busy readers, write
controlled technical Norwegian, and lint Markdown with Vale.

Category: `writing`

## Skills

Model-invoked - Claude activates these automatically when the request matches.

- **[writing-revision](./skills/writing-revision/SKILL.md)** - Revises text for
  clarity, scannability, and direct action by busy readers.
- **[kontrollert-norsk](./skills/kontrollert-norsk/SKILL.md)** - Writes or
  revises documentation in controlled technical Norwegian (klarspråk per NS-ISO
  24495-1 with ASD-STE100 principles).
- **[auto-cite-factual-claims](./skills/auto-cite-factual-claims/SKILL.md)** -
  Finds web sources for factual claims and adds them as Markdown footnotes.

## Hooks

- **Vale lint** (`hooks/vale_lint.py`, PostToolUse on Write|Edit) - Runs
  [Vale](https://vale.sh/) on Markdown files after Claude writes or edits them,
  surfacing prose style issues. Requires the `vale` CLI on your PATH.
