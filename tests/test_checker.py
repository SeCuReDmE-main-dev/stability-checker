import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stability_checker import check, coverage, load_plans  # noqa: E402


def by_id(results):
    return {r.plan_id: r for r in results}


class DataIntegrity(unittest.TestCase):
    def test_every_plan_has_a_source_and_rules(self):
        for plan in load_plans():
            self.assertTrue(plan["source"].startswith("https://"), plan["id"])
            self.assertTrue(plan["rules"], plan["id"])

    def test_plan_ids_are_unique(self):
        ids = [p["id"] for p in load_plans()]
        self.assertEqual(len(ids), len(set(ids)))


class SixtyDayDoseChange(unittest.TestCase):
    """The question from the entry: my dose changed 60 days ago."""

    def setUp(self):
        self.r = by_id(check(days_since_change=60, age=72, condition="other", change="dose"))

    def test_fails_90_day_and_longer_windows(self):
        for plan_id in ("desjardins-standard", "desjardins-stability-3-months", "medipac-2026-2027",
                        "croix-bleue-quebec", "tugo-gold", "tugo-silver", "tugo-bronze"):
            self.assertFalse(self.r[plan_id].passes, plan_id)

    def test_passes_only_the_7_day_option(self):
        self.assertTrue(self.r["tugo-7-day-option"].passes)


class AgeAndConditionRules(unittest.TestCase):
    def test_desjardins_uses_182_days_at_55_and_older(self):
        self.assertEqual(by_id(check(100, 55))["desjardins-standard"].required_days, 182)
        self.assertEqual(by_id(check(100, 54))["desjardins-standard"].required_days, 90)

    def test_tugo_bronze_needs_365_days_for_heart(self):
        r = by_id(check(200, 70, condition="heart"))["tugo-bronze"]
        self.assertEqual(r.required_days, 365)
        self.assertFalse(r.passes)


class IgnoredChanges(unittest.TestCase):
    def test_medipac_ignores_cholesterol_medication_changes(self):
        r = by_id(check(10, 70, change="cholesterol_medication"))
        self.assertTrue(r["medipac-2026-2027"].passes)
        self.assertFalse(r["tugo-gold"].passes)


class Coverage(unittest.TestCase):
    def test_more_plans_open_up_as_time_passes(self):
        counts = [row["plans_passing"] for row in coverage([0, 30, 90, 182, 365], 72)]
        self.assertEqual(counts, sorted(counts))
        self.assertEqual(counts[-1], len(load_plans()))

    def test_day_zero_leaves_no_plan(self):
        self.assertEqual(coverage([0], 72)[0]["plans_passing"], 0)


class InputValidation(unittest.TestCase):
    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            check(-1, 70)
        with self.assertRaises(ValueError):
            check(10, 70, condition="unknown")


if __name__ == "__main__":
    unittest.main()
