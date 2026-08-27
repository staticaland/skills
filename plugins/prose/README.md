# prose

Revise prose for clarity and busy readers, add sourced footnotes, strip
references the reader cannot see, and lint Markdown with Vale.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install prose@staticaland-skills
```

## Skills

- **[writing-revision](./skills/writing-revision/SKILL.md)** (skill) -
  Makes text clear, scannable, and action-oriented for busy readers.
- **[Auto-cite Factual Claims](./skills/auto-cite-factual-claims/SKILL.md)**
  (skill) - Finds web sources for the factual claims a document rests
  on and adds them as Markdown footnotes.
- **[standalone](./skills/standalone/SKILL.md)** (skill) - Strips
  references the reader cannot see - "as discussed", "the old
  handler" - from prose and code comments.

## Hooks

- **Vale lint** (`hooks/vale_lint.py`) - Runs [Vale](https://vale.sh/) on
  Markdown files after Claude writes or edits them. Requires the `vale` CLI.

## License

MIT
