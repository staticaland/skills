# github-actions

Run GitHub Actions workflow steps in parallel, replace repeated workflow
configuration with YAML anchors, and pin every action reference to a commit SHA
on workflow edits.

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
- **[yaml-anchors](./skills/yaml-anchors/SKILL.md)** (skill) - Finds the
  configuration a workflow writes twice, replaces the identical in-file copies
  with YAML anchors and aliases, and routes the rest to a matrix, composite
  action, reusable workflow, or workflow template.

## Hooks

- **pinact** (`hooks/pinact_actions.py`) - Pins GitHub Actions references
  to full commit SHAs with [pinact](https://github.com/suzuki-shunsuke/pinact)
  after Claude writes or edits workflow files. Requires the `pinact` CLI.

## License

MIT
