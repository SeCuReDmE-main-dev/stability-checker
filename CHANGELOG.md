# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [0.4.0] - 2026-11-12

### Added
- Stella and the logo redrawn in the We The Flywheel palette.
- Web checker: "days until you leave" field, "opens in N more days" on each closed plan, and Stella the snowbird telling you how many plans open if your treatment stays the same a little longer.
- `stability_checker.research`: `plan` prints 29 searches grouped by the Find the Gap scoring criteria (demand, gap, concept, money, plan); `audit` checks that each criterion in an evidence sheet has public links and figures.
- `docs/evidence.md`: public links for every criterion (Statistics Canada, RAMQ, 4 policy wordings, Squaremouth affiliate page, AMF).
- Tests: web page vs Python parity on 1,680 cases, no-tracking check, research planner and audit, page script syntax check (17 tests).
- CI runs the evidence audit.

## [0.3.0] - 2026-11-12

### Added
- `docs/index.html`: bilingual web checker (GitHub Pages), same rules as the Python engine; shareable cases through the URL (`?days=60&age=72`); benchmark table computed in the page.
- `docs/evidence.md` and `docs/llms.txt`: one-page evidence sheet, each claim tied to a file or public source.
- `DESIGN.md`, `assets/logo.svg`, `assets/mascot.svg` (Stella the snowbird).
- Parity check: the page's rules give the same 40 results as `data/coverage_matrix.csv`.

## [0.2.0] - 2026-11-12

### Added
- `coverage()` function: plans still open by days since the last change.
- `data/coverage_matrix.csv` (40 rows) and `benchmarks/coverage_matrix.py`.
- `data/market_quebec_q1.csv` (108 rows) and `benchmarks/market_table.py`, from Statistics Canada Table 24-10-0071.
- 2 tests (10 total).

## [0.1.0] - 2026-11-12

### Added
- `data/clauses.json`: 10 plan rules from 5 insurers (Desjardins, Medipac, Croix Bleue du Québec, TuGo, Manulife), each with source and section.
- `stability_checker` CLI and library.
- 8 unit tests, including the 60-day dose change case.
- Research log, source check and Statistics Canada benchmark.
- HUMAN.md, AGENTS.md, SECURITY.md, CONTRIBUTING.md, Code of Conduct, CITATION.cff.
