# upgrade-path

Work toward the next major framework upgrade in small, bounded steps with the
Mikado Method, tracked in `UPGRADE-PATH.md`.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install upgrade-path@staticaland-skills
```

## Skills

- **[upgrade-path](./skills/upgrade-path/SKILL.md)** (skill) - Each run either
  explores, attempting the upgrade and recording each breakage as a blocker in a
  Mikado graph before reverting, or executes, fixing one leaf blocker and
  committing it on a green build.

## License

MIT
