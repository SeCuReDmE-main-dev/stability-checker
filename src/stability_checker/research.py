"""Research planner and evidence audit, organised by the Find the Gap scoring criteria.

Two commands, standard library only:

    python -m stability_checker.research plan            # search queries per criterion
    python -m stability_checker.research audit FILE.md   # which criteria lack sourced numbers

`plan` turns the clause data into concrete searches (one per insurer and criterion), so a
deep search covers every point a reviewer checks. `audit` reads an evidence sheet and counts,
for each criterion section, the public links and the figures it contains.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from .checker import load_plans


@dataclass(frozen=True)
class Criterion:
    key: str
    weight: int
    heading: str          # section heading in the evidence sheet
    needs: str            # what counts as evidence
    queries: tuple[str, ...]


CRITERIA: tuple[Criterion, ...] = (
    Criterion("demand", 25, "Demand",
              "Real people asking the question, plus market size with a public source.",
              ('"stability period" travel insurance snowbird medication change site:reddit.com',
               'assurance voyage "période de stabilité" changement de médicament forum',
               'Statistics Canada 24-10-0071 Quebec residents trips United States',
               '"{insurer}" travel insurance claim denied pre-existing condition stable')),
    Criterion("gap", 20, "The gap",
              "What current answers leave out, shown with clause-level numbers.",
              ('"{insurer}" policy wording stability period days pdf',
               '"{insurer}" "stable" "90 days" OR "180 days" OR "365 days" pre-existing',
               'travel insurance comparison stability period side by side Canada')),
    Criterion("concept", 15, "The product",
              "A working product a reader can use, with a link.",
              ('travel insurance stability period calculator Canada',
               'pre-existing condition checker travel insurance tool')),
    Criterion("money", 15, "Money",
              "Published referral or affiliate rates and a named partner type.",
              ('travel insurance affiliate program commission Canada',
               'assurance voyage programme de référencement commission courtier Québec',
               'AMF "commission de référencement" assurance')),
    Criterion("plan", 10, "Operator plan",
              "Concrete next steps, owners and dates.",
              ('"{insurer}" travel insurance renewal date policy year wording update',)),
)


def plan(insurers: list[str] | None = None) -> list[tuple[str, str]]:
    """Return (criterion, query) pairs; templates with {insurer} expand per insurer."""
    if insurers is None:
        insurers = sorted({p["insurer"] for p in load_plans()})
    out: list[tuple[str, str]] = []
    for c in CRITERIA:
        for q in c.queries:
            if "{insurer}" in q:
                out.extend((c.key, q.format(insurer=i)) for i in insurers)
            else:
                out.append((c.key, q))
    return out


URL = re.compile(r"https?://[^\s)>\]|]+")
NUMBER = re.compile(r"(?<![\w/])[$−-]?\d[\d,.\s]*\s?%?")


def sections(markdown: str) -> dict[str, str]:
    """Split a Markdown document on '## ' headings."""
    parts: dict[str, str] = {}
    current = None
    for line in markdown.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            parts[current] = ""
        elif current is not None:
            parts[current] += line + "\n"
    return parts


def audit(markdown: str, min_links: int = 1, min_numbers: int = 2) -> list[dict]:
    """Score each criterion section: links, figures, and whether it meets the minimum."""
    found = sections(markdown)
    rows = []
    for c in CRITERIA:
        body = next((v for k, v in found.items() if k.lower().startswith(c.heading.lower())), None)
        links = len(set(URL.findall(body or "")))
        files = len(set(re.findall(r"`[\w./-]+\.(?:csv|json|md|py)`", body or "")))
        numbers = len(NUMBER.findall(body or ""))
        ok = body is not None and links >= min_links and numbers >= min_numbers
        rows.append({"criterion": c.key, "weight": c.weight, "section": body is not None,
                     "links": links, "files": files, "numbers": numbers, "ok": ok, "needs": c.needs})
    return rows


def simulate(markdown: str, index: dict) -> list[dict]:
    """Rubric coverage benchmark: how well each public criterion is backed by evidence.

    This is not a prediction of a judge's score. For each criterion it combines the share of
    targets met (3 public links in its section, 4 figures, 3 tagged sources in the index) and
    multiplies by the criterion's published weight.
    """
    tagged: dict[str, int] = {}
    for src in index.get("sources", []):
        for c in src.get("criteria", []):
            tagged[c] = tagged.get(c, 0) + 1
    rows = []
    for r in audit(markdown):
        cover = (0.5 * min(1, r["links"] / 3) + 0.3 * min(1, r["numbers"] / 4)
                 + 0.2 * min(1, tagged.get(r["criterion"], 0) / 3))
        rows.append({"criterion": r["criterion"], "weight": r["weight"], "links": r["links"],
                     "numbers": r["numbers"], "tagged_sources": tagged.get(r["criterion"], 0),
                     "coverage": round(cover, 2), "weighted": round(cover * r["weight"], 1)})
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="stability_checker.research", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan", help="print search queries per criterion")
    a = sub.add_parser("audit", help="check an evidence sheet")
    a.add_argument("file", type=Path)
    sim = sub.add_parser("simulate", help="rubric coverage benchmark to CSV")
    sim.add_argument("file", type=Path)
    sim.add_argument("--index", type=Path, default=Path("data/sources_index.json"))
    sim.add_argument("--out", type=Path, default=Path("data/rubric_coverage.csv"))
    args = ap.parse_args(argv)
    if args.cmd == "simulate":
        import csv
        import json
        rows = simulate(args.file.read_text(encoding="utf-8"),
                        json.loads(args.index.read_text(encoding="utf-8")))
        with args.out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        for r in rows:
            print(f"{r['criterion']:<8} coverage {r['coverage']:.2f}  {r['weighted']:>5} / {r['weight']}")
        covered = sum(r["weighted"] for r in rows)
        print(f"covered {covered:.1f} of {sum(r['weight'] for r in rows)} rubric points (opening paragraph not measured)")
        return 0
    if args.cmd == "plan":
        for key, q in plan():
            print(f"{key}\t{q}")
        return 0
    rows = audit(args.file.read_text(encoding="utf-8"))
    print("criterion  weight  links  files  numbers  status")
    for r in rows:
        print(f"{r['criterion']:<10} {r['weight']:>6} {r['links']:>6} {r['files']:>6} {r['numbers']:>8}  "
              f"{'OK' if r['ok'] else 'WEAK: ' + r['needs']}")
    return 0 if all(r["ok"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
