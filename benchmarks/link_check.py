"""Open every source link in data/clauses.json and print its HTTP status.

Usage: python benchmarks/link_check.py
Some insurer sites block scripts (HTTP 403); check those in a browser.
"""
import concurrent.futures as cf
import json
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "clauses.json"


def status(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return response.status
    except Exception as error:  # noqa: BLE001
        return getattr(error, "code", type(error).__name__)


def main() -> None:
    urls = sorted({plan["source"] for plan in json.loads(DATA.read_text(encoding="utf-8"))["plans"]})
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        for url, code in zip(urls, pool.map(status, urls)):
            print(code, url)


if __name__ == "__main__":
    main()
