---
name: adopt-small-dependencies
description:
  Find dependencies a project barely uses - one function, a small helper - and
  adopt that code into the repo, copied with a comment naming its source and
  keeping the same interface, then drop the dependency. Use when the user wants
  fewer dependencies, or wants to inline or vendor a package used for one
  function.
version: 0.1.0
---

# Adopt Small Dependencies

A dependency costs more than its install size: every update, advisory, and
compromised release reaches the project through it, along with its own
dependencies. When the repo calls one small function from it, that cost buys
little.

**Adopting** copies only the code the repo uses into the repo, where the repo
owns it from then on. It differs from a vendored package: the rest of the
package stays out, and nobody syncs the copy with upstream.

The copy keeps the upstream interface, so it works as a **drop-in**. Calling
code stays as it is, and only the import changes to point at the adopted
module.

## Procedure

### 1. Inventory what the repo uses

Take the scope from the user: the packages they named, or else every direct
runtime dependency in every manifest. Leave out dev tooling - linters,
formatters, type checkers, test runners - which the product code never calls.

For each package, search the source for its imports - every form the language
allows, including re-exports and imports by string name - and list the names
used and where.

Check for indirect use too: a framework or config file that loads the package
by name. Note any other dependency that requires the package, since the package
then stays in the tree whatever you do.

Done when every package in scope has a row naming the functions, classes, or
modules the repo uses and the files that use them.

### 2. Give each package a verdict

Mark each row **adopt** or **keep**, with a one-line reason.

Adopt when the used piece is small, stable, and easy to read and test, and the
copy can keep its interface. Keep when any of these holds:

- The used piece pulls in a large share of the library - formatting, parsing,
  or locale code that leans on the library's internal helpers.
- It needs native code or a compiled extension.
- It is security-sensitive: sanitising, escaping, crypto, auth.
- It is a parser, or anything else whose upstream fixes are worth receiving.
- It is the framework, or the repo uses it throughout.

Read the licence before an adopt verdict. Permissive licences (MIT, ISC, BSD,
Apache-2.0) allow the copy as long as their notice is kept, and Apache-2.0 also
asks you to say the code was changed. A copyleft licence (GPL, LGPL, MPL) binds
the copied file or the whole project, so it means keep unless the user decides
otherwise. No licence means no permission to copy.

Show the table to the user:

| Package   | What the repo uses               | Verdict   | Why                          |
| --------- | -------------------------------- | --------- | ---------------------------- |
| `<pkg-a>` | One maths function, in two files | **adopt** | About 20 stable lines; MIT   |
| `<pkg-b>` | Formatting helpers               | keep      | Pulls in much of the library |
| `<pkg-c>` | Sanitises HTML                   | keep      | Security-sensitive           |

Done when every row has a verdict and a reason, every adopt has a licence that
permits the copy, and the user has seen the table before step 3 changes code.

### 3. Adopt one package per commit

For each adopt verdict, in its own commit:

1. **Copy the code.** Take the functions the repo calls, plus the private
   helpers they need, from the tag or commit matching the version in the lock
   file. Keep each public name, signature, and behaviour as upstream has it, so
   the copy matches the code the tests ran against.
2. **Write the header** (below).
3. **Test it.** Add tests for the adopted code, or name the existing tests that
   cover every call site. Port upstream's tests for the copied functions when
   they exist.
4. **Change the imports** to the adopted module. The import line is the only
   change at each call site.
5. **Remove the dependency** with the package manager's own command, so the
   manifest and lock file change together. Note which transitive packages left
   the lock file.
6. **Remove the leftovers**: update-bot rules and comments or docs that name
   the package.
7. **Run** the project's tests and lint.

The header says what the code is for, then where it came from, then the notice
the licence requires:

```text
<What this code is for, in one line.>

Adopted from <package> <version>, <licence>:
<link to each source file, pinned to the tag or commit for <version>>

<copyright line from the package's licence file>

<the full licence notice, verbatim>
```

Write it as a comment in the language of the file. Link each source file at the
pinned tag or commit, never at a branch. Copy the copyright line and licence
text from the package's own `LICENSE` at that version.

Done when `git grep` finds the package name only in the header of its adopted
file, the diff at each call site touches only imports, the lock file no longer
lists the package, and tests and lint pass.

### 4. Check the lock file diff

A package manager's remove command can change more than the removed package.
It may rewrite project metadata in the lock file, such as a name taken from the
current folder when run in a worktree. Read the lock file diff and restore
anything beyond the removal.

Done when the lock file diff holds only the removed package and the transitive
packages that left with it.

Report the table from step 2, the commit for each adoption, and the transitive
packages that left the lock file.
