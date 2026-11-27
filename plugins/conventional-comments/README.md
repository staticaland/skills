# conventional-comments

Post inline review comments on a GitHub pull request in the
[Conventional Comments](https://conventionalcomments.org) format, with
`suggestion` blocks for concrete replacements.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install conventional-comments@staticaland-skills
```

## Skills

- **[conventional-comments](./skills/conventional-comments/SKILL.md)**
  (skill) - Writes each comment as a label, a decoration, a subject, and a
  sourced discussion with a `suggestion` block, posts them as one review
  through `gh api`, and reads each one back by its id.

## License

MIT
