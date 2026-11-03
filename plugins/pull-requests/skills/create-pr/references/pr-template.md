<!--
Always write the pull request title and description in ASD-STE100 Simplified Technical English.

Write each paragraph on one line. GitHub reflows the markdown when it renders, so a hard wrap at 80 columns buys nothing and makes the description awkward to edit.

Use short sentences.
Use a controlled and consistent vocabulary.
Make direct statements.
Remove hedging and information that reviewers do not need.
Say each fact one time. Each section gives information that the other sections do not give. Do not repeat the title, and do not name the kind of change when the title prefix, such as `feat:` or `chore:`, already names it.

Follow Zinsser's four principles of quality writing:
1. Simplicity
2. Brevity
3. Clarity
4. Humanity

Avoid these patterns:
- Staccato pairs
- Antithesis reframes and negative parallelism
- Isocolon metaphor-pairs
- Backward references
-->

## What is this change?

<!-- State what changed. Keep the reason for the next section. -->

[Add a brief description of what the change does.]

## Why do we need this change?

<!-- State the problem and why it matters. Do not describe the change again. -->

[Add a description of the problem the change solves.]

## Who is this change for?

[Add information about the users that the change is for.]

## What is the merge danger?

<!--
Door: say if the change is a one-way door or a two-way door. A revert undoes a two-way door. A one-way door stays after a revert: deleted data, a published release, a changed public API or URL, a migration, or a message sent to an external service. Name what makes the door one-way.

What can break: name what fails if the change is wrong, and who notices. Think about consumers of the code, installed users, CI, and other systems that read the output.
-->

**Door:** [One-way or two-way. Add one sentence if the answer is not obvious.]

**What can break:** [Name the scope in one word, such as none, local, repo, or consumers. Then name what fails.]

## Which issue(s) does this PR fix?

<!-- Link the issues this PR closes, or state that there are none. -->
