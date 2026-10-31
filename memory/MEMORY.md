# Project memory

Kortix is open source, so the target layout is files in a repo the team owns, and every decision
below is one a reviewer can read and reverse.

## Migrations in progress

- `python3 inventory.py --demo` is the worked export: two agents, one complete, one with four
  pieces still to collect. `agents/worker.md` and `skills/migration-checklist/SKILL.md` are what
  the first of them turns into.

## Decisions

- The inventory format has no field for a secret value. A key enters this project through the secret
  store, and the manifest carries only its name.
- One agent per file. A team reviews a prompt change as a diff on one file, not as a config diff.
