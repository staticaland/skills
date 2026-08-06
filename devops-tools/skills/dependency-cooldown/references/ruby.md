# Ruby cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

## Bundler

Native cooldown since **4.0.13**. The value is always a non-negative integer number of days — a string, float, negative number, or array is rejected.

```bash
bundle install --cooldown 3        # also on update, add, outdated
bundle config set cooldown 3       # current project
bundle config set --global cooldown 3
export BUNDLE_COOLDOWN=3
```

Per source in the `Gemfile`:

```ruby
source "https://rubygems.org", cooldown: 3
```

Override hierarchy: command-line flag > configuration setting > per-source `Gemfile` declaration.

Bypass for a whole run with `bundle install --cooldown 0`. There is no per-gem exemption, but a per-source override exempts everything from one registry:

```ruby
source "https://gems.internal.example.com", cooldown: 0 do
  gem "internal-tool"
end
```

Bundler **fails open**: it only holds back versions it can prove are too new, so releases with no `created_at` timestamp (older servers, v1-format registries, private gems) stay resolvable. See the [RubyGems announcement](https://blog.rubygems.org/2026/06/03/cooldown-let-new-gems-be-vetted.html).

The community-run [gem.coop](https://gem.coop) index is beta-testing a 48-hour registry-level delay on newly published gems.
