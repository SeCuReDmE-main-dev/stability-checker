"""Winter (Q1) overnight trips by Quebec residents, by destination, 2019-2026.

Source: Statistics Canada Table 24-10-0071-01.
Usage: python -I scripts/statcan_winter_shift.py data/statcan/24100071.csv
"""
import sys

import pandas as pd

pd.set_option("display.width", 200)
df = pd.read_csv(sys.argv[1], usecols=["REF_DATE", "GEO", "Province of trip origin", "Visit duration",
                                       "Visit statistics", "VALUE", "STATUS"])
q = df[(df["Province of trip origin"] == "Quebec (trip origin)")
       & (df["Visit duration"] == "Overnight (Tourists)")
       & (df["Visit statistics"].isin(["Visits", "Nights"]))
       & (df["REF_DATE"].str.endswith("-01"))]
geos = ["United States of America", "North America", "Caribbean", "South and Central America", "Europe", "Overseas"]
t = q[q["GEO"].isin(geos)].pivot_table(index="REF_DATE", columns=["Visit statistics", "GEO"], values="VALUE", aggfunc="first")
print("NIGHTS (thousands), Q1 each year")
print(t["Nights"][geos].to_string())
print("\nVISITS (thousands), Q1 each year")
print(t["Visits"][geos].to_string())
s = q[(q["REF_DATE"].isin(["2025-01", "2026-01"])) & (q["GEO"].isin(geos))][["REF_DATE", "GEO", "Visit statistics", "STATUS"]]
print("\nQuality flags 2025-01 / 2026-01:")
print(s.pivot_table(index=["GEO", "Visit statistics"], columns="REF_DATE", values="STATUS", aggfunc="first").to_string())
