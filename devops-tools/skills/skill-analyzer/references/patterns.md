# Extended Patterns and Examples

## Example 1: Analyzing a Writing Revision Skill

Given a skill that revises text for clarity and conciseness:

### Step 1: Inventory

| # | Step |
|---|------|
| 1 | Read the original text completely |
| 2 | Identify the core message and any asks |
| 3 | Restructure to lead with the point |
| 4 | Cut filler words and redundancy |
| 5 | Format for scannability (bullets, bold, headers) |
| 6 | Verify next steps are explicit (if applicable) |
| 7 | Output the revised text directly |

### Step 2: Classification

| # | Step | Category | Rationale |
|---|------|----------|-----------|
| 1 | Read the original text completely | SCRIPT | File I/O with a known path, no interpretation needed |
| 2 | Identify the core message and any asks | LLM | Requires comprehension of meaning and intent |
| 3 | Restructure to lead with the point | LLM | Deciding what "the point" is requires understanding |
| 4 | Cut filler words and redundancy | LLM | While some filler words are mechanical (regex for "just", "basically"), deciding what is redundant requires judgment |
| 5 | Format for scannability | LLM | Choosing where to break text into lists or add headers requires understanding the content structure |
| 6 | Verify next steps are explicit | LLM | Judging whether next steps are clear enough requires understanding of the context |
| 7 | Output the revised text directly | SCRIPT | Writing output to a file or stdout is mechanical |

### Step 3: Proposed Script

```bash
#!/usr/bin/env bash
# writing-revision/scripts/prepare.sh
# Reads input text and writes output to a known location.
# Usage: ./scripts/prepare.sh <input-file>

set -euo pipefail

INPUT_FILE="${1:?Usage: prepare.sh <input-file>}"

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Error: File not found: $INPUT_FILE" >&2
  exit 1
fi

# Read and output the file contents for the LLM to process
cat "$INPUT_FILE"
```

### Step 4: Summary

- **Total steps:** 7
- **SCRIPT:** 2 (29%)
- **LLM:** 5 (71%)
- **Verdict:** This skill is heavily LLM-dependent. The core value is in comprehension and rewriting, which cannot be scripted. The only scriptable parts are file I/O, which are trivial. Extracting scripts here adds complexity without meaningful benefit.

---

## Example 2: Analyzing a Release Notes Skill

Given a skill that generates release notes from git history:

### Step 1: Inventory

| # | Step |
|---|------|
| 1 | Determine the version range (previous tag to HEAD) |
| 2 | Collect git log between the two versions |
| 3 | Group commits by type (feat, fix, chore, etc.) based on conventional commits |
| 4 | Filter out chore/ci commits that don't affect users |
| 5 | Resolve PR numbers and link to the repository |
| 6 | Write a human-readable summary of the release |
| 7 | Highlight breaking changes with migration guidance |
| 8 | Format the output as a markdown changelog entry |
| 9 | Write the changelog to CHANGELOG.md |

### Step 2: Classification

| # | Step | Category | Rationale |
|---|------|----------|-----------|
| 1 | Determine the version range | SCRIPT | `git describe --tags --abbrev=0` gives the previous tag; HEAD is HEAD |
| 2 | Collect git log | SCRIPT | `git log --oneline prev_tag..HEAD` is a fixed command |
| 3 | Group commits by type | SCRIPT | Parse conventional commit prefixes with regex (`^feat:`, `^fix:`, etc.) |
| 4 | Filter out internal commits | LLM | Deciding what "affects users" can be ambiguous; some chores (dependency bumps) may matter |
| 5 | Resolve PR numbers and links | SCRIPT | Parse `(#123)` from commit messages, construct URL from known repo base |
| 6 | Write a human-readable summary | LLM | Requires understanding what changed and why it matters to users |
| 7 | Highlight breaking changes | LLM | Requires understanding the impact of changes and writing migration guidance |
| 8 | Format as markdown changelog | SCRIPT | Template-based rendering with known structure |
| 9 | Write changelog to file | SCRIPT | File write to a known path |

### Step 3: Proposed Script

