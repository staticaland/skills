---
name: slack-messages
description: Write a message for the user to paste into Slack, in Slack markup (`mrkdwn`) instead of standard Markdown. Use when the user asks for a Slack message, or to turn something from the thread into one.
---

# Slack messages

The user copies the message from this chat and pastes it into Slack. Slack
renders its own markup, not standard Markdown, so write the message in it.

Put the whole message in one fenced code block, so the user copies the raw
markup and not your chat's rendering of it.

The user has turned on markup formatting in Slack's preferences. Inside the
message:

- Write bold with one asterisk on each side: `*bold*`. Double asterisks show up
  as literal asterisks.
- For a heading, write a bold line of its own. `#` renders as a literal hash.
- Open a code block with three bare backticks. A language name after them shows
  up as text in the first line.
- For a table, put aligned plain text in a code block.
- Write a link as `[text](url)`. The composer turns it into a link.
- Write a mention as `@name`. A pasted mention is plain text until the user
  picks the person from Slack's autocomplete, so tell the user which mentions
  to redo.
