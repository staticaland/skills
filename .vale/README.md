# Vale styles and vocabulary

This directory backs [`.vale.ini`](../.vale.ini). The `Skills` style and the
`Skills` vocabulary live here as source; the `ai-tells` and `ai-tells-commits`
styles are synced from the packages `.vale.ini` names and are committed so CI
runs without a download.

## Reading a report

An alert is advice from a style guide. The goal is prose that serves the
reader; a change that silences an alert while weakening the sentence is a
regression, even though the report goes green. Work through a report like an
editor: give every alert a verdict, rewrite or suppress.

**Rewrite.** Each rule detects a smell: vagueness, hedging, filler, padding.
The flagged span is where the smell surfaced, which is seldom where the
problem lives. Reread the whole sentence and ask what it is trying to say.
Restructure over substitute: when `a number of` is flagged, name the things;
when a hedge is flagged, make the call and state it plainly. Keep the
meaning true: replace `several` with `5` when you counted five, and when
nobody counted, keep only the precision you possess. Then reread the result.
A sentence that satisfies the rule but reads worse than before means the
verdict was wrong; suppress instead.

**Suppress.** Quoted material, terms of art, deliberate emphasis, honest
vagueness: keep the prose and mute the one rule around the one passage, as
[When a rule flags text that needs no fix](#when-a-rule-flags-text-that-needs-no-fix)
shows. Suppression with a stated reason is an editor's outcome, a deliberate
judgment that the prose wins. A rule you find yourself suppressing at every
occurrence is worth raising with a maintainer; changing the rules themselves
is a separate decision, outside the scope of fixing prose.

The editor test, before you commit: reread each sentence you changed as an
editor who never saw the report. You are done when every alert has a verdict
and every touched sentence reads at least as well as it did before.

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

A tool can carry two names. The prose name takes the project's official
orthography (Git, Prettier, Vale), and the command form takes backticks
(`git`, `prettier`, `vale`). A project can also declare a lowercase prose name
(prek, uv). That casing is part of the name: follow the project's styling, and
recast a sentence that would capitalize such a name at its start.

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

A lowercase official name is the exception. When prose names the project
(prek, uv), the bare form is what the project itself writes, and the entry
belongs in the list. Write the entry in the project's exact casing: the
built-in `Vale.Terms` rule then flags every other casing, so a stray `Prek`
gets "use `prek` instead". Place such an entry under the "Official lowercase
names" comment in `accept.txt`, with a link above it that confirms the casing
at the source, so the lowercase form reads as deliberate and not as a typo in
the list itself. An entry meant to accept two casings uses a character class,
as `[Rr]epo` does.

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

## When a rule flags text that needs no fix

A rule can flag text that needs no fix. Prose about a valley would trip the
`Vale` casing term, which expects the product name. Do not widen `accept.txt`
for such a case, since the section above shows an entry mutes the term
everywhere. Turn the one rule off around the one passage instead, with Vale's
[comment markers](https://vale.sh/docs/keys/commentdelimiters):

```markdown
<!-- vale Vale.Terms = NO -->
<!-- The paragraph below names the valley, not the linter. -->

The vale lay under morning fog.

<!-- vale Vale.Terms = YES -->
```

Scope the marker to the single rule and turn it back on right after the
passage. A bare `<!-- vale off -->` mutes every rule and is almost always too
broad. Pair each marker with a comment that states why the rule is off there,
so the next editor can tell a deliberate exception from a leftover.
