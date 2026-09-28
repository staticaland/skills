---
type: regex
pattern: '(&\s*$|&\s*\)|\bnohup\b|\bdisown\b)'
flags: m
match: not_contains
---

No command runs in the background with a shell trick such as `&` at the end of
a line or `nohup`. The step keywords do this job.