```bash
#!/usr/bin/env bash
# release-notes/scripts/collect.sh
# Collects and pre-processes git history for release notes.
# Usage: ./scripts/collect.sh [previous-tag]
#
# Output: JSON to stdout with grouped commits and PR links.

set -euo pipefail

REPO_URL=$(git remote get-url origin | sed 's/\.git$//' | sed 's|git@github.com:|https://github.com/|')
PREV_TAG="${1:-$(git describe --tags --abbrev=0 2>/dev/null || echo "")}"

if [[ -z "$PREV_TAG" ]]; then
  RANGE="HEAD"
else
  RANGE="${PREV_TAG}..HEAD"
fi

# Collect commits as JSON array
echo "{"
echo "  \"range\": \"$RANGE\","
echo "  \"repo_url\": \"$REPO_URL\","
echo "  \"commits\": ["

FIRST=true
git log --format="%H%x09%s" "$RANGE" | while IFS=$'\t' read -r hash subject; do
  # Parse conventional commit type
  TYPE="other"
  if [[ "$subject" =~ ^(feat|fix|docs|style|refactor|perf|test|chore|ci|build)\(?.*\)?:\ .* ]]; then
    TYPE="${BASH_REMATCH[1]}"
  fi

  # Parse PR number if present
  PR=""
  if [[ "$subject" =~ \(#([0-9]+)\) ]]; then
    PR="${BASH_REMATCH[1]}"
  fi

  if [[ "$FIRST" == "true" ]]; then
    FIRST=false
  else
    echo ","
  fi

  printf '    {"hash": "%s", "type": "%s", "subject": "%s", "pr": "%s"}' \
    "$hash" "$TYPE" "$subject" "$PR"
done

echo ""
echo "  ]"
echo "}"
```

### Step 4: Proposed Simplified SKILL.md

```markdown
---
name: Release Notes
description: Generate release notes from git history
version: 0.2.0
---

# Release Notes

Generate user-facing release notes from git commit history.

## When to Use

Activate when the user asks to generate release notes, write a changelog,
or summarize what changed between versions.

## Process

1. Run `./scripts/collect.sh [previous-tag]` to gather commit data.
   The script outputs JSON with commits grouped by type and PR links resolved.

2. Review the JSON output. Filter out commits that don't affect end users
   (internal refactors, CI changes, test-only changes). Use judgment:
   dependency bumps may matter if they fix vulnerabilities.

3. Write a human-readable summary of the release. Lead with the most
   impactful changes. Group by: Breaking Changes, New Features, Bug Fixes,
   Other.

4. For any breaking changes, write specific migration guidance explaining
   what users need to change and why.

5. Run `./scripts/format.sh` to render the final markdown and append it
   to CHANGELOG.md.
```

### Step 5: Summary

- **Total steps:** 9
- **SCRIPT:** 5 (56%)
- **LLM:** 4 (44%)
- **Verdict:** This skill benefits significantly from scripting. The git data collection, commit parsing, PR linking, and file formatting are all deterministic. The LLM focuses on the high-value work: deciding what matters to users, writing clear summaries, and explaining breaking changes. This is a good candidate for the split.

---

## Example 3: Analyzing a Branch Naming Skill

Given a skill that creates a branch from an issue description:

### Step 1: Inventory

| # | Step |
|---|------|
| 1 | Read the issue title and body |
| 2 | Determine the branch type (feature, fix, chore) from the issue labels |
| 3 | Generate a slug from the issue title |
| 4 | Assemble the branch name as `type/issue-number-slug` |
| 5 | Check if the branch already exists |
| 6 | Create and switch to the branch |

### Step 2: Classification

| # | Step | Category | Rationale |
|---|------|----------|-----------|
| 1 | Read the issue title and body | SCRIPT | `gh issue view` with known issue number |
| 2 | Determine branch type from labels | SCRIPT | Map label strings to type prefixes with a lookup table |
| 3 | Generate a slug from the title | SCRIPT | Lowercase, replace spaces with hyphens, strip special chars, truncate |
| 4 | Assemble the branch name | SCRIPT | String concatenation with known format |
| 5 | Check if branch exists | SCRIPT | `git branch --list` or `git ls-remote` |
| 6 | Create and switch to the branch | SCRIPT | `git checkout -b` with the computed name |

### Summary

- **Total steps:** 6
- **SCRIPT:** 6 (100%)
- **LLM:** 0 (0%)
- **Verdict:** This skill is entirely deterministic. It should be replaced with a shell script entirely. No SKILL.md is needed; a simple CLI tool covers the full workflow.

---

## Borderline Cases

### Filler Word Removal

Removing known filler words ("just", "basically", "actually") from text can be done with regex. But deciding whether "actually" is filler or a meaningful contrast ("It's not X; it's actually Y") requires LLM judgment. **Classify as LLM** unless the skill explicitly treats all instances the same.

### Template Rendering with Optional Sections

Rendering a template where all variables are known is `SCRIPT`. But if some sections are conditional based on judgment ("include the breaking changes section only if there are breaking changes worth mentioning"), the decision of what to include is `LLM` even though the rendering is `SCRIPT`. **Split the step:** LLM decides which sections to include, script renders the template.

### Code Formatting

Running a formatter like `prettier` or `black` is `SCRIPT`. Deciding whether to format, or choosing between conflicting style options, is `LLM`. Most skills should just run the formatter unconditionally, making the whole step `SCRIPT`.
