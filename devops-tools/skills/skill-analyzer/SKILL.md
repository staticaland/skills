---
name: Skill Analyzer
description: This skill should be used when the user asks to "analyze a skill", "break down a skill", "find what can be scripted", "separate deterministic from LLM parts", "extract scripts from a skill", "simplify a SKILL.md", or wants to identify which parts of a skill require LLM judgment versus mechanical automation.
version: 0.1.0
---

# Skill Analyzer

Analyze any skill to classify each step as deterministic (scriptable) or requiring LLM judgment, then propose a script interface and a simplified SKILL.md.

## When to Use

Activate this skill when the user:

- Asks to analyze or break down a skill's steps
- Wants to know which parts of a skill can be automated
- Wants to extract deterministic work into scripts
- Asks to simplify or modularize a SKILL.md
- Wants to separate mechanical steps from judgment calls

## Output Behavior

**Default output:** Provide the full analysis directly in the response, structured into the three sections described below (Classification Table, Script Interface, Simplified SKILL.md).

**File input:** When the user points to a specific SKILL.md file, read it and produce the analysis. When the user asks to apply changes, write the proposed script and simplified SKILL.md to disk.

---

## Analysis Process

### Step 1: Read and Inventory Steps

Read the skill completely. Extract every discrete action, instruction, or decision point as a numbered step. Include implicit steps (e.g., "read the file" before "edit the file") that the skill assumes.

### Step 2: Classify Each Step

For each step, assign exactly one category:

| Category | Label | Definition | Examples |
|----------|-------|------------|----------|
| Deterministic | `SCRIPT` | Predictable outcome. No judgment, interpretation, or context-sensitivity needed. Inputs and outputs are well-defined. | Running a CLI command, string replacement in a file, creating a branch with a known name, formatting output to a fixed template, copying a file, reading a path from config |
| Requires LLM | `LLM` | Requires inference, interpretation, or context-dependent reasoning. The correct action depends on understanding meaning, not just following a rule. | Deciding which repo to target, judging if a user's request is complete, interpreting vague instructions, choosing between approaches, evaluating quality, summarizing content, generating prose |

**Deciding between the two:**

- If you can write a bash/python script that handles the step correctly for all valid inputs without needing to "understand" anything, it is `SCRIPT`.
- If a human (or LLM) would need to read and think about the context to do the step correctly, it is `LLM`.
- When in doubt, classify as `LLM`. It is better to keep judgment in the SKILL.md than to force a brittle script.

### Step 3: Produce the Classification Table

Output a table with one row per step:

```
| # | Step | Category | Rationale |
|---|------|----------|-----------|
| 1 | Read the input file | SCRIPT | File path is provided, no interpretation needed |
| 2 | Identify the core message | LLM | Requires comprehension of meaning |
| ...| ... | ... | ... |
```

### Step 4: Propose a Script Interface

Group all `SCRIPT` steps into a proposed shell or Python script. The script should:

- Accept clear inputs (file paths, flags, config values)
- Produce deterministic outputs (files on disk, stdout, exit codes)
- Fail loudly on bad input rather than guessing
- Be invocable from a SKILL.md instruction like "Run `./scripts/prepare.sh <input>`"

Provide the full script source in a fenced code block. Include a brief comment header describing what it does and what inputs it expects.

### Step 5: Propose a Simplified SKILL.md

Write a new SKILL.md that:

1. Keeps the same YAML frontmatter (name, description, version)
2. Keeps all `LLM` steps as instructions for the LLM to follow
3. Replaces `SCRIPT` steps with a single instruction to invoke the script, e.g., "Run `./scripts/prepare.sh <path>` to set up the workspace"
4. Preserves the skill's original intent and quality bar
5. Focuses the LLM's work on input resolution, judgment calls, and quality evaluation

### Step 6: Summarize the Split

End with a summary:

- Total steps identified
- Count and percentage of `SCRIPT` steps
- Count and percentage of `LLM` steps
- Key tradeoffs or risks in the proposed split (e.g., "Step 5 is borderline; if input formats vary widely, it may need LLM handling")

---

## Classification Principles

### What Makes a Step Deterministic

A step is deterministic when:

- The **input is known or provided** (file path, config value, flag)
- The **transformation is rule-based** (regex, template, CLI command)
- The **output is predictable** (same input always produces same output)
- **No understanding of meaning** is required

Common deterministic operations:

- File I/O (read, write, copy, move, delete)
- Running CLI tools with known arguments
- String replacement, regex transforms
- Template rendering with provided variables
- Git operations (branch, commit, push) with known names
- Directory scaffolding (mkdir, touch)
- Format conversion between known schemas

### What Requires LLM Judgment

A step requires LLM judgment when:

- The **input is ambiguous or incomplete** (natural language, vague request)
- The **correct action depends on understanding context** (what the user meant, what the code does)
- **Multiple valid outputs exist** and choosing between them requires reasoning
- **Quality evaluation** is needed (is this good enough? does this match the intent?)

Common LLM-dependent operations:

- Interpreting user intent from a natural language request
- Deciding what information to include or exclude
- Evaluating whether output meets a quality bar
- Choosing between multiple valid approaches
- Generating prose, summaries, or explanations
- Resolving ambiguous references ("the main config" could mean several files)
- Adapting instructions to a specific codebase or context

---

## Additional Resources

For detailed examples of analyzing real skills:

- [references/patterns.md](references/patterns.md) - Worked examples showing the full analysis process applied to sample skills
