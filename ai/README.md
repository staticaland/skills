# ai

Analyze skills, prune no-op prose, refactor references, and write documents for
agents.

Category: `ai`

## Skills

- **[progressive-disclosure](./skills/progressive-disclosure/SKILL.md)** -
  Refactors a skill to load only relevant guidance by splitting broad references
  and mapping concrete project markers to focused files.
- **[prune-no-ops](./skills/prune-no-ops/SKILL.md)** - Deletes the sentences in
  a skill that change no behavior: asides, justification, emphasis, and
  restated defaults.
- **[skill-analyzer](./skills/skill-analyzer/SKILL.md)** - Splits a skill into
  scriptable and judgment work: classifies each step as deterministic or LLM,
  proposes a script interface and a simplified SKILL.md.
- **[writing-for-agents](./skills/writing-for-agents/SKILL.md)** - Guides writing
  skills, agent instructions, and documents reached through context pointers.

### Install individual skills

```bash
npx skills add staticaland/skills --skill progressive-disclosure
npx skills add staticaland/skills --skill prune-no-ops
npx skills add staticaland/skills --skill skill-analyzer
npx skills add staticaland/skills --skill writing-for-agents
```
