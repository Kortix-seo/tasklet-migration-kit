# From an export to a Kortix project

The order here is the one this kit is built around. The script in the repository root does the inventory, and the files under `agents/` and `skills/` do the writing. Two steps belong to a person. Archive the run record before access ends, and reissue every credential instead of copying it.

## Archive the run record before you touch a file

A migration moves text. What it leaves behind is an account of what the agents already did: each run, its input, its output, and who approved it. That record sits in the vendor's cloud and stops being readable on the day you cancel.

Copy it first, while the account is open and the exports still work. One export per agent, in whatever the product offers, plus screenshots only where the export drops a field you need. Name the files with the agent and the date range, so a later search finds them. `support-triage-2026-01-01_2026-10-31.csv` beats `export (3).zip`.

How long to keep it: measure from the farthest question any of these will ask. Your audit cycle, the retention a customer contract names, and the far edge of what your own support team answers. If a finance team will ask in March which refunds ran in July, the answer comes from the archive or it does not come at all.

Store it where the company keeps records, with a copy, not on the laptop of the person doing the migration.

## The four pieces per agent

Every agent is four pieces of text, plus a schedule. The names differ from product to product; the pieces do not.

| Piece | Where it lives in the old product | File it becomes |
| --- | --- | --- |
| prompt | the agent's instructions screen | `agents/<name>.md` |
| skills | the saved skills or instruction library | `skills/<skill>/SKILL.md` |
| tool list | the connections or tools panel | connectors in `kortix.yaml` |
| approval rules | the approval or autonomy settings | grants in `kortix.yaml` |
| schedule | the schedule or trigger setting | a trigger in `kortix.yaml` |

Write each piece out in plain text before you write any configuration. `inventory.py` gives you the folder shape, and each file it expects is one of these pieces, so a folder that inventories clean is a folder you have already collected.

The prompt is the cheap part. It is already written, and the work is copying it into a file that takes a diff. Teams budget weeks for it because it reads like writing, then discover that the expensive part was the run record they no longer have.

Approval rules deserve their own pass. Tasklet describes the idea in one sentence on [tasklet.ai](https://tasklet.ai): "Decide what your agents can do on their own, and what they need permission for. They'll reach out when they need your approval." Copy the rules as sentences first, in the words the owner of the account uses. Then turn each sentence into a grant: the connector call the agent may make alone, the one that needs someone's approval first, and the one it may never make.

## Reissue the credentials, do not copy them

The credential step decides whether this was a move or a duplicate. A key copied out of the old product arrives with every scope somebody chose months ago. That scope reaches every board and mailbox it covered, and its use history is something you cannot read.

Issue new keys instead. One per connector, limited to the systems that agent really needs. Store the value in the secret store, so the manifest holds only the name. Where a connector supports it, let Kortix broker the credential: connector credentials are brokered server-side and never enter the machine, so the key is not sitting in a working directory an agent can read.

Track the work in the export's `credentials.csv`. Every row the inventory printed as `to reissue` gets a new key. The key exists when its `kid` cell is filled in, and the next run of `inventory.py` shows what is left. A row with a blank `kid` is unfinished work, which is the point of putting the column in the file.

Revoke the old key after the overlap, not before. Two live copies for the week of the trial is a controlled risk. Two live copies for a quarter is how a migration becomes an incident.

## Prove it on one real job

Pick one agent and one job you actually needed. Choose the agent that does work somebody would notice if it stopped, even if it is the messiest one in the export.

Bring up the new instance, on hardware you control or on Kortix Cloud:

```
curl -fsSL https://kortix.com/install | bash
kortix self-host init --domain kortix.example.com --admin-email you@example.com
kortix self-host start
```

Kortix is open source, so the instance these three commands bring up is one the company controls, on hardware you choose, rather than a tenant inside someone else's product.

Then run the smoke test before you trust a schedule to it. `kortix doctor` verifies your login and the project. Then it starts a throwaway session, sends it a ping, waits for the agent's reply and deletes the session. It exits with a failure when a check does not pass. A failing check here is cheaper than a failing run at 03:00.

Run the job on both systems for a week and compare what comes back, including the parts nobody reads: the diff, the drafts, the messages that went out. The old side hands you a thread to scroll. The new side hands you a branch, so the week's work is reviewable line by line before it lands. Keep that review as part of the test. Open a change request from the session, read it, merge it yourself, and check that what landed matches what the old side produced.

Cancel once a week of those diffs has looked right to the person who owns the work.

## Checklist to paste into an issue

```markdown
- [ ] run record exported per agent, dated filenames, a copy where the company keeps records
- [ ] every agent folder collected: prompt, skills, tool list, approval rules, schedule
- [ ] `python3 inventory.py <export_dir>` exits 0
- [ ] one prompt file per agent under `agents/`
- [ ] one folder per skill under `skills/`, with the original examples kept
- [ ] connectors declared in `kortix.yaml`; grants written from the approval rules
- [ ] a trigger for each schedule that was collected
- [ ] every `credentials.csv` row reissued, `kid` filled in, old keys still live for the trial
- [ ] `kortix doctor` passes on the new instance
- [ ] one real job run on both systems for a week, outputs compared
- [ ] a person merged the change request that came out of the new side
- [ ] old credentials revoked, old plan canceled
```
