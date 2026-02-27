import json

# File paths
file_2014 = "2014_election_with_year_Final.json"
file_2022 = "2022_election_with_year_Final.json"
file_2026 = "2026_election_with_year_Final.json"

combined_file = "combined.json"

# Load 2014 features
with open(file_2014, "r", encoding="utf-8") as f:
    data_2014 = json.load(f)
features_2014 = data_2014.get("features", [])

# Load 2022 features
with open(file_2022, "r", encoding="utf-8") as f:
    data_2022 = json.load(f)
features_2022 = data_2022.get("features", [])

# Load 2026 features
with open(file_2026, "r", encoding="utf-8") as f:
    data_2026 = json.load(f)
features_2026 = data_2026.get("features", [])

# Combine features
all_features = features_2014 + features_2022 + features_2026

# Create combined GeoJSON
combined_geojson = {
    "type": "FeatureCollection",
    "features": all_features
}

# Save to file
with open(combined_file, "w", encoding="utf-8") as f:
    json.dump(combined_geojson, f, ensure_ascii=False, indent=2)

print(f"Combined GeoJSON saved as {combined_file}")
