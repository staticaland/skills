# github-actions

Run GitHub Actions workflow steps in parallel, name every workflow, job,
and step, and pin every action reference to a commit SHA on workflow edits.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install github-actions@staticaland-skills
```

## Skills

- **[parallel-steps](./skills/parallel-steps/SKILL.md)** (skill) - Makes
  GitHub Actions workflow steps run in parallel with the `background`, `wait`,
  `cancel`, and `parallel` keywords, written in ASD-STE100 Simplified Technical
  English.
- **[workflow-names](./skills/workflow-names/SKILL.md)** (skill) - Checks
  that every GitHub Actions workflow, job, and step has a name, and writes the
  missing ones in imperative, sentence-case style.

## Hooks

- **pinact** (`hooks/pinact_actions.py`) - Pins GitHub Actions references
  to full commit SHAs with [pinact](https://github.com/suzuki-shunsuke/pinact)
  after Claude writes or edits workflow files. Requires the `pinact` CLI.

## License

MIT
