---
name: conventional-comments
description: >-
  Post inline review comments on a GitHub pull request in the Conventional
  Comments format, with a `suggestion` block where a concrete replacement
  exists. Use when the user asks to comment on a pull request, or to post a
  review finding or a suggested change as a comment.
---

# conventional-comments

A posted comment notifies the author and speaks for the user in public. Post
only the comments the user asked for. A review you ran on your own ends as a
list of findings in the chat; it becomes comments when the user picks which
ones to post.

## Write each comment

Follow the [Conventional Comments](https://conventionalcomments.org) shape:

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

- **Label** - what the comment asks of the author, from the table below.
- **Decoration** - how firmly the user holds the point. Use `(blocking)` only
  when the user called it a must, and `(non-blocking)` otherwise. `(if-minor)`
  asks for the change only if it stays small. `note`, `nitpick`, and `thought`
  are non-blocking by nature and take no decoration.
- **Subject** - one line, bold with the label, that says what to do.
- **Discussion** - the reason, how the claim was established ("read from the
  template, not tested"), and a link to the source.
- **Suggestion block** - the replacement text, when there is one.

| Label        | Use for                                                  |
| ------------ | -------------------------------------------------------- |
| `suggestion` | an improvement, with what to change and why it is better |
| `issue`      | a specific problem; pair it with a suggestion            |
| `question`   | a concern you are unsure of; ask the author to check     |
| `todo`       | a small change that must happen before merge             |
| `nitpick`    | a trivial preference                                     |
| `praise`     | something done well, said only when it is true           |
| `thought`    | an idea the change sparked, for later                    |
| `note`       | something the reader should know, with nothing to change |
| `chore`      | a process step needed before merge; link the process     |

The site also lists `typo`, `polish`, and `quibble`.

## Check the suggestion block

A `suggestion` block replaces every line the comment covers, so its contents
must be the finished lines:

- Copy the lines' exact leading whitespace. A list item inside a tab block four
  spaces in keeps those four spaces.
- One comment covers one line or one contiguous range. When the same text
  appears in two places, post two comments; the second can say "Same wording as
  in ..." and repeat the block.
- Run the target repository's own linter on the replacement text when it has
  one, such as Vale for prose or the formatter for code. A suggestion that fails
  the repository's CI costs the author a second round.
- Write suggested prose for the reader of that file. Lead with the action the
  reader takes, and drop jargon that reader does not need.

## Done

Each comment the user asked for shows on the pull request with the intended
body on the intended line, and the user has its link.
