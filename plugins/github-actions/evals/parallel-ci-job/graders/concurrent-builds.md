---
type: regex
pattern: '(^[ \t]*- parallel:|- name: Build the (app|docs)\n(?:[ \t]+(?!- )\S[^\n]*\n)*?[ \t]+background: true)'
flags: m
---

The app build and the docs build run concurrently: in one `parallel:` block,
or with `background: true` on one of them.
