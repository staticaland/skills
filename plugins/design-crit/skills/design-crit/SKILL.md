---
name: design-crit
description: >
  Run a design crit on a rendered UI and fix what it finds: broken alignment,
  inconsistent spacing, flat or competing hierarchy, and overlapping or
  clipped elements, each named in designer terms. Use when the user says a
  page, screen, or component looks off, cramped, messy, or unpolished, asks
  for a design or visual review, or wants layout and spacing cleaned up.
---

# Design crit

Look at the UI the way a senior visual designer does in a crit: name every
defect with the term a designer would use, point at where it is, measure it,
and fix it at the source. A note like "this looks off" is not a finding; "the
card titles sit 3px off the grid's left edge, a ragged left edge" is.

## Steps

### 1. Render it

Look at pixels, not only code. Render the UI at the viewport it ships at, and
at one narrow width (375px) when it is responsive. Drive the browser with the
agent-browser skill from the `browser` plugin when it is available, else with
Playwright. Take a full-page screenshot and keep the page open to measure
boxes with `getBoundingClientRect()` and `getComputedStyle()`. When the user gave only a
screenshot, crit the screenshot and estimate measurements from it. Done when
you have a screenshot of every state you will judge - default, hover, empty,
long content, error - that the change touches.

### 2. Crit it

Walk every lens in [the crit lenses](#crit-lenses) over every screenshot. For
each defect, write one finding:

- **Term** - the designer's name for it, from the lens.
- **Where** - the element, by visible label or selector.
- **Evidence** - the measurement: the 3px offset, the 14px gap beside the 16px
  ones, the two 600-weight labels competing for the focal point.
- **Fix** - the change, in the project's own tokens where it has them
  (`space-4`, `text-lg`), else on its spacing scale.

Done when every lens is applied to every screenshot, and each finding has all
four parts. A lens with no defect says so in one line.

### 3. Fix it

Fix each finding at its source: the shared component, the token, or the
layout container, not a one-off margin on the symptom. Reach for layout
primitives before nudges - `gap` over sibling margins, a grid over absolute
offsets, `align-items` over `top: 2px`. Keep values on the project's spacing
and type scales; add a value to a scale only when the crit shows the scale
has a real hole. When there is no code to change, the deliverable is the
finding list, ranked by how much each defect hurts the read.

### 4. Re-render and re-crit

Render the same states again and walk the lenses over the new screenshots.
A fix that moves a defect somewhere else - a tightened row that now collides
at 375px - is a new finding. Done when every finding is resolved or listed
as open with the reason, and the report shows each finding's term, the fix,
and before and after screenshots.

## Crit lenses

### Alignment

- **Grid** - elements snap to the layout grid's columns and gutters. An
  element off the grid by a few pixels reads as a mistake, not a choice.
- **Edges** - text and boxes that start at the same x share one left edge.
  Mixed padding produces a **ragged edge**.
- **Optical alignment** - align what the eye sees: icons and text centered on
  the x-height or cap height, not the line box; round and pointed shapes
  overshoot slightly; punctuation and quotes hang outside the text edge.
- **Baseline** - adjacent text of different sizes shares a baseline. Labels
  and values in a row align on baseline, not on box top.
- **Tangents** - two edges that almost touch or almost align create tension.
  Align them or separate them clearly.

### Spacing

- **Spacing scale** - every gap is a step on one scale, such as a 4pt or 8pt
  grid. An off-scale value (13px, 18px) is a finding.
- **Proximity** - related items sit closer to each other than to unrelated
  ones. Space inside a group is smaller than space between groups; equal
  spacing everywhere erases grouping.
- **Vertical rhythm** - consistent spacing between sections and a leading
  that fits the type size.
- **Padding** - containers pad evenly, with the same inset on sides that
  look equal; a button or card whose padding differs between siblings is a
  finding.
- **Density** - whitespace is deliberate. **Crowding** is too little
  breathing room; **dead space** is a large gap that groups nothing.

### Hierarchy

- **Focal point** - each view has one entry point the eye lands on first. Two
  elements of equal weight fighting for it are **competing**.
- **Visual weight** - size, weight, color, and contrast rank elements in the
  order the user reads them. A secondary action as loud as the primary one is
  a finding.
- **Type scale** - sizes come from one modular scale with clear steps between
  levels. Sizes too close together (15px and 16px) read as an error, not a
  level.
- **Squint test** - blur the screenshot. What stays visible is the hierarchy;
  when nothing stands out, or the wrong thing does, it is **flat**.
- **Grouping** - common region (a shared container), similarity, and
  proximity tell the eye what belongs together.
- **Measure** - body text runs 45-75 characters per line.

### Collisions

- **Overlap** - two elements share pixels they were not designed to share:
  text under an icon, a badge over a label, a sticky header over content.
- **Clipping and overflow** - text cut off, truncated without an ellipsis, or
  spilling out of its container at long content or narrow widths.
- **Stacking** - a dropdown, tooltip, or modal behind something it should sit
  above: a z-index or stacking-context defect.
- **Wrapping** - **widows** and **orphans** in headings, buttons that wrap to
  two lines, and labels that push their neighbors out of alignment.
- **Hit targets** - interactive targets under 44px or touching each other.

### Consistency

- **Repetition** - the same element looks the same everywhere: one radius, one
  border weight, one shadow per elevation level, one icon size per context.
- **Contrast** - text meets WCAG AA (4.5:1 body, 3:1 large text), and
  differences that carry meaning are strong enough to read as intended.
