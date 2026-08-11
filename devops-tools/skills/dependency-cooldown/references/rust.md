# Rust cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

## Cargo

No native cooldown on stable. Cargo 1.94 added `pubtime` fields to the crate index (the prerequisite), [RFC #3923](https://github.com/rust-lang/rfcs/blob/master/text/3923-cargo-min-publish-age.md) is accepted, and the unstable `-Zmin-publish-age` feature has landed on nightly (since nightly-2026-06-21). Stabilization is tracked in [cargo#17009](https://github.com/rust-lang/cargo/issues/17009).

## cargo-cooldown

Until then, use the third-party [`cargo-cooldown`](https://crates.io/crates/cargo-cooldown) crate. It is a **subcommand, not a transparent wrapper** - `COOLDOWN_MINUTES` alone does nothing, and every command must be run through `cargo cooldown`.

```bash
cargo install cargo-cooldown
export COOLDOWN_MINUTES=4320  # 3 days, in minutes
cargo cooldown build
```

Bypass a crate in `cooldown.toml`:

```toml
[[allow.package]]
crate = "openssl"
min-publish-age = "0"

[[allow.exact]]
crate = "serde"
version = "1.0.218"
```
