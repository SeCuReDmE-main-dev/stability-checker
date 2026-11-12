# Evidence sheet: Stable Enough / stability-checker

One page, plain text, every claim tied to a file or a public source. Numbers come from files in this repository and can be recomputed with `python benchmarks/coverage_matrix.py` and `python benchmarks/statcan_winter_shift.py`.

## The question people ask

"My doctor changed my dose last month. Am I still covered in Florida this winter?" Each Canadian travel medical policy answers it with a different *stability period* (the number of days a condition must stay unchanged before the trip). The rules are buried in 40-page wordings.

## Demand

| Fact | Value | Source |
|---|---|---|
| Quebec residents' trips to the US, Q1 2026 | 398,000 (−26.16 % vs Q1 2025, quality flag B) | Statistics Canada Table 24-10-0071: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2410007101 , `benchmarks/statcan_q1_2025_2026.md` |
| Quebec residents' trips overseas, Q1 2026 | 1,098,000 (flag A) | same table |
| Nights per US visit, winter vs summer | 9.1 vs 5.7 | same table, `benchmarks/statcan_winter_shift.py` |
| What RAMQ pays on a US ICU stay billed $25,000 | $300 (hospital cap $100/day) | RAMQ: https://www.ramq.gouv.qc.ca/fr/citoyens/absence-quebec/connaitre-services-couverts-hors-quebec |

## The gap, measured

From `data/coverage_matrix.csv` (10 plan rules read from public wordings, `data/clauses.json`):

| Days since a dose change (age 72, condition "other") | Plans open |
|---|---|
| 0 | 0 of 10 |
| 7 to 89 | 1 of 10 (TuGo 7-day option, listed by a broker) |
| 90 | 6 of 10 |
| 182 | 9 of 10 |
| 365 | 10 of 10 |

Wordings also disagree on what counts as a change: Medipac ignores a cholesterol drug change; Croix Bleue excludes a heart condition if nitroglycerine was used more than once in 7 days. I found no comparison site that shows these rules side by side.

Policy wordings read: Desjardins https://www.desjardins.com/content/dam/pdf/fr/particuliers/assurances/voyage/police-assurance.pdf · Medipac https://www.medipac.com/UserFiles/files/MedipacPolicyText.pdf · Croix Bleue https://qc.croixbleue.ca/images/docs/Qc_Policy-fr.pdf · Manulife https://www.manulife.com/content/dam/consumer-portal/documents/en/travel/single-trip-all-inclusive-policye.pdf

## The product

- Live checker: https://securedme-main-dev.github.io/stability-checker/?days=60&age=72&condition=other&change=dose
- Research planner and evidence audit: `python -m stability_checker.research plan` prints 29 searches by scoring criterion; `audit docs/evidence.md` checks each criterion has public links and figures.
- Python engine and CLI: `src/stability_checker/checker.py`, 10 tests in CI on Python 3.10 and 3.12.
- Each answer links to the clause it comes from; the page states "information, not advice" above the result.

## Money

Published referral rates for travel insurance: Squaremouth, "non-licensed referrers can make up to $50 per sale" (https://www.squaremouth.com/about/affiliates); InsureandGo 12 %; Arch RoamRight cites 28 % as an industry average. In Quebec, the AMF describes the *commission de référencement* paid to a referrer (https://lautorite.qc.ca/professionnels/cabinets-societes-et-representants-autonomes/obligations-et-formalites-administratives/paiement-de-la-remuneration); Assur360 and SécuriGlobe run referral programs. Sources in `research/sources.md`.

## Operator plan

Day 0 is done (engine, data, tests, page). Next: add the 20 most-sold Quebec plans to `data/clauses.json` (one pull request per wording, template: https://github.com/SeCuReDmE-main-dev/stability-checker/blob/main/.github/ISSUE_TEMPLATE/clause_update.md), then sign one referral agreement before the October renewal season.

## Limits

10 plan rules, not the whole market. Clauses change every policy year; each rule carries its source and section so it can be rechecked. Not insurance advice.
