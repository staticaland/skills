# Scala Steward cooldowns (Maven, Mill, `sbt`, Scala CLI)

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

Maven and Gradle have no native cooldown. The gate here sits at the update bot,
so it holds back pull requests, not resolution - see
[bot_renovate.md](bot_renovate.md) and [bot_github.md](bot_github.md), and lock
dependencies to exact versions alongside it.

## Scala Steward

[Scala Steward](https://github.com/scala-steward-org/scala-steward) is a bot
that opens dependency update PRs. Despite the name it covers **Maven, Mill,
`sbt`, and Scala CLI** (not Gradle). Cooldowns since **0.38.0**, with finer
configuration in 0.38.1, in `.scala-steward.conf` at the repo root:

```properties
updates.cooldown = {
  minimumAge = "3 days"
}
```

Age is counted from when Scala Steward first observed the version, and younger
updates are ignored.

Bypass per dependency:

```properties
updates.cooldown = {
  minimumAge = "3 days"
}

dependencyOverrides = [
  {
    dependency = { groupId = "com.my-company" },
    cooldown = { minimumAge = "1 day" }
  },
  {
    dependency = { groupId = "com.example", artifactId = "foo" },
    cooldown = { minimumAge = "14 days" }
  }
]
```

The first matching entry wins, so list specific patterns before broad ones. Keep
a small cooldown (one day) even on internal libraries, not zero: they still pull
third-party transitive dependencies that may themselves be compromised. See the
[repo-specific configuration docs](https://github.com/scala-steward-org/scala-steward/blob/main/docs/repo-specific-configuration.md).
