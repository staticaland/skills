# Private PyPI registry cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

Upload times come only from the JSON version of the PyPI Simple API, so
HTML-only indexes carry no timestamps. On missing metadata, `uv` and `pip`
**fail closed** (reject the version) while Poetry **fails open**. JFrog
Artifactory needs the PyPI Simple JSON API enabled, available from 7.139.1
(SaaS, February 2026) or 7.146 (self-hosted, April 2026).
