---
name: slack-messages
description: Write a message for the user to paste into Slack, in Slack markup (`mrkdwn`) instead of standard Markdown. Use when the user asks for a Slack message, or to turn something from the thread into one.
---

# Slack messages

The user copies the message from this chat and pastes it into Slack. Slack
renders its own markup, not standard Markdown, so write the message in it.

## Output

Put the whole message in one fenced code block, so the user copies the raw
markup and not your chat's rendering of it. When the message contains a
code block, fence the outer block with four backticks.

When the user asks for the message on the clipboard, pipe it to `pbcopy` on
macOS, `wl-copy` on Wayland, or `xclip -selection clipboard` on X11.

## Markup

| Effect        | Write                              |
| ------------- | ---------------------------------- |
| Bold          | `*bold*`                           |
| Italic        | `_italic_`                         |
| Strikethrough | `~struck~`                         |
| Inline code   | `` `code` ``                       |
| Code block    | ` ``` ` on its own lines           |
| Quote         | `>` and a space at the line start  |
| List item     | `-` and a space at the line start  |
| Numbered item | `1.` and a space at the line start |

- Bold takes one asterisk on each side. Double asterisks show up as literal
  asterisks.
- A marker touches the word it wraps and has a space or punctuation outside
  it: `*done*,` renders, `* done *` and `un*done*` do not.
- Start list items with a hyphen and keep lists flat.
- Open a code block with three bare backticks. A language name after them
  shows up as text in the first line.
- For a heading, write a bold line of its own. `#` renders as a literal hash.
- For a table, put aligned plain text in a code block.
- Separate paragraphs with one blank line. One newline is a line break.
- Write links as bare URLs. Slack links them on its own, and `[text](url)`
  renders as literal brackets.
- Write a mention as `@name`. A pasted mention is plain text until the user
  picks the person from Slack's autocomplete, so tell the user which mentions
  to redo.
