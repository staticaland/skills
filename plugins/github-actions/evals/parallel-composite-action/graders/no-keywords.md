---
type: regex
pattern: 'using: "?composite"?\n(?:(?!```)[^\n]*\n)*?[ \t]*(- )?(background|parallel|wait|wait-all|cancel):'
match: not_contains
---

The code block with the composite action has no `background`, `parallel`,
`wait`, `wait-all`, or `cancel` key. A composite action cannot use these
keywords. A workflow job that the response suggests as an alternative can use
them.
