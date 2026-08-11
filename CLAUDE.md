# Skills Marketplace

This repo is a multi-plugin Claude Code marketplace. Each top-level plugin
directory (`writing-tools/`, `learning-tools/`, `devops-tools/`, ...) is an
independently installable plugin with its own `.claude-plugin/plugin.json`.

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
