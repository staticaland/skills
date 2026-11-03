---
name: vale-alerts
description: Give each Vale alert an editor's verdict - rewrite the sentence or suppress the one rule. Use when Vale reports an error, warning, or suggestion, or before adding a term to a Vale vocabulary.
---

# Vale alerts

An alert is advice from a style guide. The goal is prose that serves the
reader; a change that silences an alert while weakening the sentence is a
regression, even though the report goes green. Work through a report like an
editor: give every alert a verdict, rewrite or suppress.

## Verdicts

**Rewrite.** Each rule detects a smell: vagueness, hedging, filler, padding.
The flagged span is where the smell surfaced, which is seldom where the
problem lives. Reread the whole sentence and ask what it is trying to say.
Restructure over substitute: when `a number of` is flagged, name the things.
When a hedge is flagged, make the call and state it plainly. Keep the meaning
true: replace `several` with `5` when you counted five. When nobody counted,
keep only the precision you possess. Then reread the result. A sentence that
satisfies the rule but reads worse than before means the verdict was wrong;
suppress instead.

**Suppress.** Quoted material, terms of art, deliberate emphasis, honest
vagueness: keep the prose and mute the one rule around the one passage, as
[Suppressing one passage](#suppressing-one-passage) shows. Suppression with a
stated reason is an editor's outcome, a deliberate judgment that the prose
wins. A rule you find yourself suppressing at every occurrence is worth
raising with a maintainer; changing the rules themselves is a separate
decision, outside the scope of fixing prose.

**Spelling and term alerts** (`Vale.Spelling`, `Vale.Terms`) usually ask a
different question: is the string a word, or code that wants backticks? Read
[`VOCABULARY.md`](VOCABULARY.md) before you add an entry to a vocabulary.

## Suppressing one passage

Turn the one rule off around the one passage with Vale's
[comment markers](https://vale.sh/docs/keys/commentdelimiters). Prose about a
valley trips a `Vale` casing term that expects the product name:

```markdown
<!-- vale Vale.Terms = NO -->
<!-- The paragraph below names the valley, not the linter. -->

The vale lay under morning fog.

<!-- vale Vale.Terms = YES -->
```

Name the rule exactly as the report prints it, and turn it back on right after
the passage. A bare `<!-- vale off -->` mutes every rule and is almost always
too broad. Pair each marker with a comment that states why the rule is off
there, so the next editor can tell a deliberate exception from a leftover.

Widening the vocabulary is not a suppression: an accepted term mutes every
rule on that string across the whole project, as `VOCABULARY.md` explains.

## Done

Reread each sentence you changed as an editor who never saw the report. You
are done when every alert has a verdict and every touched sentence reads at
least as well as it did before.
