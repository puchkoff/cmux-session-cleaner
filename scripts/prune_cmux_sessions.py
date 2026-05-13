#!/usr/bin/env python3
"""
Prune dead/stale entries from cmux's claude-hook-sessions.json.

Keeps sessions that are either:
- Updated within MAX_AGE_HOURS (recently active, even if process ended)
- Have a live PID (currently running)

Enforces a MAX_SESSIONS hard cap, keeping the most recently updated.
"""
import json
import os
import sys
import time
from pathlib import Path

SESSIONS_FILE = Path.home() / ".cmuxterm" / "claude-hook-sessions.json"
MAX_AGE_HOURS = 48
MAX_SESSIONS = 20

if not SESSIONS_FILE.exists():
    sys.exit(0)

with open(SESSIONS_FILE) as f:
    data = json.load(f)

sessions = data.get("sessions", {})
now = time.time()
cutoff = now - MAX_AGE_HOURS * 3600


def pid_alive(pid):
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def keep(sid, s):
    if s.get("updatedAt", 0) >= cutoff:
        return True
    if pid_alive(s.get("pid")):
        return True
    return False


kept = {k: v for k, v in sessions.items() if keep(k, v)}

if len(kept) > MAX_SESSIONS:
    kept = dict(
        sorted(kept.items(), key=lambda x: x[1].get("updatedAt", 0), reverse=True)[
            :MAX_SESSIONS
        ]
    )

removed = len(sessions) - len(kept)
if removed == 0:
    sys.exit(0)

data["sessions"] = kept

tmp = SESSIONS_FILE.with_suffix(".tmp")
with open(tmp, "w") as f:
    json.dump(data, f, indent=2)
tmp.replace(SESSIONS_FILE)

print(f"Pruned {removed} dead sessions, kept {len(kept)}")
