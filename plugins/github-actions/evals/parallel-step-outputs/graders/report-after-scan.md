---
type: regex
pattern: '(?:^      - name: Scan the dependencies\n(?:        (?!background: true)[^\n]*\n)*(?=      - |```)(?:[^\n]*\n)*?^[ \t]*- name: Report the scan findings\n|^      - parallel:\n(?:[ \t]{8,}(?![ \t])[^\n]*\n|\n)*?[ \t]{8,}- name: Scan the dependencies\n(?:[^\n]*\n)*?^(?=      - )(?:[^\n]*\n)*?^[ \t]*- name: Report the scan findings\n|^[ \t]*- name: Scan the dependencies\n(?:[ \t]+(?![ \t]|- )[^\n]*\n)*?[ \t]+id: ([\w-]+)\n(?:[^\n]*\n)*?^[ \t]*(?:- )?(?:wait: [^\n]*\b\1\b|wait-all:)(?:[^\n]*\n)*?^[ \t]*- name: Report the scan findings\n)'
flags: m
---

The report step reads `steps.scan.outputs.findings`. It starts only after the
scan is complete. The pattern accepts three shapes, with steps at the six-space indent of the original file:

- The scan is a step before it.
- The scan is in a `parallel:` block that ends before it.
- The scan is a background step with an `id`, and a `wait` that names the
  `id` or a `wait-all` comes before it.
