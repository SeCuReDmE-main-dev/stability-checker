"""Build data/coverage_matrix.csv: how many plans a traveller still qualifies for,
by days since the last medication change, age and condition.

Usage: python benchmarks/coverage_matrix.py
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stability_checker import coverage  # noqa: E402

DAYS = [0, 7, 14, 30, 60, 90, 120, 182, 270, 365]
PROFILES = [(54, "other"), (72, "other"), (72, "heart"), (72, "diabetes")]
OUT = ROOT / "data" / "coverage_matrix.csv"


def main() -> None:
    rows = [row for age, condition in PROFILES for row in coverage(DAYS, age, condition)]
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")
    print("plans still open after a dose change (out of", rows[0]["plans_total"], ")")
    print("days  " + "  ".join(f"{a}/{c:<8}" for a, c in PROFILES))
    for days in DAYS:
        cells = [next(r["plans_passing"] for r in rows
                      if r["days_since_change"] == days and r["age"] == a and r["condition"] == c)
                 for a, c in PROFILES]
        print(f"{days:>4}  " + "  ".join(f"{n:>11}" for n in cells))


if __name__ == "__main__":
    main()
