# ai

Analyze skills, prune no-op prose, refactor references, write documents for
agents, and retrospect on a coding session to improve the environment the next
one runs in.

Category: `ai`

## Skills

- **[progressive-disclosure](./skills/progressive-disclosure/SKILL.md)** -
  Refactors a skill to load only relevant guidance by splitting broad references
  and mapping concrete project markers to focused files.
- **[prune-no-ops](./skills/prune-no-ops/SKILL.md)** - Deletes the sentences in
  a skill that don't change behavior: asides, justification, emphasis, and
  restated defaults.
- **[retro](./skills/retro/SKILL.md)** - Reviews a coding session and ranks the
  changes that would make the next one go better: navigation pointers,
  automated checks, coding standards, and tool economy.
- **[skill-analyzer](./skills/skill-analyzer/SKILL.md)** - Splits a skill into
  scriptable and judgment work: classifies each step as deterministic or LLM,
  proposes a script interface and a simplified SKILL.md.
- **[writing-for-agents](./skills/writing-for-agents/SKILL.md)** - Guides writing
  skills, agent instructions, and documents reached through context pointers.

### Install individual skills

```bash
npx skills add staticaland/skills --skill progressive-disclosure
npx skills add staticaland/skills --skill prune-no-ops
npx skills add staticaland/skills --skill retro
npx skills add staticaland/skills --skill skill-analyzer
npx skills add staticaland/skills --skill writing-for-agents
```
