# Staticaland Skills

Skills and hooks for Claude Code, shipped as a marketplace of small, single-purpose plugins. Install only the plugins you want — each one is an independent bundle.

## Install

Add the marketplace, then install individual plugins:

```
/plugin marketplace add staticaland/skills
/plugin install writing-tools@staticaland-skills
/plugin install learning-tools@staticaland-skills
/plugin install devops-tools@staticaland-skills
```

## Plugins

### [writing-tools](./writing-tools/README.md)

Tools for revising and improving written communication.

- **[writing-revision](./writing-tools/skills/writing-revision/SKILL.md)** (skill) — Revises text to be clear, scannable, and action-oriented for busy readers.
- **Vale lint** (hook) — Runs [Vale](https://vale.sh/) on Markdown files after Claude writes or edits them. Requires the `vale` CLI.

### [learning-tools](./learning-tools/README.md)

Tools for creating study materials and enhancing learning.

- **[anki-flashcards](./learning-tools/skills/anki-flashcards/SKILL.md)** (skill) — Creates effective Anki flashcards from text, documents, or images for spaced repetition learning.

### [devops-tools](./devops-tools/README.md)

Tools for securing and automating CI/CD workflows.

- **[skill-analyzer](./devops-tools/skills/skill-analyzer/SKILL.md)** (skill) — Splits a skill into scriptable and judgment work: classifies each step as deterministic or LLM, proposes a script interface and a simplified SKILL.md.
- **pinact** (hook) — Pins GitHub Actions references to full commit SHAs with [pinact](https://github.com/suzuki-shunsuke/pinact) after Claude writes or edits workflow files. Requires the `pinact` CLI.

## Repo layout

- Each top-level plugin directory ships as one marketplace entry.
- [`in-progress/`](./in-progress/README.md) holds drafts not yet shipped.
- [`deprecated/`](./deprecated/README.md) holds retired plugins kept for reference.

## Development

Validate before committing:

```bash
claude plugin validate .
```

## License

MIT
