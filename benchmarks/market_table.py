"""Build data/market_quebec_q1.csv from Statistics Canada Table 24-10-0071-01.

Quebec residents, overnight trips abroad, Q1 (January to March), 2018 onward:
visits and nights by destination, with Statistics Canada quality flags.
Downloads the official table (about 6 MB). Statistics Canada Open Licence.

Usage: python benchmarks/market_table.py
"""
import csv
import io
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

URL = "https://www150.statcan.gc.ca/n1/tbl/csv/24100071-eng.zip"
OUT = Path(__file__).resolve().parents[1] / "data" / "market_quebec_q1.csv"
GEOS = ["United States of America", "Overseas", "Caribbean", "North America",
        "South and Central America", "Europe"]


def main() -> None:
    raw = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"}),
                                 timeout=120).read()
    df = pd.read_csv(zipfile.ZipFile(io.BytesIO(raw)).open("24100071.csv"),
                     usecols=["REF_DATE", "GEO", "Province of trip origin", "Visit duration",
                              "Visit statistics", "VALUE", "STATUS"])
    q = df[(df["Province of trip origin"] == "Quebec (trip origin)")
           & (df["Visit duration"] == "Overnight (Tourists)")
           & (df["Visit statistics"].isin(["Visits", "Nights"]))
           & (df["REF_DATE"].str.endswith("-01"))
           & (df["GEO"].isin(GEOS))]
    out = q.rename(columns={"REF_DATE": "quarter", "GEO": "destination", "Visit statistics": "measure",
                            "VALUE": "thousands", "STATUS": "quality_flag"})
    out = out[["quarter", "destination", "measure", "thousands", "quality_flag"]].sort_values(
        ["quarter", "destination", "measure"])
    out.to_csv(OUT, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"Wrote {len(out)} rows to {OUT.name}")
    latest = out[(out.quarter == out.quarter.max()) & (out.measure == "Visits")]
    print(latest.to_string(index=False))


if __name__ == "__main__":
    main()
