# HUMAN.md

## Read this first (5 lines)

1. What it does: tells a traveller which stability clauses they meet, from 10 plan rules read in public wordings.
2. Where it stands: v0.4.0, 10 tests passing, data checked on 2026-11-12.
3. Run it: `PYTHONPATH=src python -m stability_checker --days 60 --age 72`
4. Trust level: every clause links to its source; nothing is advice.
5. Next human decision: below.

## Next human decision

Check each line of `data/clauses.json` against its PDF before any public page uses it. One decision at a time; nothing else is waiting.

## Who decides what

| The human decides and signs | Agents may do |
|---|---|
| Every clause before it is published | Fetch wordings, draft table rows, diff versions |
| Every correction sent by an insurer | Flag a changed clause as "under review" |
| Any referral partner and its disclosure | Count clicks and leads |
| What gets released, and when | Run tests, open pull requests |

Agents never merge to `main`, never publish a clause on their own, and never present output as advice.

## Before spending more tokens

Name the one decision the next run must unblock. If none, stop.

## When something breaks, look in this order

1. `data/clauses.json` (wrong number or outdated wording)
2. `tests/` (missing case)
3. `src/` (logic)
4. The model, last.
