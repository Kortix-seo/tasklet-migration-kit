#!/usr/bin/env python3
"""Inventory a hosted agent platform export before moving it into a git repo.

Point it at a folder that has one subfolder per agent. Each agent folder may hold:

    prompt.md        the instructions the agent runs on
    skills/          one folder per skill, each with a SKILL.md inside
    tools.txt        one tool or connector per line
    approvals.txt    one rule per line: what the agent may do alone, what waits for a person
    schedule.txt     when the agent runs, in plain words

and a `credentials.csv` at the folder root with the columns `system,account,kid` (kid is to be
filled in after the key is reissued).

The script is read only. It prints one line per agent and one line per credential, and it never
prints a secret value: the export format has no field for one on purpose.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

PIECES = ("prompt.md", "skills", "tools.txt", "approvals.txt", "schedule.txt")
PIECE_LABEL = {
    "prompt.md": "prompt",
    "skills": "skills",
    "tools.txt": "tool list",
    "approvals.txt": "approval rules",
    "schedule.txt": "schedule",
}


def count_skills(agent_dir: Path) -> int:
    skills = agent_dir / "skills"
    if not skills.is_dir():
        return 0
    return sum(1 for d in skills.iterdir() if d.is_dir() and (d / "SKILL.md").is_file())


def describe_piece(agent_dir: Path, piece: str) -> str | None:
    path = agent_dir / piece
    if piece == "skills":
        n = count_skills(agent_dir)
        return f"{n} skill folder{'s' if n != 1 else ''}" if n else None
    if not path.is_file():
        return None
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return None
    if piece == "prompt.md":
        return f"{len(lines)} lines"
    return f"{len(lines)} entr{'ies' if len(lines) != 1 else 'y'}"


def inventory(root: Path) -> int:
    if not root.is_dir():
        print(f"error: {root} is not a folder", file=sys.stderr)
        return 2

    agents = sorted(p for p in root.iterdir() if p.is_dir())
    if not agents:
        print(f"error: no agent folders under {root}", file=sys.stderr)
        return 2

    total_missing = 0
    print(f"export: {root}")
    print(f"agents: {len(agents)}")
    for agent in agents:
        found, missing = [], []
        for piece in PIECES:
            detail = describe_piece(agent, piece)
            if detail:
                found.append(f"{PIECE_LABEL[piece]} ({detail})")
            else:
                missing.append(PIECE_LABEL[piece])
        total_missing += len(missing)
        print(f"\n[{agent.name}]")
        print(f"  move:    {', '.join(found) if found else 'nothing found'}")
        print(f"  collect: {', '.join(missing) if missing else 'complete'}")
        if missing:
            print(f"  file:    agents/{agent.name}.md {'(rewrite from the pieces you collect)' if 'prompt' in missing else ''}".rstrip())

    creds = root / "credentials.csv"
    print("\ncredentials")
    if not creds.is_file():
        print("  none listed: add credentials.csv (system,account,kid) before you reissue keys")
    else:
        rows = list(csv.DictReader(creds.open(encoding="utf-8")))
        if not rows:
            print("  none listed")
        for row in rows:
            system = row.get("system", "").strip() or "?"
            account = row.get("account", "").strip() or "?"
            kid = row.get("kid", "").strip()
            state = f"reissued as {kid}" if kid else "to reissue"
            print(f"  {system:<12} {account:<28} {state}")

    print(f"\nresult: {total_missing} piece{'s' if total_missing != 1 else ''} still to collect")
    print("next: one file per agent under agents/, one folder per skill under skills/, the rest in kortix.yaml")
    return 0 if total_missing == 0 else 1


DEMO = {
    "support-triage/prompt.md": "# Support triage\n\nRead the overnight queue in Zendesk. Group tickets by product area. For every ticket that\nmentions a refund, check the order in Stripe and the policy in Notion, then draft a reply.\nOpen a change request with the digest and the drafts. Never send.\n",
    "support-triage/tools.txt": "zendesk.search\nzendesk.read_ticket\nstripe.read_charge\nnotion.read_page\nkortix_slack.post_message\n",
    "support-triage/approvals.txt": "read: zendesk.search, zendesk.read_ticket, stripe.read_charge, notion.read_page\nwait for a person: kortix_slack.post_message, any refund above 100 USD\nnever: stripe.create_refund\n",
    "support-triage/schedule.txt": "Weekdays at 08:00 Europe/Berlin, on a cron.\n",
    "support-triage/skills/refund-policy/SKILL.md": "# Refund policy\n\nRead `policy/refunds.md` from the company Notion page before drafting. A refund above 100 USD\nor older than 30 days needs a person to approve it in the thread. Quote the policy line in the\ndraft so the customer sees the rule that decided the answer.\n",
    "weekly-digest/prompt.md": "# Weekly digest\n\nEvery Monday, collect the closed tickets from the week, count them by product area, and open a\nchange request with a one-page summary.\n",
    "credentials.csv": "system,account,kid\nzendesk,support@acme.example,\nstripe,acme-live-01,\nnotion,ops@acme.example,\n",
}


def write_demo(root: Path) -> None:
    """Write the worked example export the README shows. Nothing secret: the
    credentials file carries account names and an empty reissue column."""
    for rel, text in DEMO.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory a hosted agent platform export.")
    parser.add_argument("export_dir", type=Path, nargs="?", help="folder with one subfolder per agent")
    parser.add_argument("--demo", action="store_true", help="inventory the built-in worked example")
    args = parser.parse_args()
    if args.demo:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            previous = Path.cwd()
            os.chdir(tmp)
            try:
                write_demo(Path("acme-support"))
                return inventory(Path("acme-support"))
            finally:
                os.chdir(previous)
    if not args.export_dir:
        parser.print_help()
        return 2
    return inventory(args.export_dir)


if __name__ == "__main__":
    raise SystemExit(main())
