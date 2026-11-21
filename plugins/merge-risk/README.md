# merge-risk

Rate the risk of merging a pull request as low, medium, or high from its
alignment, impact, verification, rollback cost, and error detection.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install merge-risk@staticaland-skills
```

## Skills

- **[merge-risk](./skills/merge-risk/SKILL.md)** (skill) - Grades a pull
  request on five categories, weights them into one low, medium, or high merge
  risk, and lists the gaps behind each verdict.

## License

MIT
