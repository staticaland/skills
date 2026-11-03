# Vale styles and vocabulary

This directory backs [`.vale.ini`](../.vale.ini). The `Skills` style and the
`Skills` vocabulary live here as source; the `ai-tells` and `ai-tells-commits`
styles are synced from the packages `.vale.ini` names and are committed so CI
runs without a download.

## Acting on alerts

The [`vale-alerts`](../plugins/vale/skills/vale-alerts/SKILL.md) skill covers
how to act on a report: every alert gets a verdict (rewrite or suppress), and
the vocabulary holds only real spelling needs. Its
[`VOCABULARY.md`](../plugins/vale/skills/vale-alerts/VOCABULARY.md) explains
when a term belongs in the allowlist and when it belongs in backticks.

## The `Skills` vocabulary

[`styles/config/vocabularies/Skills/accept.txt`](styles/config/vocabularies/Skills/accept.txt)
holds the allowlist for this repository. Beyond product names and English
technical words, it holds the Norwegian words that
`plugins/norsk/skills/kontrollert-norsk/SKILL.md` uses in prose.

Official lowercase names (prek, uv) go under the "Official lowercase names"
comment in `accept.txt`, each with a link above it that confirms the casing at
the source. The plugin READMEs are the usual source of a bare tool name: link
text such as `[prek](https://prek.j178.dev/)` reaches Vale, while the same name
in backticks does not.
