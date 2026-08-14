---
name: standalone
description: Strip references the reader cannot see from prose and code comments.
disable-model-invocation: true
---

# Standalone

Make an artifact stand alone. Agent output points back at the session that
produced it — "as discussed", "the old handler", "we decided" — and the reader
has none of it.

## The test

Can a reader holding only this artifact resolve the reference? If it points at
context that isn't in the artifact, it goes.

References that fail the test:

- Conversational deixis — "as discussed", "per your suggestion".
- Process narration — "I refactored this to…".
- Diff talk in a non-diff artifact — "changed X to Y", "this used to be".
- Ghost alternatives — "instead of the approach that didn't work".
- Unanchored temporal words — "now", "currently", "the new format" — stale on
  arrival.

## Scope

Prose files and code comments. Not commit messages or PR descriptions: a commit
_is_ a change, so "changed X to Y" is correct there. When an artifact's job is
to record change — changelogs, ADRs, migration guides, deprecation notices —
past reference is the content; leave it.

## Fixing a failed reference

Match each failed reference to one of three shapes:

- **Decoration** — the sentence survives without the reference. "As we
  discussed, use the retry wrapper." → "Use the retry wrapper." Delete the
  clause.
- **Load-bearing** — the fact is stated only by reference. "This replaces the
  old handler." Rewrite the sentence to state what the thing does.
- **Unrecoverable** — the missing context isn't in the artifact at all. Surface
  it: quote the reference and name what's missing. Don't delete silently, don't
  invent the context.

## Output

Inline text comes back bare — the revised text with no wrapper or explanation.
File input is edited in place with the Edit tool. Unrecoverable references are
reported after, whichever the input.

Done when every reference in the artifact resolves from the artifact alone or
is surfaced as unrecoverable.
