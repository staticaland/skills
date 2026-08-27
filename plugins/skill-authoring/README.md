# skill-authoring

Write documents for agents, analyze a skill, prune the prose that changes no
behavior, and split broad references into focused files.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install skill-authoring@staticaland-skills
```

## Skills

- **[writing-for-agents](./skills/writing-for-agents/SKILL.md)**
  (skill) - Guides writing skills, agent instructions, and documents
  reached through context pointers.
- **[skill-analyzer](./skills/skill-analyzer/SKILL.md)** (skill) - Splits
  a skill into scriptable and judgment work: classifies each step as
  deterministic or LLM, proposes a script interface and a simplified SKILL.md.
- **[prune-no-ops](./skills/prune-no-ops/SKILL.md)** (skill) - Deletes
  the sentences in a skill that don't change behavior: asides, justification,
  emphasis, and restated defaults.
- **[progressive-disclosure](./skills/progressive-disclosure/SKILL.md)**
  (skill) - Refactors a skill to load only relevant guidance by splitting
  broad references and mapping concrete project markers to focused files.

## License

MIT
