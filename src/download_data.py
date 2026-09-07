"""
Fetch the Inside Airbnb Cape Town snapshot.

Three files, about 85 MB compressed, so they are not committed:

  listings.csv.gz          27,381 listings x 90 columns
  calendar.csv.gz          ~10M rows of forward nightly availability
  neighbourhoods.geojson   City of Cape Town ward boundaries

Inside Airbnb publishes by city and scrape date. If this snapshot is retired, browse
https://insideairbnb.com/get-the-data/ for the current date and update SNAPSHOT below.

Usage:
    python src/download_data.py
"""

from pathlib import Path
from urllib.request import Request, urlopen
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

SNAPSHOT = "2026-06-29"
BASE = f"https://data.insideairbnb.com/south-africa/wc/cape-town/{SNAPSHOT}"

FILES = [
    ("data/listings.csv.gz", "listings.csv.gz"),
    ("data/calendar.csv.gz", "calendar.csv.gz"),
    ("visualisations/neighbourhoods.geojson", "neighbourhoods.geojson"),
]


def fetch(remote: str, local: Path) -> None:
    request = Request(f"{BASE}/{remote}", headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=600) as response, local.open("wb") as target:
        shutil.copyfileobj(response, target)


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    print(f"Inside Airbnb — Cape Town, snapshot {SNAPSHOT}\n")

    for remote, name in FILES:
        target = DATA / name
        if target.exists():
            print(f"  {name:<26} already present ({target.stat().st_size/1e6:.0f} MB)")
            continue
        print(f"  {name:<26} downloading …", flush=True)
        try:
            fetch(remote, target)
        except Exception as exc:
            print(f"\nFailed on {name}: {exc}")
            print("If the snapshot has been retired, pick the current date from")
            print("https://insideairbnb.com/get-the-data/ and update SNAPSHOT in this file.")
            return 1
        print(f"  {name:<26} {target.stat().st_size/1e6:.0f} MB")

    print(f"\nAll files in {DATA}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
