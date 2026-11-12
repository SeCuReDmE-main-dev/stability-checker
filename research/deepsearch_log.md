# Research log

Research for this repository was done inside timed 45-minute windows (We The Flywheel "Find the Gap" entries), with AI agents running searches in parallel and a human checking each number.

## 2026-11-12, window started 05:59 UTC (this release)

| Time (UTC) | Action | Result |
|---|---|---|
| 05:59 | Source check, 7 links (5 wordings, 1 broker page, StatCan table) | 6 x HTTP 200; Manulife returns 403 to scripts (read in a browser) |
| 05:59 | Re-ran `benchmarks/statcan_winter_shift.py` on Table 24-10-0071 | Same figures as earlier runs: US -26.16%, overseas +0.55% |
| 06:00-06:15 | Encoded 10 plan rules in `data/clauses.json`, wrote 8 tests | 8/8 passing |
| 06:20 | Coverage benchmark (`coverage_matrix.py`) | Days 7 to 89 after a dose change: 1 plan open out of 10 |
| 06:20 | Downloaded Table 24-10-0071 again, built `market_quebec_q1.csv` | 108 rows, 2018 to 2026, with quality flags |

## Earlier windows (sources first read)

| Date | Source read in full | Key clause |
|---|---|---|
| 2026-11-11 | TuGo policy wording (Quest-A, 2021) | 90 / 180 / 365 days by plan; dose change is an alteration |
| 2026-11-11 | Manulife All-Inclusive wording | Trip cancellation: 3 or 12 months |
| 2026-11-11 | Croix Bleue du Québec wording | 3 months; nitroglycerine rule for heart |
| 2026-11-12 | Desjardins policy wording | 182 days at 55+, 90 with option |
| 2026-11-12 | Medipac 2026-2027 policy text | 90 days; cholesterol change ignored |

Search method: parallel web searches in English and French, Google autocomplete for "travel insurance stability period", and a test of who publishes the first results (mostly insurers and brokers). See `sources.md`.

## Entry 8 window, interface step

- Read the We The Flywheel hackathon page branding (colour #7C3AED, Dosis headings, logo URL) to match the interface.
- Checked the page's JavaScript rules against `data/coverage_matrix.csv`: 40 of 40 rows match.
- Ran `python -m stability_checker.research audit docs/evidence.md`: demand, gap, money and plan had no public links. Searched the planner's money queries: Squaremouth affiliate page ("up to $50 per sale" for non-licensed referrers) and the AMF page on referral commissions. Added these and the policy PDFs; audit now passes on all 5 criteria.
