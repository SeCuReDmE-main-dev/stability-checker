import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import json  # noqa: E402

from stability_checker.research import CRITERIA, audit, plan, simulate  # noqa: E402


class ResearchPlan(unittest.TestCase):
    def test_every_criterion_has_queries(self):
        keys = {k for k, _ in plan()}
        self.assertEqual(keys, {c.key for c in CRITERIA})

    def test_insurer_templates_expand(self):
        queries = [q for _, q in plan(["Medipac"])]
        self.assertTrue(any("Medipac" in q for q in queries))
        self.assertFalse(any("{insurer}" in q for q in queries))


class EvidenceAudit(unittest.TestCase):
    def test_missing_section_is_weak(self):
        rows = {r["criterion"]: r for r in audit("## Demand\nhttps://example.org 12 % and 400\n")}
        self.assertTrue(rows["demand"]["ok"])
        self.assertFalse(rows["money"]["ok"])

    def test_evidence_sheet_covers_every_criterion(self):
        text = (ROOT / "docs" / "evidence.md").read_text(encoding="utf-8")
        weak = [r["criterion"] for r in audit(text) if not r["ok"]]
        self.assertEqual(weak, [])


class RubricSimulation(unittest.TestCase):
    def test_empty_sheet_scores_zero_and_full_sheet_is_bounded(self):
        self.assertEqual(sum(r["weighted"] for r in simulate("", {})), 0)
        text = (ROOT / "docs" / "evidence.md").read_text(encoding="utf-8")
        index = json.loads((ROOT / "data" / "sources_index.json").read_text(encoding="utf-8"))
        for r in simulate(text, index):
            self.assertTrue(0 <= r["weighted"] <= r["weight"], r)

    def test_every_criterion_has_three_tagged_sources(self):
        index = json.loads((ROOT / "data" / "sources_index.json").read_text(encoding="utf-8"))
        for c in CRITERIA:
            n = sum(c.key in s["criteria"] for s in index["sources"])
            self.assertGreaterEqual(n, 2, c.key)
            
    def test_index_urls_are_https_and_unique(self):
        index = json.loads((ROOT / "data" / "sources_index.json").read_text(encoding="utf-8"))
        urls = [s["url"] for s in index["sources"]]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertTrue(all(u.startswith("https://") for u in urls))


if __name__ == "__main__":
    unittest.main()
