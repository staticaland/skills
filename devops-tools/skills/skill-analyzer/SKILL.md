---
name: skill-analyzer
description: Split a skill into scriptable and judgment work, proposing a script interface and a simplified SKILL.md.
disable-model-invocation: true
version: 0.2.0
---

# Skill Analyzer

Classify every step of a target skill as `SCRIPT` (deterministic) or `LLM` (judgment), then propose a script interface and a simplified SKILL.md.

Deliver the analysis in the response. Write the script and simplified SKILL.md to disk only when the user asks to apply the changes.

## Process

### 1. Inventory the steps

Read the target skill and list every discrete action, instruction, or decision point as a numbered step — including implicit steps the skill assumes (e.g. "read the file" before "edit the file"). Done when no instruction in the skill is left unaccounted for.

### 2. Classify each step

One test: could a script perform this step **blind** — producing the correct result for all valid inputs without reading or understanding anything?

- Blind → `SCRIPT`: CLI commands with known arguments, file I/O on known paths, regex and template transforms, git operations with known names.
- Not blind → `LLM`: interpreting intent, choosing between valid outputs, evaluating quality, generating prose, resolving ambiguous references.

When in doubt, classify `LLM` — judgment kept in the SKILL.md beats a brittle script. For borderline patterns (filler-word removal, conditional templates, formatters) and worked end-to-end examples, see [references/patterns.md](references/patterns.md).

Output one row per step:

```
| # | Step | Category | Rationale |
```

Done when every inventoried step has a category and a rationale.

### 3. Propose the script

Collect the `SCRIPT` steps into one shell or Python script, full source in a fenced block with a usage comment header. The script takes explicit inputs (paths, flags), produces deterministic outputs (files, stdout, exit codes), fails loudly on invalid input, and is invocable from a single SKILL.md instruction like "Run `./scripts/prepare.sh <input>`".

### 4. Propose the simplified SKILL.md

Rewrite the target SKILL.md: keep the frontmatter and every `LLM` step; replace the `SCRIPT` steps with the single instruction that invokes the script. The remaining LLM work is input resolution, judgment calls, and quality evaluation.

### 5. Summarize the split

Report the step counts and `SCRIPT`/`LLM` percentages, then a verdict: is the split worth it? Name each borderline step and the risk if its inputs vary more than assumed.
