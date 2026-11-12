# AGENTS.md

Instructions for AI coding agents working in this repository. Read `HUMAN.md` first.

## Project map

- `data/clauses.json`: one entry per plan rule, with `source` and `section`. The single source of truth.
- `src/stability_checker/checker.py`: pure functions, standard library only.
- `tests/test_checker.py`: `unittest`, no network.
- `research/`: search logs and source checks. `benchmarks/`: market figures and the link checker.

## Commands

```bash
python -m unittest discover -s tests          # must pass before any commit
PYTHONPATH=src python -m stability_checker --days 60 --age 72
python benchmarks/link_check.py                # network; not part of CI
```

## Rules

1. Every new or changed clause needs: a public `https://` source, the section name, the date checked, and a test.
2. Paraphrase in one or two sentences. Never paste full policy text.
3. Never describe output as advice. Keep the disclaimer in README and CLI output.
4. No new runtime dependencies without a human decision.
5. Do not commit secrets, personal data, or files under `.claude/` other than `settings.json`.
6. Open a pull request; a human merges. Do not push to `main`.

## Done means

Tests pass, `clauses.json` is valid JSON, every source link answers, `CHANGELOG.md` is updated.
