# plain-language

Restate a message in plain human language, ask for a re-pitch when it does
not land, or have the agent restate your intent before it continues.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install plain-language@staticaland-skills
```

## Skills

- **[bro](./skills/bro/SKILL.md)** (skill) - Restates the last message in
  plain human language, with no jargon.
- **[wait-what](./skills/wait-what/SKILL.md)** (skill) - Asks for a
  re-pitch of the last message, in Simplified Technical English and the
  project's own domain terms.
- **[restate-intent](./skills/restate-intent/SKILL.md)** (skill) - Asks
  the agent to restate your goals and the problem you're solving, then wait
  for you to confirm. Useful after dictating a long, rambling prompt.

## License

MIT
