import csv
import re
import unicodedata
from io import StringIO
from pathlib import Path
from urllib.request import urlopen

lap_file = Path("lap 1 times by course") / "all_drivers_all_races_lap_times.csv"
out_file = Path("DATA") / "track_lengths.csv"
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

latest_laps = {}
with lap_file.open(newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        track = row["circuit"]
        race = (row["date"], int(row["lap_number"]))
        if track not in latest_laps or race > latest_laps[track]:
            latest_laps[track] = race

text = urlopen(url).read().decode("utf-8-sig")
track_data = {clean_name(row["circuit"]): row for row in csv.DictReader(StringIO(text))}

with out_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["circuit", "lap_length_km", "laps", "total_track_length_km"])
    for track in sorted(latest_laps):
        lookup = clean_name(name_fixes.get(track, track))
        length = float(track_data[lookup]["length_km"])
        laps = latest_laps[track][1]
        writer.writerow([track, length, laps, round(length * laps, 3)])

print(f"Saved {len(latest_laps)} tracks to {out_file}")
