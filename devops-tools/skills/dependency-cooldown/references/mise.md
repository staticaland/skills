# mise cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

[mise](https://mise.jdx.dev/) takes a relative or absolute date, and applies a 24-hour default since **v2026.6.2**.

```toml
[settings]
minimum_release_age = "3d"
```

Override per tool:

```toml
[tools.trivy]
version = "latest"
minimum_release_age = "1d"
```

Bypass with [`minimum_release_age_excludes`](https://mise.jdx.dev/configuration/settings.html#minimum_release_age_excludes), or by pinning a version (a pinned version installs regardless):

```toml
[settings]
# Trivy and everything on the npm backend gets no cooldown
minimum_release_age_excludes = ["trivy", "npm:*"]

[tools]
node = "22.5.0"
```

**Not every mise backend supports minimum release age** — see the [security docs](https://mise.jdx.dev/security.html#minimum-release-age). List a backend's packages with `mise registry | grep '  npm:'`, and packages that fall back to it with `mise registry | grep -v '  npm:' | grep ' npm:'`.
