# stability-checker

[![CI](https://github.com/SeCuReDmE-main-dev/stability-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/SeCuReDmE-main-dev/stability-checker/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests: 8 passing](https://img.shields.io/badge/tests-8%20passing-brightgreen)
[![Concept submitted to We The Flywheel – Find the Gap 2026](https://img.shields.io/badge/concept-submitted%20to%20We%20The%20Flywheel%20%E2%80%93%20Find%20the%20Gap%202026-6f42c1)](NOTICE)
![Built with AI agents](https://img.shields.io/badge/built%20with-AI%20agents-black)

> **Information, not advice.** This tool paraphrases public travel insurance wordings. Read the full wording at each source link and confirm with a licensed advisor before you buy.

## English

**The question:** *"My medication changed 60 days ago. Which travel policies still cover me this winter?"*

Travel medical policies sold to Quebec snowbirds exclude pre-existing conditions that were not "stable" for a set period before departure. That period ranges from 7 to 365 days, depends on age and condition, and some wordings ignore certain changes (Medipac does not count a cholesterol medication change). No public page puts these clauses side by side. This repository does, as data and as a tested checker.

```bash
git clone https://github.com/SeCuReDmE-main-dev/stability-checker
cd stability-checker
PYTHONPATH=src python -m stability_checker --days 60 --age 72 --condition other --change dose
python -m unittest discover -s tests
```

Output for that example: every plan with a 90-day or longer window fails; only the 7-day reduced-stability option passes.

| Plan | Window | Note |
|---|---|---|
| Desjardins | 182 days at 55+, 90 under 55 | 90 days with the paid "Stabilité 3 mois" option |
| Medipac 2026-2027 | 90 days | Cholesterol medication changes do not count |
| Croix Bleue du Québec | 3 months | Heart: nitroglycerine more than once in 7 days excludes |
| TuGo Gold / Silver / Bronze | 90 / 180 / 180 days | Bronze: 365 days for heart, lung, diabetes |
| TuGo 7-day option | 7 days | As listed by a broker; confirm in the current wording |
| Manulife All-Inclusive (trip cancellation) | 3 or 12 months | 12 months when cancellation cover is 20,000 dollars or more |

Data: [`data/clauses.json`](data/clauses.json). Every entry has its source link and section. Research trail: [`research/`](research/). Market figures: [`benchmarks/`](benchmarks/).

## Français

**La question :** *« Mon médicament a changé il y a 60 jours. Quelles polices d'assurance voyage me couvrent encore cet hiver ? »*

Ce dépôt met côte à côte les clauses de stabilité des polices achetées par les snowbirds québécois, sous forme de données et d'un vérificateur testé. Chaque clause renvoie à son contrat source. **Ce n'est pas un conseil** : lisez le contrat complet et confirmez avec un conseiller titulaire d'un permis.

## Project files

[`HUMAN.md`](HUMAN.md) · [`AGENTS.md`](AGENTS.md) · [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`SECURITY.md`](SECURITY.md) · [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) · [`CHANGELOG.md`](CHANGELOG.md) · [`NOTICE`](NOTICE) · [`CITATION.cff`](CITATION.cff)

## License

Code and data structure: [Apache-2.0](LICENSE). Insurer names and policy wordings belong to their owners and are quoted briefly for reference.
