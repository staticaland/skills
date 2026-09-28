---
type: regex
pattern: '- name: Start the test server\n(?:[ \t]+(?!- )\S[^\n]*\n)*?[ \t]+id: \S'
---

The test server step has an `id`, so a later step can cancel it.
