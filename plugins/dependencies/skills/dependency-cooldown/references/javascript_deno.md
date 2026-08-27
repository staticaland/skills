# Deno cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

`minimumDependencyAge` since **2.6**. A 24-hour gate applies by default since
**2.9** and any explicit setting overrides it. Takes **minutes, an ISO 8601
duration, or an RFC 3339 timestamp**. In `deno.json`:

```json
{
  "minimumDependencyAge": "P3D"
}
```

Bypass with the object form:

```json
{
  "minimumDependencyAge": {
    "age": "P3D",
    "exclude": ["npm:@mycompany/cli", "jsr:@mycompany/lib"]
  }
}
```

CLI: `deno install|update|outdated --minimum-dependency-age=P3D`.
