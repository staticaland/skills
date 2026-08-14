# other

Turn text, notes, code, or images into Anki flashcards built on Andy Matuschak's
prompt-writing principles, and ask for a message again in plain language when it
does not land.

Category: `other`

## Skills

Model-invoked - Claude activates these automatically when the request matches.

- **[anki-flashcards](./skills/anki-flashcards/SKILL.md)** - Creates focused
  Anki flashcards from text, documents, or images for spaced repetition
  learning.

User-invoked - run these by name.

- **[bro](./skills/bro/SKILL.md)** - Restates the last message in plain human
  language, with no jargon.
- **[wait-what](./skills/wait-what/SKILL.md)** - Asks for a re-pitch of the last
  message, in Simplified Technical English and the project's own domain terms.

### Install individual skills

```bash
npx skills add staticaland/skills --skill anki-flashcards
npx skills add staticaland/skills --skill bro
npx skills add staticaland/skills --skill wait-what
```
