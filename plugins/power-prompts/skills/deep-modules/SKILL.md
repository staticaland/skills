---
name: deep-modules
description: Make each module deep, with a small interface over substantial behavior.
disable-model-invocation: true
---

<!-- vale Skills.WeaselWords = NO -->
<!-- vale ai-tells.VerbTricolon = NO -->
<!-- The prompt is quoted verbatim. -->

Make each module deep: a simple interface hiding a lot of behavior. If deleting
a module would only push its complexity back onto its callers, it's earning its
place; if nothing would be lost, merge it away. Put each concept in the one
module that owns it, and pull special cases, ordering rules, validation and
derived values inside, so callers never have to know them. Shrink the interface
until there's one obvious way to call it: drop any parameter, flag or option the
module can work out itself, that every caller passes the same way, or that
nobody reads, then move every caller to the new shape and delete the old path
completely.

<!-- vale ai-tells.VerbTricolon = YES -->
<!-- vale Skills.WeaselWords = YES -->

Apply it to the task the user names with this command, or else to the task at
hand in this conversation.
