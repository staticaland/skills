# Skills Marketplace

This repo is a multi-plugin Claude Code marketplace. Each category directory
(`writing/`, `dev/`, `ai/`, or `other/`) is an
independently installable plugin with its own `.claude-plugin/plugin.json`.

## Writing

Always use ASD-STE100 Simplified Technical English for repository prose. Use
short sentences and a controlled, consistent vocabulary. Make direct
statements. Remove hedging and information that the reader does not need.

Follow Zinsser's four principles of quality writing:

1. **Simplicity.** Use familiar words and plain sentence structures.
2. **Brevity.** Remove words that do not help the reader.
3. **Clarity.** Name the actor, action, and object. Use precise references.
4. **Humanity.** Write in a natural and respectful tone.

Before you write or revise repository prose, read
[the forbidden writing patterns](.github/forbidden-patterns.md). Add a new
pattern when review finds a repeatable problem.

## Structure rules

- Every available plugin directory must have an entry in
  `.claude-plugin/marketplace.json` and a section in the top-level `README.md`
  catalog.
- Every plugin has its own `README.md` listing each of its skills and hooks with
  a one-line description. Skill names link to their `SKILL.md`, both in the
  plugin README and in the top-level catalog.
- Every marketplace entry has one lowercase category: `writing`, `dev`, `ai`, or
  `other`. Every published skill and hook in a plugin must belong to that
  category.
- Directories under `in-progress/` (drafts) and `deprecated/` (retired) must NOT
  appear in `marketplace.json` or the top-level README catalog.
- When a plugin's contents change, bump its `version` in both its `plugin.json`
  and its entry in `marketplace.json` - installed users only see updates when
  the version changes.

## Validation

Validate the marketplace structure before committing:

```bash
claude plugin validate .
```
