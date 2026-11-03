---
type: regex
pattern: '(?:^      - name: Build the app into dist\n(?:        (?!background: true)[^\n]*\n)*(?=      - |```)(?:[^\n]*\n)*?^[ \t]*- name: Upload dist\n|^      - parallel:\n(?:[ \t]{8,}(?![ \t])[^\n]*\n|\n)*?[ \t]{8,}- name: Build the app into dist\n(?:[^\n]*\n)*?^(?=      - )(?:[^\n]*\n)*?^[ \t]*- name: Upload dist\n|^[ \t]*- name: Build the app into dist\n(?:[ \t]+(?![ \t]|- )[^\n]*\n)*?[ \t]+id: ([\w-]+)\n(?:[^\n]*\n)*?^[ \t]*(?:- )?(?:wait: [^\n]*\b\1\b|wait-all:)(?:[^\n]*\n)*?^[ \t]*- name: Upload dist\n)'
flags: m
---

The upload of `dist` starts only after the build is complete. The pattern accepts three
shapes, with steps at the six-space indent of the original file:

- The build is a step before it.
- The build is in a `parallel:` block that ends before it.
- The build is a background step with an `id`, and a `wait` that names the
  `id` or a `wait-all` comes before it.
