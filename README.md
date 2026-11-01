# tasklet-migration-kit

This repo is a Kortix project, and Kortix is the open-source CompanyOS: your agents, their skills, your company memory, and every connector in one git repo you own, with the agents working on real cloud computers. The script here inventories what an export from a hosted agent product holds, and the rest of this file is the Kortix layout it moves onto.

What a migration carries is four pieces of text per agent and a list of credentials. The export is what you wrote, because there is no running process to move. That is why a team can budget a month for the prompt rewrite and still lose the run history, which is the one part that does not travel. The migration that goes wrong is usually the one planned around the wrong artifact.

## What the script checks

Point it at a folder with one subfolder per agent. For each agent it looks for five things:

- `prompt.md`, the instructions the agent runs on.
- `skills/`, one folder per skill, each with a `SKILL.md` inside.
- `tools.txt`, one tool or connector per line.
- `approvals.txt`, one rule per line: what the agent may do alone, what waits for a person.
- `schedule.txt`, when the agent runs, in plain words.

At the folder root it reads `credentials.csv` with the columns `system,account,kid`, and prints one line per credential. A blank `kid` means the key has not been reissued yet. The format has no column for a secret value, on purpose, so a checklist of key names can sit in the repository without carrying one.

## Quick start

```
python3 inventory.py --demo
```

The demo writes a worked example export into a temporary folder, inventories it, and removes the folder when it exits. That export holds two agents, one complete and one with four pieces still to collect. The script changes nothing in your project, prints this, and exits 1 because pieces are missing:

```
export: acme-support
agents: 2

[support-triage]
  move:    prompt (4 lines), skills (1 skill folder), tool list (5 entries), approval rules (3 entries), schedule (1 entry)
  collect: complete

[weekly-digest]
  move:    prompt (3 lines)
  collect: skills, tool list, approval rules, schedule
  file:    agents/weekly-digest.md

credentials
  zendesk      support@acme.example         to reissue
  stripe       acme-live-01                 to reissue
  notion       ops@acme.example             to reissue

result: 4 pieces still to collect
next: one file per agent under agents/, one folder per skill under skills/, the rest in kortix.yaml
```

The exit code is 0 when every piece is present and 1 when something is still to collect, so the same command can gate a pull request once an export is in the repository. When you have a real export, pass its folder instead of the flag: `python3 inventory.py <export_dir>`.

## Where the pieces land

A migrated agent in a Kortix project looks like this:

```
agents/<name>.md            the prompt: one file per agent
skills/<skill>/SKILL.md     the skill: one folder per skill
kortix.yaml                 connectors, grants and the trigger
memory/MEMORY.md            what the team decided along the way
```

The prompt becomes the file, in full, with its examples. The skill becomes a folder, and it keeps the examples the original skill carried, because those examples are what made the agent behave. The tool list becomes connectors in `kortix.yaml`, and each approval rule becomes a grant that names what the agent may call alone, what waits for a person, and what it may never call. The schedule becomes a trigger. `memory/MEMORY.md` holds the decisions a person would otherwise re-explain at every session: which credential went where, and why one agent sends and another only drafts.

Those three files are in this repository, and they are the Kortix side of the move: `agents/worker.md` is the prompt for the agent that runs a migration, `skills/migration-checklist/SKILL.md` is the checklist it follows, and `memory/MEMORY.md` records the decisions the worked example made. A migrated agent lands in the same shape, with its prompt as one file under `agents/`, its skills as folders under `skills/`, and its connectors and grants in `kortix.yaml`.

## The manifest a Kortix project starts from

The repository ships that manifest at its root, in `kortix.yaml`, so a clone of it is already a Kortix project. These are the parts that matter to a migration:

```yaml
project:
  name: "tasklet-migration-kit"

default_agent: worker

skills:
  - migration-checklist

agents:
  worker:
    mode: primary
    permission: allow
    prompt_file: agents/worker.md
    tools: all
    skills: all
    connectors: all
    secrets: all
    kortix_permissions: all
    workspace: { project_repository: true }
```

Each block under `agents:` names one prompt file, the grants that agent holds, and the credentials it may reach. Under `skills:`, each entry is a folder in `skills/` registered by name, which is how `migration-checklist` is wired. A schedule you collected becomes an entry under `triggers:`, which the shipped manifest leaves to you, with a commented example to copy. The Kortix docs carry a reference for every key.

## What does not come across

- The run history. Every run, its input, its output and who approved it stays in the vendor's cloud and stops being readable the day you cancel. `docs/MIGRATION.md` opens with it.
- The live connection configuration. A connection is a credential plus a mapping held on the vendor's side, and only the credential half can be reissued.
- The credits. Tasklet bills work in credits, so a balance left on a plan is money already spent on a service you are leaving ([tasklet.ai/pricing](https://tasklet.ai/pricing)).

## Where to read next

- `docs/MIGRATION.md`: archive the run record first, the four pieces per agent, the credential step, and the week that proves the new setup before you cancel.
- The migration walkthrough: [taskletalternative.com/migrate-from-tasklet](https://taskletalternative.com/migrate-from-tasklet).
- The four products a Tasklet searcher is usually offered, each cell taken from that vendor's own page, with what open source changes about the answer: [taskletalternative.com/tasklet-alternatives](https://taskletalternative.com/tasklet-alternatives).
- If the reason for leaving is custody rather than features, [taskletalternative.com/self-hosted-tasklet-alternative](https://taskletalternative.com/self-hosted-tasklet-alternative) walks the route where the control plane runs on machines you choose.
- Kortix docs: [kortix.com/docs](https://kortix.com/docs).

Kortix is open source. Self-host is free, and `docs/MIGRATION.md` has the three commands that bring up an instance you own.
