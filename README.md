# cmux-session-cleaner

A Claude Code plugin that prevents [cmux](https://cmux.app) from accumulating memory by pruning dead Claude Code session entries from `~/.cmuxterm/claude-hook-sessions.json`.

## Problem

cmux tracks Claude Code sessions in `~/.cmuxterm/claude-hook-sessions.json`. This file grows indefinitely — dead sessions (with gone PIDs) are never removed, and cmux retains all of them in memory. On active machines this can contribute to cmux reaching tens of GB of RAM usage (see [manaflow-ai/cmux#2871](https://github.com/manaflow-ai/cmux/issues/2871)).

## What this plugin does

- Fires on every Claude Code prompt (`UserPromptSubmit`) and session end (`Stop`)
- Removes session entries whose process is dead and last activity was >48 hours ago
- Enforces a hard cap of 20 sessions maximum
- Atomic write — no corruption risk

## Install

```bash
claude plugins install puchkoff/cmux-session-cleaner
```

Or manually add to `~/.claude/settings.json`:

```json
"extraKnownMarketplaces": {
  "puchkoff": {
    "source": {
      "source": "github",
      "repo": "puchkoff/cmux-session-cleaner"
    }
  }
}
```

Then: `claude plugins install cmux-session-cleaner@puchkoff`

## Configuration

Edit `MAX_AGE_HOURS` and `MAX_SESSIONS` at the top of `scripts/prune_cmux_sessions.py` to tune retention.

## License

MIT
