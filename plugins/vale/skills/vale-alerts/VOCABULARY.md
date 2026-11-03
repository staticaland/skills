# Vocabulary vs. formatting

A Vale vocabulary's `accept.txt` is a spelling allowlist. `.vale.ini` names
the vocabulary with its `Vocab` key, and the file is
`<StylesPath>/config/vocabularies/<Vocab>/accept.txt`. The file does not
decide how a term looks in prose.

Typeset a term by the use-mention distinction: does the text use a word for
its meaning, or mention the literal string itself?

| Presentation       | Name           | Use for                                                                                                |
| ------------------ | -------------- | ------------------------------------------------------------------------------------------------------ |
| `backticks`        | code font      | Literal strings the reader types or the machine reads: commands, flags, filenames, identifiers, values |
| _italics_          | words-as-words | Naming a term _as a term_, or introducing a new one before defining it                                 |
| "quotes"           | quotation      | Actual quotations. Avoid for terminology, where scare quotes read as sneering                          |
| plain, capitalized | brand name     | Products, services, and organizations such as Renovate, Homebrew, Docker                               |

A tool's prose name takes the project's official orthography (Git, Prettier,
Vale), and its command form takes backticks (`git`, `prettier`, `vale`). A
lowercase prose name (prek, uv) is part of that orthography: keep it, and
recast a sentence that would capitalize such a name at its start.

## Backticks hide text from Vale

Vale's default [`IgnoredScopes`](https://docs.vale.sh/keys/ignoredscopes)
covers the inline `code` scope, and
[`SkippedScopes`](https://docs.vale.sh/keys/skippedscopes) covers fenced code
blocks, so anything in backticks never reaches the spell-checker or any other
rule. Italics and quotes are still linted.

A spelling alert on a command, flag, or filename means it appears bare somewhere Vale still reads:
link text such as `[prek](https://prek.j178.dev/)`, or bare prose that wants
backticks. Fix the prose instead of adding an entry that enshrines the bare
usage.

A lowercase official name is the exception. When prose names the project
(prek, uv), the bare form is what the project itself writes, and the entry
belongs in the list. Write the entry in the project's exact casing: the
built-in `Vale.Terms` rule then flags every other casing, so a stray `Prek`
gets "use `prek` instead". Group such entries under a comment with a link that
confirms the casing at the source, so the lowercase form reads as deliberate
and not as a typo in the list itself. An entry meant to accept two casings
uses a character class, as `[Rr]epo` does.

Genuine allowlist material is what legitimately appears bare and Vale would
not otherwise know: product names (Renovate, Homebrew), English technical
words missing from Vale's dictionary (lockfile, allowlist), and words from
another language that the prose uses.

## Comments in `accept.txt`

Each line of an accept file is a regular expression, and the format has no
comment syntax. A line starting with `$^` can never match, so it acts as one:

```text
$^ Official lowercase names - casing confirmed at https://prek.j178.dev/
prek
```

## The allowlist doubles as a global mute

<!-- vale ai-tells.FigurativeIdioms = NO -->
<!-- "Blast radius" is the term of art for how far a suppression reaches. -->

An entry has the widest blast radius of any suppression. Vale mutes every alert
whose matched text is an accepted term, from every style, not only spelling.
A rule that polices or renames a term only works while that term stays out of
the vocabulary, so keep entries scoped to real spelling needs, and suppress one
passage with comment markers instead.

<!-- vale ai-tells.FigurativeIdioms = YES -->
