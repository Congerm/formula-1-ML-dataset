import pandas as pd

# Load datasets
flags = pd.read_csv("DATA/sessions_with_weather_and_yellow_flags.csv")
lengths = pd.read_csv("DATA/track_lengths.csv")
types = pd.read_csv("DATA/track_types.csv")
mapping = pd.read_csv("DATA/circuit_name_mapping.csv")

# Merge datasets
flags = (
    flags
    .merge(mapping, on="circuit_short_name", how="left")
    .merge(lengths, on="circuit", how="left")
    .merge(types, on="circuit", how="left")
)

# Verify results
print("Total rows:", len(flags))
print("Missing track lengths:", flags["lap_length_km"].isna().sum())
print("Missing track types:", flags["track_type"].isna().sum())

# Export
flags.to_csv("DATA/sessions_complete.csv", index=False)