# Elixir cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

## Hex

Built in since **[2.5.0](https://github.com/hexpm/hex/releases/tag/v2.5.0)**. The `cooldown` key takes `<N>d` (days), `<N>w` (weeks), or `<N>mo` (months).

```bash
mix hex.config cooldown 3d
export HEX_COOLDOWN="3d"
```

Project config in `mix.exs`:

```elixir
def project do
  [
    # ...
    hex: [cooldown: "3d"]
  ]
end
```

Bypass per repository — the useful case when an organization publishes hotfixes to its own repo:

```bash
mix hex.config cooldown_exclude_repos '["hexpm:myorg"]'
export HEX_COOLDOWN_EXCLUDE_REPOS="hexpm:myorg"   # comma-separated
```

Hex **fails open**: releases without a `published_at` timestamp stay resolvable. Packages already in the lockfile skip the cooldown entirely, and a package locked to a retired version or one with a security advisory may re-resolve during the cooldown.
