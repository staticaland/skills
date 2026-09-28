---
type: regex
pattern: '(^[ \t]*- parallel:|- name: (Scan the dependencies|Run the tests)\n(?:[ \t]+(?!- )\S[^\n]*\n)*?[ \t]+background: true)'
flags: m
---

The scan and the tests run concurrently: in one `parallel:` block, or with
`background: true` on one of them.
