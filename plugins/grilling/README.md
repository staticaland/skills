# grilling

Grill a plan until its design tree holds, and write the outcome up as domain
terms and architecture decisions.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install grilling@staticaland-skills
```

## Skills

- **[grilling](./skills/grilling/SKILL.md)** (skill) - Interviews you
  about a plan, decision, or idea, mapping it as a design tree and attacking
  each branch until the thinking holds.
- **[grill-me](./skills/grill-me/SKILL.md)** (skill) - Starts a grilling
  session on the plan or design at hand.
- **[grill-with-docs](./skills/grill-with-docs/SKILL.md)** (skill) -
  Starts a grilling session that writes the outcome up as ADRs and domain terms
  while it runs.
- **[domain-modeling](./skills/domain-modeling/SKILL.md)** (skill) - Pins
  down the words a project uses for its domain in a `CONTEXT.md`, and records
  the decisions behind them as ADRs.

## License

MIT
