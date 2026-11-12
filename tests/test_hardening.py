"""Invariants that must hold for every plan and every input."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stability_checker import check, load_plans  # noqa: E402
from stability_checker.checker import CHANGES, CONDITIONS  # noqa: E402

KEYS = {"id", "insurer", "plan", "rules", "condition_overrides", "ignored_changes", "summary", "source", "section"}


class DataSchema(unittest.TestCase):
    def setUp(self):
        self.plans = load_plans()

    def test_every_plan_has_exactly_the_expected_keys(self):
        for p in self.plans:
            self.assertEqual(set(p), KEYS, p["id"])

    def test_ids_are_kebab_case(self):
        for p in self.plans:
            self.assertRegex(p["id"], r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_age_rules_cover_at_least_0_to_120_without_gaps(self):
        for p in self.plans:
            rules = sorted(p["rules"], key=lambda r: r["min_age"])
            self.assertEqual(rules[0]["min_age"], 0, p["id"])
            self.assertGreaterEqual(rules[-1]["max_age"], 120, p["id"])
            for a, b in zip(rules, rules[1:]):
                self.assertEqual(a["max_age"] + 1, b["min_age"], p["id"])

    def test_days_are_positive_and_plausible(self):
        for p in self.plans:
            values = [r["days"] for r in p["rules"]] + list(p["condition_overrides"].values())
            for d in values:
                self.assertIsInstance(d, int)
                self.assertTrue(1 <= d <= 365, (p["id"], d))

    def test_overrides_and_ignored_changes_use_known_values(self):
        for p in self.plans:
            self.assertTrue(set(p["condition_overrides"]) <= set(CONDITIONS), p["id"])
            self.assertTrue(set(p["ignored_changes"]) <= set(CHANGES), p["id"])

    def test_sources_are_https_and_sections_named(self):
        for p in self.plans:
            self.assertTrue(p["source"].startswith("https://"), p["id"])
            self.assertTrue(p["section"].strip(), p["id"])
            self.assertTrue(10 <= len(p["summary"]) <= 300, p["id"])


class Behaviour(unittest.TestCase):
    def test_waiting_longer_never_closes_a_plan(self):
        days = list(range(0, 400, 1))
        for age in (40, 54, 55, 72, 90):
            for cond in CONDITIONS:
                for ch in CHANGES:
                    before = set()
                    for d in days:
                        now = {r.plan_id for r in check(d, age, cond, ch) if r.passes}
                        self.assertTrue(before <= now, (d, age, cond, ch, before - now))
                        before = now

    def test_every_plan_is_open_after_365_days(self):
        for age in (40, 72):
            for cond in CONDITIONS:
                self.assertTrue(all(r.passes for r in check(365, age, cond, "dose")))

    def test_no_plan_is_open_on_day_zero_for_a_counted_change(self):
        self.assertFalse(any(r.passes for r in check(0, 72, "other", "dose")))

    def test_ignored_change_passes_even_on_day_zero(self):
        r = {x.plan_id: x for x in check(0, 72, "other", "cholesterol_medication")}
        self.assertTrue(r["medipac-2026-2027"].passes)

    def test_bad_inputs_are_rejected(self):
        for args in [(-1, 72), (10, -1), (10, 121)]:
            with self.assertRaises(ValueError):
                check(*args)
        with self.assertRaises(ValueError):
            check(10, 72, condition="kidney")
        with self.assertRaises(ValueError):
            check(10, 72, change="vitamins")

    def test_result_count_matches_plan_count(self):
        self.assertEqual(len(check(60, 72)), len(load_plans()))


class PublishedFiles(unittest.TestCase):
    def test_llms_txt_points_to_existing_files(self):
        text = (ROOT / "docs" / "llms.txt").read_text(encoding="utf-8")
        for path in re.findall(r"/main/([\w./-]+)\)", text):
            self.assertTrue((ROOT / path).exists(), path)

    def test_coverage_matrix_matches_engine(self):
        lines = (ROOT / "data" / "coverage_matrix.csv").read_text(encoding="utf-8").strip().splitlines()[1:]
        for line in lines:
            d, a, c, n, total, _ = line.split(",", 5)
            got = sum(r.passes for r in check(int(d), int(a), c, "dose"))
            self.assertEqual(got, int(n), line)

    def test_clauses_json_is_utf8_and_sorted_by_insurer(self):
        raw = json.loads((ROOT / "data" / "clauses.json").read_text(encoding="utf-8"))
        insurers = [p["insurer"] for p in raw["plans"]]
        self.assertEqual(len(insurers), 10)


if __name__ == "__main__":
    unittest.main()
