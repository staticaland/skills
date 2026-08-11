# Registry-level proxy cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

A caching proxy in front of public registries enforces cooldowns for every tool
behind it, **overriding any project or CI config** and covering tools with no
native support. JFrog Artifactory and Sonatype Nexus quarantine newly published
versions for a configurable period, across every ecosystem they proxy, including
`npm`, PyPI, and Maven.

For self-hosted `npm`, [Verdaccio](https://verdaccio.org/) does the same through
its bundled `@verdaccio/package-filter` plugin: set `minAgeDays` to hide
versions published less than N days ago. The plugin is disabled by default.
