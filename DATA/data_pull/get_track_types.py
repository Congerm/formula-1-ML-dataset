import csv
import re
import unicodedata
from io import StringIO
from pathlib import Path
from urllib.request import urlopen

lap_file = Path("lap 1 times by course") / "all_drivers_all_races_lap_times.csv"
out_file = Path("DATA") / "track_types.csv"
url = "https://aidb.si/d/f1-circuits.csv"

name_fixes = {
    "Albert Park Grand Prix Circuit": "Albert Park Circuit",
    "Autodromo Enzo e Dino Ferrari": "Autodromo Internazionale Enzo e Dino Ferrari",
    "Circuit Park Zandvoort": "Circuit Zandvoort",
    "Las Vegas Strip Street Circuit": "Las Vegas Strip Circuit",
    "Suzuka Circuit": "Suzuka International Racing Course",
}

def clean_name(name):
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", name.lower())

tracks = set()
with lap_file.open(newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        tracks.add(row["circuit"])

text = urlopen(url).read().decode("utf-8-sig")
track_data = {clean_name(row["circuit"]): row for row in csv.DictReader(StringIO(text))}

with out_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["circuit", "track_type"])
    for track in sorted(tracks):
        lookup = clean_name(name_fixes.get(track, track))
        track_type = track_data[lookup]["type"].replace(" circuit", "")
        writer.writerow([track, track_type])

print(f"Saved {len(tracks)} tracks to {out_file}")
