---
type: regex
pattern: '- name: Send usage telemetry\n(?:[ \t]+(?!- )\S[^\n]*\n)*?[ \t]+background: true'
---

The telemetry step has `background: true`. No step reads its result, so it
needs no `wait`.
