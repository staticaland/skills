---
name: polish-ui
description: Review a UI for visual polish and fix what you find, covering alignment, spacing, grouping, typography, visual weight, emphasis, and colour. Use when asked to polish, tidy, or review the look of a page, component, or screenshot.
---

# Polish UI

Review this UI for visual polish and fix what you find. Look at the rendered result, not only the code: take a screenshot before and after.

Check:

- **Alignment:** elements sharing an edge or axis line up. Nothing is off-grid or ragged.
- **Alignment axes:** as few distinct left edges as possible. Anchor each element to a shared edge so that nothing floats on its own axis.
- **Overflow:** text stays inside its container. Long content wraps, scrolls, or truncates cleanly.
- **Spacing:** padding and gaps use a consistent spacing scale (such as 4/8/12/16/24/32). Related items sit closer than unrelated ones.
- **Grouping:** related items are grouped by proximity first, then by common region (subtle background, border, or card) where needed. Avoid nesting boxes inside boxes.
- **Row alignment:** everything in a row sits on one shared line from end to end, however far apart the items are. Text of different sizes shares a baseline. Icons and logos are optically centred on that text, not only mathematically.
- **Typographic hierarchy:** headings, body, and labels follow a clear type scale with a limited set of sizes and weights.
- **Visual weight:** the heaviest elements (fills, borders, size) are the most important ones. Nothing outweighs what it belongs to.
- **Emphasis:** bold, colour, and size are used sparingly and consistently. If everything is emphasised, nothing is.
- **Colour:** a limited palette from shared tokens. Each colour means the same thing everywhere (such as one accent for actions). Contrast meets WCAG AA.
- **Squint test:** blurred, the most important element and the main groupings should still be obvious.

For each issue, say what it is and where, then fix it. Prefer shared tokens over one-off values.
