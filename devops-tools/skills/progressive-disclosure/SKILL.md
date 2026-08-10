---
name: progressive-disclosure
description: Refactor a Claude Code skill so it loads only relevant guidance, splitting broad references by concrete project marker and repairing links. Use when a skill has large mixed-topic references, loads irrelevant context, or needs progressive disclosure.
disable-model-invocation: true
version: 0.1.0
---

# Progressive Disclosure

Refactor one target skill so its core workflow stays in `SKILL.md` and conditional detail loads only when it applies. Preserve the skill's behavior and guidance; reduce only irrelevant context.

Apply the refactor unless the user asks for analysis only.

## Process

### 1. Trace the current loading paths

Read the target `SKILL.md` and every file it links. Find inbound links to those files across the plugin.

Inventory each distinct topic, where it lives, and what makes it relevant. Include concrete project markers such as filenames, config keys, commands, tool names, and user-selected modes.

Do not use file length alone as the reason to split. Done when every topic is marked either always needed or conditional, and every conditional topic has an observable relevance condition.

### 2. Choose the disclosure boundaries

Keep the core procedure, safety constraints, and guidance needed on every invocation in `SKILL.md`. Put conditional implementation detail in references.

Create one reference for each topic that can apply independently. Keep topics together when they always apply together or separating them would force readers through chains of references. Name split files for their narrow scope, using a shared prefix when it makes the grouping clear, such as `python_uv.md` and `python_pip.md`.

Done when loading any proposed reference does not also load substantial guidance for an inapplicable topic.

### 3. Build the reference dispatch

Place discovery before reference loading. Map each relevance condition directly to the narrowest reference:

```markdown
Read only the files for the markers present:

| Marker | Reference |
| --- | --- |
| `tool.lock`, `[tool.example]` | [tool_example.md](references/tool_example.md) — Example Tool |
```

Use precise markers. If a filename can represent several tools, instruct the reader to inspect the distinguishing config key and load only the matching row. For topics with no filesystem marker, use an explicit user choice or a condition discovered by the core procedure.

Do not retain a catch-all link that loads the split references as a group. Done when every conditional topic maps to a reference and each reference has a specific loading condition.

### 4. Split without losing guidance

Move each topic into its focused reference. Preserve its facts, examples, caveats, attribution, and source links. Keep small prerequisites with the guidance that needs them when doing so avoids an extra load.

Update all links that pointed to the old file, including links between references. Delete the old file only after all of its content and inbound links are accounted for.

Done when the new files collectively preserve the old guidance and no link still names a removed file.

### 5. Update versions and catalogs

Bump the target skill's version. If the repository versions its enclosing plugin or marketplace entry, bump every synchronized version declaration and update catalogs when the skill list or plugin description changed.

### 6. Verify the disclosure

Check every Markdown link and search the repository for removed filenames. Run the repository's existing skill or plugin validator.

Walk through at least these loading cases:

1. One marker loads one focused reference.
2. Multiple markers load only the union of their references.
3. An ambiguous filename loads nothing until its contents identify the matching topic.
4. No marker leaves the core workflow usable without loading conditional guidance.

Report the old and new reference layout, the marker-to-reference mapping, the versions changed, and the validation result.
