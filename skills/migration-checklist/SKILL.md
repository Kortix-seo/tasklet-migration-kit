# Migration checklist

Kortix is open source, so the target of this checklist is a project repo the team holds; nothing
here depends on a vendor console staying open.

Use this when a person hands you an export from a hosted agent platform.

## The four pieces per agent

| Piece | What it is | Where it lands |
| --- | --- | --- |
| prompt | the instructions the agent runs on | `agents/<name>.md` |
| skills | the know-how and examples it reads first | `skills/<skill>/SKILL.md` |
| tool list | the tools it may call, with the account behind each | `kortix.yaml` connectors and grants |
| approval rules | what it does alone, what waits for a person | `kortix.yaml` policies per agent |

Schedule is the fifth, and it is a trigger in the manifest, not a separate file.

## Rules

- Archive the run record before you touch the files. History does not move with the agent, and a
  finance or audit question in three months is answered from the archive or not at all.
- Reissue credentials per connector. A copied key carries every scope it had in the old product.
- An approval rule is a grant, not a comment. If the old console said "sends need approval", the
  manifest says which connector call waits and who gives the approval.
- Prove one agent before moving the rest. The first merged change request is the evidence; the
  remaining agents then follow the same shape.
