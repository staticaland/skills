# Cooldowns in container images

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

Developer-machine config does not carry into an image. Where a team maintains
shared base images, bake the cooldown in so nobody has to remember it.

## Relative durations

`uv`, `pip` (26.1+), `npm`, `pnpm`, Bun, Deno, and Yarn all accept relative
durations, which never go stale - set environment variables or copy config files
in at build time:

```dockerfile
FROM quay.io/fedora/fedora

# pip cooldown (26.1+)
ENV PIP_UPLOADED_PRIOR_TO="P3D"

# uv cooldown
ENV UV_EXCLUDE_NEWER="3 days"

# npm cooldown (if you also use Node)
COPY .npmrc /path/to/your/app/dir
```

## Absolute timestamps

For `pip` < 26.1, compute the cutoff in the same `RUN` step that installs, so it
is evaluated at build time:

```dockerfile
FROM quay.io/fedora/fedora

COPY requirements.txt .
RUN PIP_UPLOADED_PRIOR_TO=$(date -u -d '3 days ago' '+%Y-%m-%dT%H:%M:%SZ') \
    pip install -r requirements.txt
```

In a development container where developers also run `pip install`
interactively, drop the wrapper function from [python_pip.md](python_pip.md)
into `/etc/profile.d/` so it is sourced for interactive shells:

```dockerfile
COPY pip-cooldown.sh /etc/profile.d/pip-cooldown.sh
```
