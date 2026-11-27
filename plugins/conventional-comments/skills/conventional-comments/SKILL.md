---
name: conventional-comments
description: >-
  Post inline review comments on a GitHub pull request in the Conventional
  Comments format, with a `suggestion` block where a concrete replacement
  exists. Use when the user asks to comment on a pull request, or to post a
  review finding or a suggested change as a comment.
---

# conventional-comments

Post only the comments the user asked for. A review you ran on your own ends
as a list of findings in the chat; it becomes comments when the user picks
which ones to post.

## Write each comment

Follow the [Conventional Comments](https://conventionalcomments.org) format:

````markdown
**suggestion (non-blocking):** Say that automerge covers Renovate pull requests only.

Automerge applies to Renovate pull requests only: the workflow adds an
`automerge` label and Renovate merges ([README](https://example.com/readme#automerge)).
"No pull request merges automatically" reads as if ordinary pull requests
would merge too.

```suggestion
    1. Replace `<dir>` with the directory of your `dev` stacks. Until you do, no Renovate pull request merges automatically.
```
````

- Use `(blocking)` only when the user called the point a must, and
  `(non-blocking)` otherwise.
- In the discussion, say how the claim was established ("read from the
  template, not tested") and link the source.
- Copy the commented lines' exact leading whitespace into the `suggestion`
  block. The block replaces those lines, so a list item four spaces in keeps
  its four spaces.
- Run the target repository's own linter on the replacement text when it has
  one, such as Vale for prose or the formatter for code.

## Done

Each comment the user asked for shows on the pull request with the intended
body on the intended line, and the user has its link.
