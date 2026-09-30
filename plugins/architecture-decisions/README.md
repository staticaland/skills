# architecture-decisions

Write architecture decision records: decide whether a decision needs one, pick
a template, name the file, and supersede an old record.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install architecture-decisions@staticaland-skills
```

## Skills

- **[architecture-decision-record-skill](./skills/architecture-decision-record-skill/SKILL.md)**
  (skill) - Creates and maintains architecture decision records (ADRs):
  finds or sets up the ADR directory, names the file, picks a template such
  as Nygard or MADR, and records supersession instead of editing an accepted
  record.

## License

CC BY-NC-SA 4.0, the license of the
[upstream repository](https://github.com/architecture-decision-record/architecture-decision-record).
