# github-actions

Run GitHub Actions workflow steps in parallel, replace repeated workflow
configuration with YAML anchors, and name every workflow, job, and step.

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
  configuration a workflow writes twice in the same file and replaces the
  identical copies with YAML anchors and aliases.
- **[workflow-names](./skills/workflow-names/SKILL.md)** (skill) - Checks
  that every GitHub Actions workflow, job, and step has a name, and writes the
  missing ones in imperative, sentence-case style.

## Hooks

The pinact hook that pins action references on workflow edits moved to the
[pinact](../pinact/README.md) plugin. Install that plugin to keep it.

## License

MIT
