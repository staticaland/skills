---
name: write-skill
description: Skill work in this marketplace repo - drafting a new skill, revising an existing SKILL.md, or the plugin packaging that ships it.
tools: ["read", "edit", "search", "execute", "github/*"]
---

Every skill here belongs to a marketplace plugin, so a change is complete only once the writing and packaging are both done.

## Write

Read `.agents/skills/writing-for-agents/SKILL.md` before drafting or editing any `SKILL.md`, and apply every lever it names - it is the standard this repo holds its skills to. `SKILL-MECHANICS.md` beside it covers frontmatter, invocation, and router skills.

## Package

Read `CLAUDE.md` for the structure rules binding a plugin's `plugin.json`, its `marketplace.json` entry, the plugin README, and the top-level catalog. Apply every rule to every plugin your change touches.

## Verify

Run `claude plugin validate .` and clear every finding. Run `vale` over each file you changed - the Vale workflow runs the same check on push, so a finding you leave becomes a red check on the pull request.
