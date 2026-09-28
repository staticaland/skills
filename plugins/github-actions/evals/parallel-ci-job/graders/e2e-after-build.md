---
type: regex
pattern: '(?:^      - name: Build the app\n(?:        (?!background: true)[^\n]*\n)*(?=      - |```)(?:[^\n]*\n)*?^[ \t]*- name: Run the E2E tests\n|^      - parallel:\n(?:[ \t]{8,}(?![ \t])[^\n]*\n|\n)*?[ \t]{8,}- name: Build the app\n(?:[^\n]*\n)*?^(?=      - )(?:[^\n]*\n)*?^[ \t]*- name: Run the E2E tests\n|^[ \t]*- name: Build the app\n(?:[ \t]+(?![ \t]|- )[^\n]*\n)*?[ \t]+id: ([\w-]+)\n(?:[^\n]*\n)*?^[ \t]*(?:- )?(?:wait: [^\n]*\b\1\b|wait-all:)(?:[^\n]*\n)*?^[ \t]*- name: Run the E2E tests\n)'
flags: m
---

The E2E tests start only after the app build is complete. The pattern accepts three
shapes, with steps at the six-space indent of the original file:

- The app build is a step before them.
- The app build is in a `parallel:` block that ends before them.
- The app build is a background step with an `id`, and a `wait` that names the
  `id` or a `wait-all` comes before them.
