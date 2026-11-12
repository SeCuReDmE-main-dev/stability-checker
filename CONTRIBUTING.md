# Contributing

Thank you for helping keep these clauses accurate.

## Propose or correct a clause

1. Open a "Clause update" issue with the insurer, plan, the public wording link, the section, and the date you read it.
2. Or send a pull request that edits `data/clauses.json` and adds a test in `tests/test_checker.py`.
3. One source per clause. Paraphrase; do not paste full policy text.

## Code changes

- Python 3.10+, standard library only.
- `python -m unittest discover -s tests` must pass.
- Keep functions pure and small.

## Sign-off (DCO)

Sign each commit with `git commit -s` to certify the [Developer Certificate of Origin](https://developercertificate.org/).

## Conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md).
