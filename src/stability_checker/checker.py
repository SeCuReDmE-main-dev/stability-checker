"""Check which travel insurance stability clauses a traveller meets.

Information, not advice: the data paraphrases public policy wordings. Always read
the full wording at the source link and confirm with a licensed advisor.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "clauses.json"

CONDITIONS = ("heart", "lung", "diabetes", "other")
CHANGES = (
    "dose",
    "new_drug",
    "cholesterol_medication",
    "brand_to_generic",
    "routine_insulin_or_coumadin",
)


@dataclass(frozen=True)
class Result:
    plan_id: str
    insurer: str
    plan: str
    required_days: int
    passes: bool
    reason: str
    source: str


def load_plans(path: Path = DATA_FILE) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)["plans"]


def required_days(plan: dict, age: int, condition: str) -> int:
    if condition in plan.get("condition_overrides", {}):
        return int(plan["condition_overrides"][condition])
    for rule in plan["rules"]:
        if rule["min_age"] <= age <= rule["max_age"]:
            return int(rule["days"])
    raise ValueError(f"No rule covers age {age} in plan {plan['id']}")


def check(days_since_change: int, age: int, condition: str = "other",
          change: str = "dose", plans: list[dict] | None = None) -> list[Result]:
    if days_since_change < 0:
        raise ValueError("days_since_change must be zero or more")
    if not 0 <= age <= 120:
        raise ValueError("age must be between 0 and 120")
    if condition not in CONDITIONS:
        raise ValueError(f"condition must be one of {CONDITIONS}")
    if change not in CHANGES:
        raise ValueError(f"change must be one of {CHANGES}")

    results = []
    for plan in plans if plans is not None else load_plans():
        needed = required_days(plan, age, condition)
        if change in plan.get("ignored_changes", []):
            passes, reason = True, f"this wording does not count a '{change}' change"
        elif days_since_change >= needed:
            passes, reason = True, f"{days_since_change} days >= {needed} required"
        else:
            passes, reason = False, f"{days_since_change} days < {needed} required"
        results.append(Result(plan["id"], plan["insurer"], plan["plan"], needed,
                              passes, reason, plan["source"]))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, required=True, help="days since the last medication change")
    parser.add_argument("--age", type=int, required=True)
    parser.add_argument("--condition", choices=CONDITIONS, default="other")
    parser.add_argument("--change", choices=CHANGES, default="dose")
    args = parser.parse_args(argv)

    for r in check(args.days, args.age, args.condition, args.change):
        mark = "PASS" if r.passes else "FAIL"
        print(f"[{mark}] {r.insurer} - {r.plan}: {r.reason}\n       {r.source}")
    print("\nInformation, not advice. Read the full wording and confirm with a licensed advisor.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
