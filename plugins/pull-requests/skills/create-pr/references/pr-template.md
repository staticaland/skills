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

## What

<!-- State what changed. Keep the reason for the next section. -->

[Tell what the change does in one sentence.]

[Add a second sentence as its own paragraph only if the first is not enough.]

<details>
<summary>Details</summary>
<br>

[Show the change as a diagram, a diff sketch, or a tree. Then add the parts of the change and how they work.]

</details>

## Why

<!-- State the problem and why it matters. Do not describe the change again. -->

[Name the problem the change solves in one sentence.]

[Add a second sentence as its own paragraph only if the first is not enough.]

<details>
<summary>Details</summary>
<br>

[Add the background, the decisions, and their tradeoffs.]

</details>

## Merge danger

<!--
Reversible: say if a revert undoes the change. These things stay after a revert: deleted data, a published release, a changed public API or URL, a migration, or a message sent to an external service. If the answer is no, name what stays.

What can break: think about consumers of the code, installed users, CI, and other systems that read the output.
-->

**Reversible:** [Say in one sentence if a revert undoes the change, and what stays if it does not.]

**What can break:** [Say in one sentence what fails if the change is wrong, and who notices. Write "Nothing" if nothing can fail.]

<details>
<summary>Details</summary>
<br>

[Add the reasons for the two answers, and how to revert or recover.]

</details>

## Issues

<!-- Link the issues this PR closes, or state that there are none. -->
