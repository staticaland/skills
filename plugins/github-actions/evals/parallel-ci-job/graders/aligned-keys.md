---
type: regex
pattern: '^( *)- [a-z-]+:[^\n]*\n(?!\1  [a-z]|\1 *- |\s*```)[ \t]*[a-z-]+:'
flags: m
match: not_contains
---

In each list item, the second key lines up with the first key. The
`parallel-steps` skill once had examples indented one column off, and a copy of
them would break the YAML.
