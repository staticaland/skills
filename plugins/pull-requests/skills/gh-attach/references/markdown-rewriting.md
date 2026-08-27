# How `gh` rewrites the body

`gh` parses the body as CommonMark. Wherever a link or embed resolves to an
attached file, it edits the destination in place; everything else in the body
survives byte for byte. A file the body never references is appended as its own
paragraph after the edits, in flag order.

Matching is on the resolved absolute path, so `./login.png`, `login.png`, and
an absolute path all name the same attached file.

## Rewritten

| Written in the body                         | After the rewrite                                    |
| ------------------------------------------- | ---------------------------------------------------- |
| `![alt](./login.png)`                       | `![alt](https://.../assets/<uuid>)`                  |
| `[text](./login.png)`                       | `[text](https://.../assets/<uuid>)`                  |
| `![alt](./login.png "Title")`               | title kept, destination swapped                      |
| `![*emphasised* alt](./login.png)`          | formatting inside the label kept                     |
| `![alt](<./Screen Shot.png>)`               | angle brackets around spaces resolved                |
| `![alt](./Screen%20Shot.png)`               | percent-encoded spaces resolved                      |
| `![a](./f(1).png)`, `![a](./f\).png)`       | balanced and escaped parentheses resolved            |
| `![alt][label]` plus `[label]: ./login.png` | the definition is rewritten                          |
| `![shot][]`, `![shot]`                      | collapsed and shortcut forms, through the definition |
| `[![thumb](./login.png)](./login.png)`      | both destinations                                    |

Each definition with that destination is rewritten, including a spare label
nothing uses.

## Left alone

- A path inside a fenced block, an indented code block, or an inline code span.
- A remote URL, an anchor such as `[jump](#login.png)`, and any local path that
  no `--attach` argument named.
- A destination CommonMark doesn't parse as a link: an unbalanced opening
  parenthesis, an unbracketed space, an unclosed angle bracket.
- Every reference to a file whose upload failed, so a partially written body
  still points at the local paths for the files that never uploaded.

## Video, degraded

A video embed that cannot stand alone in its paragraph is turned into a link,
which costs the `!` and gains the filename where the body doesn't write alt
text:

| Written in the body                                 | After the rewrite                                                  |
| --------------------------------------------------- | ------------------------------------------------------------------ |
| `![the recording](./clip.mp4)` alone in a paragraph | `https://.../assets/<uuid>`                                        |
| `text ![the recording](./clip.mp4) text`            | `text [the recording](URL) text`                                   |
| `text ![](./clip.mp4)`                              | `text [clip.mp4](URL)`                                             |
| `!![the recording](./clip.mp4)`                     | `\![the recording](URL)`, so the stray `!` cannot re-form an embed |

Alt text that a degraded video would drop is discarded with the embed. A link
or an image nested inside that alt text is still rewritten in place.

## Alt text safety

Alt text is escaped before it reaches the body: `\`, `[`, and `]` gain a
backslash, and a newline becomes a space. `gh` then renders the image with a
stand-in URL and parses it back; alt text that still escapes the image syntax
fails validation before any upload runs.
