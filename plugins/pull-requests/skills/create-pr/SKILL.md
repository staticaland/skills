---
name: create-pr
description: >
  Create a GitHub pull request. Use when the user asks to open, create, or
  submit a PR, when work is ready for review, or whenever `gh pr create`
  would otherwise be run.
---

# create-pr

Open a PR whose description lets a reviewer judge the change without having
been in the session.

## Steps

1. Run `<skill-dir>/scripts/pr.py prepare`, where `<skill-dir>` is this
   skill's base directory. It pushes the branch, prints the template to fill,
   and prints the `BODY FILE:` path it created for this run.
2. Fill every template section from the whole session, not the diff alone.
   Cover the original request and the decisions made with their tradeoffs, and
   say what was tested and how. Follow the writing instructions in the template's comments,
   and leave the comments in place - the submit step removes them.
   Give each section the layout below. In the block of the section that tells
   what changed, show the change as a diagram, a diff sketch, or a tree:
   [`references/visuals.md`](references/visuals.md) has the forms.
3. Read the `BODY FILE:` path `prepare` printed with the Read tool - the file
   is an empty placeholder, and the Write tool refuses a file it has not read.
   Then write the filled template to that exact path - never a path of your
   own choosing, which risks reusing a stale body from an earlier session.
   Then run:

   ```bash
   <skill-dir>/scripts/pr.py submit "<title>" <body-file>
   ```

The submit command strips the comments, adds the AI-assistance notice below
the body, and creates the PR through `gh`; the guard hook blocks a
bare `gh pr create`.

## Layout

The layout follows the headings. Every heading in a PR body gets it, and so
does a body rewritten with `gh pr edit`.

The visible part is at most two sentences, and each sentence is its own
paragraph. The longer explanation, lists, and code go in a collapsed block
that adds to those sentences. The `<br>` gives the opened block space below
its summary. GitHub renders the markdown inside only with the two blank lines
around the block's content:

```markdown
## Heading

First sentence.

Second sentence, when the first is not enough.

<details>
<summary>Details</summary>
<br>

Longer explanation.

</details>
```

Leave the block out of a section whose visible sentences say everything.

## Other bodies

For any other PR or issue body, such as `gh issue create` or `gh pr edit`,
write the body file with the Write tool first, then run `gh` as a separate
command.
