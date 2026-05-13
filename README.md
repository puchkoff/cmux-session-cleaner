# cmux-session-cleaner

A Claude Code plugin that prevents [cmux](https://cmux.app) from accumulating memory by pruning dead Claude Code session entries from `~/.cmuxterm/claude-hook-sessions.json`.

## Problem

cmux tracks Claude Code sessions in `~/.cmuxterm/claude-hook-sessions.json`. This file grows indefinitely — dead sessions (with gone PIDs) are never removed, and cmux retains all of them in memory. On active machines this can contribute to cmux reaching tens of GB of RAM usage (see [manaflow-ai/cmux#2871](https://github.com/manaflow-ai/cmux/issues/2871)).

## Install

```bash
claude plugins marketplace add puchkoff/cmux-session-cleaner
claude plugins install cmux-session-cleaner@cmux-session-cleaner
```

## What it does

- Fires on every Claude Code prompt (`UserPromptSubmit`) and session end (`Stop`)
- Removes session entries whose process is dead and last activity was >48 hours ago
- Enforces a hard cap of 20 sessions maximum
- Atomic write — no corruption risk

## Configuration

Edit `MAX_AGE_HOURS` and `MAX_SESSIONS` at the top of `scripts/prune_cmux_sessions.py` to tune retention.

## License

MIT
