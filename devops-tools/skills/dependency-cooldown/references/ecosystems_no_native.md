# Ecosystems without native cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

Go ([open proposal](https://github.com/golang/go/issues/76485), not accepted),
[NuGet](https://github.com/NuGet/Home/issues/14657),
[Composer](https://github.com/composer/composer/issues/12633),
[Dart's pub](https://github.com/dart-lang/pub/issues/4791), Swift Package
Manager (no request filed), Maven/Gradle, and `conda` have no native cooldown.

For all of these: lock dependencies to exact versions, configure
[Renovate](bot_renovate.md) or [Dependabot](bot_github.md), and consider a
[registry-level proxy](registry_proxies.md). Maven projects can also use
[Scala Steward](jvm_scala_steward.md), though it is little used outside Scala
and does not officially support Gradle.
