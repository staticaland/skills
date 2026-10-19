---
type: regex
pattern: '- name: Start the test server\n(?:[ \t]+(?!- )\S[^\n]*\n)*?[ \t]+background: true'
---

The test server step keeps `background: true`. The key is valid, and
`actionlint` reports it only because the tool does not support it yet.
