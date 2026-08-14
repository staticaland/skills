# writing

Add sourced footnotes, revise prose for clarity and busy readers, strip
references the reader cannot see, write controlled technical Norwegian, and
lint Markdown with Vale.

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

User-invoked - run these by name.

- **[standalone](./skills/standalone/SKILL.md)** - Strips references the reader
  cannot see - "as discussed", "the old handler" - from prose and code
  comments.

### Install individual skills

```bash
npx skills add staticaland/skills --skill writing-revision
npx skills add staticaland/skills --skill kontrollert-norsk
npx skills add staticaland/skills --skill auto-cite-factual-claims
npx skills add staticaland/skills --skill standalone
```

## Hooks

- **Vale lint** (`hooks/vale_lint.py`, PostToolUse on Write|Edit) - Runs
  [Vale](https://vale.sh/) on Markdown files after Claude writes or edits them,
  surfacing prose style issues. Requires the `vale` CLI on your PATH.
