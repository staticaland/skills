---
name: vale-alerts
description: Give each Vale alert an editor's verdict - rewrite the sentence or suppress the one rule. Use when Vale reports an error, warning, or suggestion, or before adding a term to a Vale vocabulary.
---

# Vale alerts

An alert marks a sentence that breaks a style rule. The goal is a sentence
that serves the reader. A clean report is only a sign of that. When a change
silences an alert but makes the sentence worse, it is a regression, even though
the report goes green. This trap is Goodhart's law: once a measure becomes
the target, it stops measuring what you care about.

Work through the report like an editor. Give every alert a verdict: rewrite or
suppress.

## Verdicts

**Rewrite.** Each rule detects a smell: vagueness, hedging, filler, padding.
The flagged span is where the smell surfaced, which is seldom where the
problem lives. Reread the whole sentence and ask what it is trying to say.
Restructure over substitute: when `a number of` is flagged, name the things.
When a hedge is flagged, make the call and state it plainly. Keep the meaning
true: replace `several` with `5` when you counted five. When nobody counted,
keep only the precision you possess. A sentence that
satisfies the rule but reads worse than before means the verdict was wrong;
suppress instead.

**Suppress.** A false positive keeps its prose: quoted material, terms of art,
deliberate emphasis, honest vagueness. Mute the rule as
[Suppressing one passage](#suppressing-one-passage) shows. Suppression with a
stated reason is an editor's outcome, a deliberate judgment that the prose
wins. A rule you find yourself suppressing at every occurrence is worth
raising with a maintainer; changing the rules themselves is a separate
decision, outside the scope of fixing prose.

**Spelling and term alerts** (`Vale.Spelling`, `Vale.Terms`) usually ask a
use-mention question: is the string a word, or a literal that belongs in code
font? Read [`VOCABULARY.md`](VOCABULARY.md) before you add an entry to a vocabulary.

## Suppressing one passage

<!-- vale ai-tells.FigurativeIdioms = NO -->
<!-- "Blast radius" is the term of art for how far a suppression reaches. -->

Keep a suppression's blast radius to one rule over one passage, with Vale's
[comment markers](https://vale.sh/docs/keys/commentdelimiters). Prose about a
valley trips a `Vale` casing term that expects the product name:

```markdown
<!-- vale Vale.Terms = NO -->
<!-- The paragraph below names the valley, not the linter. -->

The vale lay under morning fog.

<!-- vale Vale.Terms = YES -->
```

Name the rule exactly as the report prints it, and turn it back on right after
the passage. A bare `<!-- vale off -->` mutes every rule, the widest blast
radius a marker has. Pair each marker with a comment that states why the rule
is off there, so the next editor can tell a deliberate exception from a
leftover.

<!-- vale ai-tells.FigurativeIdioms = YES -->

## Done

Reread each sentence you changed as an editor who never saw the report. You
are done when every alert has a verdict and every touched sentence reads at
least as well as it did before.
