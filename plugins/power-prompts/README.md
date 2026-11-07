# power-prompts

One-sentence prompts that change how the agent attacks a problem, each a skill
you invoke by name.

The agent never loads these on its own. Invoke one, and optionally name the
task after it: `/power-prompts:day-one-test the new cache layer`.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install power-prompts@staticaland-skills
```

## Skills

<!-- vale ai-tells.FillerIntensifier = NO -->
<!-- The prompts are quoted verbatim. -->

- **[abstract-thinking](./skills/abstract-thinking/SKILL.md)** (skill) -
  "Exercise abstract thinking when considering this task."
- **[irreducible-constraints](./skills/irreducible-constraints/SKILL.md)**
  (skill) - "Reduce this problem to its irreducible constraints and rebuild it
  from zero."
- **[principal-architect](./skills/principal-architect/SKILL.md)** (skill) -
  "What would a principal architect immediately rewrite before even starting
  this?"
- **[day-one-test](./skills/day-one-test/SKILL.md)** (skill) - "Design the
  single test that breaks this design on day one."
- **[make-it-disappear](./skills/make-it-disappear/SKILL.md)** (skill) - "What
  higher-level abstraction would make this entire problem disappear?"
- **[implicit-state-machines](./skills/implicit-state-machines/SKILL.md)**
  (skill) - "Find all of the implicit state machines in this app."

<!-- vale ai-tells.FillerIntensifier = YES -->

## Sources

Steve Ruiz posted the implicit state machines prompt on X. Wyrmfalls posted the
other five in reply to a call for a collection of prompts like it.

## License

MIT
