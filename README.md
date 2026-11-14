# 02-120 Build Journal

Code and Claude Code session logs for 02-120.

## Layout

| Path | What's in it |
| --- | --- |
| `project/` | Python code for the course project |
| `sources/` | Papers the project is based on (Rothman et al. 2014) |
| `journal/` | Claude Code session logs (`.jsonl`), one file per session |
| `.claude/` | Claude Code settings and the hook that saves the session logs |

## Running the code

Requires Python 3.

```
python3 project/main.py
```

## How the journal works

`.claude/hooks/save_journal.py` runs at the start and end of every Claude Code
session opened in this folder. It copies that session's log into `journal/`.
Sessions started from a different folder are not saved automatically; copy
their logs into `journal/` by hand.

To run the hook manually:

```
python3 .claude/hooks/save_journal.py
```
