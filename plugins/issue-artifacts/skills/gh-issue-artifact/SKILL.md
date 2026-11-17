---
name: gh-issue-artifact
description: >-
  Manage issue artifacts - the Markdown documents, HTML documents, and links
  attached to a GitHub issue - with `gh issue artifact`. Use when saving a
  plan, research notes, a log, a prototype page, or a reference link onto an
  issue; when reading, editing, or restoring an earlier version of one; or when
  downloading or deleting them. Not GitHub Actions artifacts.
---

# gh-issue-artifact

An issue artifact is a named document or link that lives on a GitHub issue,
beside the body and comments. Each artifact has a number scoped to its issue,
a type, a URL such as `.../issues/142/artifacts/3`, and an edit history of
numbered versions. Use one for material that belongs to the issue but would
bury the conversation as a comment: an implementation plan, research notes, a
log, a clickable prototype.

GitHub Actions build outputs are a different thing, downloaded with
`gh run download`.

## Before the first command

The command group is in preview and changes without notice. Confirm the
installed `gh` has it, and read the flags it actually offers:

```bash
gh issue artifact --help
```

`unknown command "artifact"` means this build predates it - upgrade `gh` and
tell the user that is the blocker.

Artifacts are refused in these cases, before anything is written:

- **Host**: GitHub Enterprise Server. github.com and `ghe.com` tenants work.
- **Target**: a pull request. Artifacts exist only on issues.

## Types

| Type            | Made from                                           | `--attach` |
| --------------- | --------------------------------------------------- | ---------- |
| `generic`       | any text file, `--body`, or `--body-file`           | yes        |
| `plan`          | `--type plan`; behaves like `generic` for now       | yes        |
| `embedded_html` | a `.html` or `.htm` file, or `--type embedded_html` | no         |
| `link`          | an `http(s)` URL argument or a `.url` shortcut file | no         |

The type is fixed at creation. `edit` never changes it, so turning a link into
a document means creating a new artifact and deleting the old one.

## Addressing an artifact

`view`, `edit`, `delete`, and `download` take either the issue and the
artifact number, or the artifact's URL:

```bash
gh issue artifact view 142 2
gh issue artifact view https://github.com/monalisa/monas-cafe/issues/142/artifacts/2
```

The issue is a number or an issue URL; add `--repo OWNER/REPO` when the
current directory isn't the target repository. Several URLs in one `delete` or
`download` must all be on the same issue.

## Create

One artifact per file or URL argument:

```bash
gh issue artifact create 142 signin-plan.md
gh issue artifact create 142 'docs/signin-plan.md#Sign-in plan' oauth-research.md
gh issue artifact create 142 menu-prototype.html
gh issue artifact create 142 https://github.com/monalisa/monas-cafe/wiki/OAuth-runbook --name 'Staging OAuth runbook'
```

Naming:

- A file is named after its filename; `path#Name` (quoted, so the shell keeps
  the `#`) or `--name` sets another. Use one of the two, not both.
- A URL is named after its host, which is rarely useful - pass `--name`.
- Characters the API refuses, such as parentheses, are stripped:
  `plan (1).md` becomes `plan 1.md`.

Content written in the session goes through `--body` or `--body-file`, which
create exactly one artifact and require `--name` when the content has no
filename to borrow:

```bash
gh issue artifact create 142 --name 'Sign-in plan' --body "$plan"
cat order-sync.log | gh issue artifact create 142 --body-file - --name 'Order sync log'
gh issue artifact create 142 --body-file notes/plan.md --type plan
```

Content must be non-blank text; a binary file is refused. `--type` sets every
document's type regardless of extension and is refused when any argument is a
link.

## List and view

```bash
gh issue artifact list 142 --json number,name,type,url
gh issue artifact list 142 --type link
gh issue artifact view 142 2 --json body --jq .body
gh issue artifact view 142 2 --json versions
gh issue artifact view 142 2 --version 5
```

`list` returns every artifact unless `--limit` caps it. Prefer `--json` for
anything you parse; run `--json` with no field list to print the available
fields. `view` adds a `versions` field holding the edit history. `--version`
and `--json` can't be combined - fetch an old version's text with
`download --version N --output -` instead.

## Edit and restore

```bash
gh issue artifact edit 142 2 --name 'OAuth callback plan v2'
gh issue artifact edit 142 2 --body-file 2-OAuth-callback-plan.md
gh issue artifact edit 142 3 --body https://github.com/monalisa/monas-cafe/wiki/OAuth-runbook-v2
gh issue artifact edit 142 2 --restore-version 5
```

Each edit saves a new version; nothing is lost. `--body` or `--body-file`
replaces the whole content, so to change part of a document, download it,
edit the file, and send it back:

```bash
gh issue artifact download 142 2 --output plan.md
# edit plan.md
gh issue artifact edit 142 2 --body-file plan.md
```

A link's new content must be an `http(s)` URL or a `.url` file.
`--restore-version N` saves version N's name and content as the newest version.

## Download

```bash
gh issue artifact download 142
gh issue artifact download 142 2 5 --dir notes
gh issue artifact download 142 2 --output -
gh issue artifact download 142 2 --version 5 --output -
```

With no artifact numbers, every artifact on the issue downloads. Files are
named `<number>-<name>`: `.md` for documents, `.html` for HTML documents, and
`.url` Internet Shortcut files for links. An existing file fails that artifact
unless you pass `--clobber` or `--skip-existing`. `--output` and `--version`
take a single artifact; `--output -` prints the content.

## Delete

A deleted artifact can't be restored. Confirm with the user before deleting, then pass `--yes` - without a terminal,
the command refuses to run without it:

```bash
gh issue artifact delete 142 2 5 --yes
```

## Images in a document

`create` and `edit` take `--attach` for `generic` and `plan` documents. A
relative image path in a document file resolves against that file's directory
first, so `![flow](./signin-flow.png)` in `docs/signin-plan.md` finds
`docs/signin-flow.png`:

```bash
gh issue artifact create 142 docs/signin-plan.md --attach docs/signin-flow.png
gh issue artifact edit 142 2 --attach ./after.png
```

`edit` with only `--attach` appends the images to the current content. With
several documents in one `create`, a file no document references is an error
before anything uploads. For alt text, video, and upload permissions, the
`gh-attach` skill in the `pull-requests` plugin covers the flag in full.

## Reading the result

`create`, `edit`, and `download` print one line per artifact. Piped, each line
starts with a status: `created`, `updated`, `written`, `skipped`, or `failed`.
A piped `delete` prints only its failures. A run with several artifacts keeps
going past a failure and exits 1 at the end, so read every line before
retrying - rerunning the whole `create` duplicates the artifacts that
succeeded.

A `created` or `updated` line that carries an error reason means some
`--attach` files uploaded and others didn't: the artifact was saved pointing at
the uploads that worked. Re-attach only the missing files with `edit`.
