---
name: Auto-cite Factual Claims
description:
  Add Markdown footnote citations to factual claims in supplied text. Use when
  the user asks to cite claims, add sources or references, fact-check and
  footnote a document, or support statements with web sources.
version: 0.1.0
---

# Auto-cite Factual Claims

Support every factual claim in supplied text with a source found through web
search, then cite it with a Markdown footnote. Preserve the text's wording and
structure apart from the citations.

## Process

### 1. Inventory the claims

Read the complete text. Treat each independently verifiable assertion as a
claim, including dates, quantities, definitions, attributed statements,
comparisons, and causal statements. Split compound sentences into atomic claims
when one source might not support the whole sentence.

Classify every sentence as nonfactual or as one or more factual claims. Opinions
clearly presented as opinions, instructions, and the author's own stated
intentions do not need citations.

Done when every sentence is classified and every factual claim is in the
inventory.

### 2. Research every claim

Search the web for each claim and open the candidate source. Prefer sources in
this order:

1. Primary sources, such as official records, research papers, standards, and
   first-party documentation
2. Authoritative institutions and subject-matter publications
3. Reputable secondary reporting

Match the source to the claim's exact scope, date, geography, quantity, and
degree of certainty. The opened page must state or directly establish the
claim. A search-result snippet is not evidence. For a time-sensitive claim, use
the most recent source that covers the stated period. Record the page title and
canonical URL without tracking parameters.

Done when every claim has a source that supports it or is recorded as
unsupported after targeted follow-up searches.

### 3. Place markers

Put a marker immediately after the clause or sentence it supports:

```markdown
The factual claim appears here.[^1]
```

<!-- vale ai-tells.UniversalObject = NO -->
<!-- "every claim" is the condition the rule sets, not a claim about coverage. -->

Use one marker for two or more claims only when its source supports every claim.

<!-- vale ai-tells.UniversalObject = YES -->

Reuse a marker when the same source supports separate claims. Place multiple
markers together when a claim needs two or more sources.

Preserve existing footnotes. Verify any existing citation used to satisfy the
inventory by opening its source. For new numeric labels, start after the highest
existing number, or at `1` when the document has none.

Done when every supported claim has a marker whose source supports that exact
claim.

### 4. Append definitions

Append each new definition at the bottom of the document, after any existing
footnote definitions. Use the source's page title as linked text:

```markdown
[^1]: [Article Title](https://example.com/article)
```

Keep one blank line between definitions. Escape Markdown punctuation in titles
when needed.

For file input, edit the file in place. For inline input, return the complete
cited text. If any claim remains unsupported, name it in a brief warning before
the inline text or in the response after editing a file. Leave that claim
unmarked and reserve markers for sources that support the exact claim.

### 5. Audit

Check every claim against its opened source. Then check that:

- Every supported factual claim has a marker.
- Every marker has one definition, and every definition is referenced.
- Every definition contains a linked source title and a working source URL.
- Marker placement makes the supported claim unambiguous.
- Footnote labels do not collide.
- The appended definitions are the final document content.

Done when all six checks pass and every unsupported claim is reported.
