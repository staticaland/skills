---
name: slack-messages
description: Format text in Slack markup (`mrkdwn`) instead of standard Markdown. Use when writing a Slack message, thread reply, DM, or channel post, or text a Slack bot, webhook, or API call sends.
---

# Slack messages

Slack renders its own markup, not standard Markdown. Write every message in it.

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

## Links and mentions

In text the user pastes into Slack, write bare URLs. Slack links them on its
own.

In text a bot, webhook, or API call sends:

- Link with `<https://example.com|link text>`. `[text](url)` renders as
  literal brackets.
- Mention a user with `<@U012AB3CD>`, a channel with `<#C012AB3CD>`, and
  everyone present with `<!here>`. Plain `@name` stays plain text.
- Escape `&`, `<`, and `>` as `&amp;`, `&lt;`, and `&gt;`.
