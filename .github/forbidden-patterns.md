# Forbidden writing patterns

This file is the source of truth for writing patterns that this repository
rejects. Add a pattern when review finds a repeatable problem. For each pattern,
give its form and the required replacement.

## Staccato pairs

### Pattern

Short adjacent sentences use the same structure for dramatic effect.

### Avoid

`Tests fail. Logs vanish.`

### Use

Join related facts in one complete sentence, or vary the sentence structure.

## Antithesis reframe and negative parallelism

### Pattern

A sentence defines a subject with a form such as `not X, but Y`. The pattern
also includes matched negative and positive statements.

### Avoid

`This is not a parser. It is a validator.`

### Use

State the exact role directly: `This component validates configuration files.`

## Isocolon metaphor-pairs

### Pattern

Balanced clauses use matching grammar and metaphors as a slogan.

### Avoid

`The API is the map; the CLI is the compass.`

### Use

State the literal relationship: `The CLI exposes API operations.`

## Backward references

### Pattern

A pronoun or position word makes the reader search earlier text for its meaning.
Common forms include `this`, `that`, `it`, `the former`, `the latter`, `above`,
and `below`.

### Avoid

`Update the marketplace entry. Then validate it.`

### Use

Repeat the specific noun: `After you update the entry, validate the marketplace.`
