# Vale styles and vocabulary

This directory backs [`.vale.ini`](../.vale.ini). The `Skills` style and the
`Skills` vocabulary live here as source; the `ai-tells` and `ai-tells-commits`
styles are synced from the packages `.vale.ini` names and are committed so CI
runs without a download.

## Vocabulary vs. formatting

The vocabulary in
[`styles/config/vocabularies/Skills/accept.txt`](styles/config/vocabularies/Skills/accept.txt)
is a spelling allowlist. It answers one question, whether a string is a typo,
and tells the spell-checker to accept terms such as Renovate or Staticaland. It
does not decide how a term looks in prose.

How to typeset a term is a separate editorial decision, governed by the
use-mention distinction: does the text use a word for its meaning, or mention
the literal string itself? English marks mention with typography:

| Presentation       | Name           | Use for                                                                                                |
| ------------------ | -------------- | ------------------------------------------------------------------------------------------------------ |
| `backticks`        | code font      | Literal strings the reader types or the machine reads: commands, flags, filenames, identifiers, values |
| _italics_          | words-as-words | Naming a term _as a term_, or introducing a new one before defining it                                 |
| "quotes"           | quotation      | Actual quotations. Avoid for terminology, where scare quotes read as sneering                          |
| plain, capitalized | brand name     | Products, services, and organizations such as Renovate, Anki, Homebrew, Docker                         |

Rule of thumb: if a reader would copy-paste or type it, use code font. If it
is a name they would say out loud, leave it plain. Quotes almost never.

### Backticks hide text from Vale

Vale's default [`IgnoredScopes`](https://docs.vale.sh/keys/ignoredscopes)
covers the inline `code` scope, and
[`SkippedScopes`](https://docs.vale.sh/keys/skippedscopes) covers fenced code
blocks, so anything in backticks never reaches the spell-checker or any other
rule. Italics and quotes are still linted.

A code-voice term rarely needs a vocabulary entry at all. An entry
for a term meant for backticks (`prek`, `pinact`, `uv`) tells you that term
appears bare somewhere Vale still reads, since inside backticks it would never
reach the linter. Link text such as `[prek](https://prek.j178.dev/)` in the
plugin READMEs is the usual source. Bare prose that wants backticks is the
other. Before adding or trusting such an entry, check the source and prefer
fixing the prose over enshrining a bare usage.

Genuine allowlist material is what legitimately appears bare and Vale would
not otherwise know: product names (Renovate, Anki, Staticaland), English
technical words missing from Vale's dictionary (lockfile, allowlist), and the
Norwegian words that `writing/skills/kontrollert-norsk/SKILL.md` uses in
prose.

### The allowlist doubles as a global mute

Vale suppresses every alert whose matched text is an accepted term, including
alerts from the `ai-tells` and `Skills` styles. Adding `synergy` to
`accept.txt` would silence the `ai-tells.OverusedVocabulary` alert on it
everywhere in the repository. A rule that polices or renames a term only works
while that term stays out of the vocabulary, so keep entries scoped to real
spelling needs.
