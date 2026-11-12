# Evidence sheet: Stable Enough / StellaCheck

One page, plain text, every claim tied to a file or a public source. Numbers come from files in this repository and can be recomputed with `python benchmarks/coverage_matrix.py` and `python benchmarks/statcan_winter_shift.py`.

## The question people ask

"My doctor changed my dose last month. Am I still covered in Florida this winter?" Each Canadian travel medical policy answers it with a different *stability period* (the number of days a condition must stay unchanged before the trip). The rules are buried in 40-page wordings.

## Demand

| Fact | Value | Source |
|---|---|---|
| Quebec residents' trips to the US, Q1 2026 | 398,000 (−26.16 % vs Q1 2025, quality flag B) | Statistics Canada Table 24-10-0071: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2410007101 , `benchmarks/statcan_q1_2025_2026.md` |
| Quebec residents' trips overseas, Q1 2026 | 1,098,000 (flag A) | same table |
| Nights per US visit, winter vs summer | 9.1 vs 5.7 | same table, `benchmarks/statcan_winter_shift.py` |
| A public post: "a minor change to your prescription could leave you completely unprotected" | Snowbird question in the wild | https://www.facebook.com/canadatousa/posts/a-minor-change-to-your-prescription-could-leave-you-completely-unprotected-this-/1402369158554314/ |
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

Wordings also disagree on what counts as a change: Medipac ignores a cholesterol drug change; Croix Bleue excludes a heart condition if nitroglycerine was used more than once in 7 days. I found no comparison site that shows these rules side by side. A search for "stability period travel insurance medication change" (English and French, 2026-11-12) returns explainers from Snowbird Advisor, Mediquote, CAA-Québec, Protecto and TuGo's own blog: each says the period "varies" between 90 and 365 days, and none lists the rule insurer by insurer. All 17 sources, tagged by criterion: `data/sources_index.json`.

Policy wordings read: Desjardins https://www.desjardins.com/content/dam/pdf/fr/particuliers/assurances/voyage/police-assurance.pdf · Medipac https://www.medipac.com/UserFiles/files/MedipacPolicyText.pdf · Croix Bleue https://qc.croixbleue.ca/images/docs/Qc_Policy-fr.pdf · Manulife https://www.manulife.com/content/dam/consumer-portal/documents/en/travel/single-trip-all-inclusive-policye.pdf

## The product

- StellaCheck, the live checker: https://securedme-main-dev.github.io/stability-checker/?days=60&age=72&condition=other&change=dose
- Research planner and evidence audit: `python -m stability_checker.research plan` prints 29 searches by scoring criterion; `audit docs/evidence.md` checks each criterion has public links and figures.
- Python engine and CLI: `src/stability_checker/checker.py`; 35 tests run in CI on Python 3.10 and 3.12 (https://github.com/SeCuReDmE-main-dev/stability-checker/actions), including 1,680 cases where the web page and the Python engine must agree and a check that waiting longer never closes a plan.
- Code and data, Apache-2.0: https://github.com/SeCuReDmE-main-dev/stability-checker
- Each answer links to the clause it comes from; the page states "information, not advice" above the result.

## Money

Published referral rates for travel insurance: Squaremouth, "non-licensed referrers can make up to $50 per sale" (https://www.squaremouth.com/about/affiliates); InsureandGo 12 %; Arch RoamRight cites 28 % as an industry average. In Quebec, the AMF describes the *commission de référencement* paid to a referrer (https://lautorite.qc.ca/professionnels/cabinets-societes-et-representants-autonomes/obligations-et-formalites-administratives/paiement-de-la-remuneration); Assur360 and SécuriGlobe run referral programs (SécuriGlobe: https://www.securiglobe.com/fr/programme-daffiliation-assurance-voyage/). Sources in `research/sources.md` and `data/sources_index.json`.

Order of magnitude, with one stated assumption: Quebec residents made 398,000 Q1 trips to the US in 2026. If 0.25 % of them (1,000 travellers) bought through the guide in one season at the published $50 per sale, that is $50,000. The assumption, not the rate, is what the first season will measure.

## Operator plan

Day 0 is done (engine, data, tests, page). Next: add the 20 most-sold Quebec plans to `data/clauses.json` (one pull request per wording, template: https://github.com/SeCuReDmE-main-dev/stability-checker/blob/main/.github/ISSUE_TEMPLATE/clause_update.md), then sign one referral agreement before the October renewal season.

| When | Step | Measure |
|---|---|---|
| Weeks 1–2 | 20 most-sold Quebec plans in `data/clauses.json`, each with source and test | 20 of 20 rules sourced |
| Week 3 | French page at assezstable.guide; the checker linked from each insurer page | 2 languages live |
| Weeks 4–6 | Referral agreement with one Quebec broker (SécuriGlobe or Assur360 program) | 1 signed |
| Each September | Re-read every wording for the new policy year; CI audit must pass | 0 stale rules |

Live product: https://securedme-main-dev.github.io/stability-checker/

## Limits

10 plan rules, not the whole market. Clauses change every policy year; each rule carries its source and section so it can be rechecked. Not insurance advice.
