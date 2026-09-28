---
type: regex
pattern: '^[ \t]*(- )?(background|parallel|wait|wait-all|cancel):'
flags: m
match: not_contains
---

The workflow has no `background`, `parallel`, `wait`, `wait-all`, or `cancel`
key. Each step needs the result of the step before it, so no step can run
concurrently.
